import celery
import os

from django.utils import timezone
from pylatex import Document, Section, Table, Tabular, NoEscape
from django.conf import settings

from apps.flow.models import CandidateActivityLog, Activity
from .helpers import latex_escape


class BaseActivityReportPdfTask(celery.Task):
    """
    Aktivite raporlarını PDF olarak kaydeden base celery task.
    Alt sınıflar gruplama ve başlık fonksiyonlarını override etmeli.
    """

    abstract = True

    def get_grouped_counts(self, logs, activity_types):
        """Alt sınıflar tarafından implement edilmeli."""
        raise NotImplementedError

    def get_title(self):
        """Alt sınıflar tarafından implement edilmeli."""
        raise NotImplementedError

    def get_section_title(self):
        """Alt sınıflar tarafından implement edilmeli."""
        raise NotImplementedError

    def get_header(self, activity_types):
        """Alt sınıflar tarafından implement edilmeli."""
        raise NotImplementedError

    def get_row(self, key, activity_types, grouped_counts):
        """Alt sınıflar tarafından implement edilmeli."""
        raise NotImplementedError

    def get_pdf_filename(self, now):
        """Alt sınıflar tarafından implement edilmeli."""
        raise NotImplementedError

    def run(self, *args, **kwargs):
        try:
            now = timezone.now()
            logs = CandidateActivityLog.objects.select_related("activity").from_year_start()
            activity_types = list(Activity.objects.values_list("name", flat=True))
            grouped_counts = self.get_grouped_counts(logs, activity_types)

            doc = Document()
            doc.preamble.append(NoEscape(r"\usepackage[utf8]{inputenc}"))
            doc.preamble.append(NoEscape(r"\usepackage[T1]{fontenc}"))
            doc.preamble.append(NoEscape(r"\usepackage[turkish]{babel}"))
            doc.preamble.append(NoEscape(r"\title{" + latex_escape(self.get_title()) + "}"))
            doc.preamble.append(NoEscape(r"\date{" + now.strftime("%Y-%m-%d") + "}"))
            doc.append(NoEscape(r"\maketitle"))
            with doc.create(Section(latex_escape(self.get_section_title()))):
                with doc.create(Table()) as table:
                    header = self.get_header(activity_types)
                    with doc.create(Tabular("c" * len(header))) as tabular:
                        tabular.add_row(header)
                        tabular.add_hline()
                        for key in sorted(grouped_counts.keys()):
                            row = self.get_row(key, activity_types, grouped_counts)
                            tabular.add_row(row)
            reports_dir = os.path.join(settings.BASE_DIR, "reports")
            os.makedirs(reports_dir, exist_ok=True)
            pdf_path = os.path.join(reports_dir, self.get_pdf_filename(now))
            doc.generate_pdf(filepath=pdf_path, clean_tex=False)
            return {"status": "success", "file": pdf_path}
        except Exception as e:
            return {"status": "error", "message": str(e)}
