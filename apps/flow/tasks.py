import calendar
import celery
from collections import defaultdict
import os

from django.utils import timezone
from pylatex import Document, Section, Table, Tabular, NoEscape
from django.conf import settings

from apps.flow.models import CandidateActivityLog, Activity
from recruitment.celery import app


def latex_escape(text):
    """LaTeX için özel karakterleri escape eder."""
    if not isinstance(text, str):
        text = str(text)
    replace_map = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "\\": r"\textbackslash{}",
    }
    for char, repl in replace_map.items():
        text = text.replace(char, repl)
    return text


class WeeklyActivityReportPdf(celery.Task):
    """
    Yıl başından itibaren haftalık bazda, aktivite türüne göre kaç kayıt girildiğini hesaplar ve PDF olarak kaydeder.
    """

    name = "apps.flow.tasks.WeeklyActivityReportPdf"

    def run(self, *args, **kwargs):
        try:
            now = timezone.now()
            # todo: add early return if latex path does not exists
            # todo: add generic path like which pdflatex
            # latex_compiler_path = "/usr/bin/pdflatex"
            logs = CandidateActivityLog.objects.select_related("activity").from_year_start()

            activity_types = list(Activity.objects.values_list("name", flat=True))

            # Haftalık bazda gruplama
            weekly_counts = defaultdict(lambda: {activity_type: 0 for activity_type in activity_types})
            # todo: db level queries
            for log in logs:
                week = log.date_created.isocalendar()[1]  # ISO week number
                activity_name = log.activity.name
                weekly_counts[week][activity_name] += 1

            # PDF oluştur
            doc = Document()
            doc.preamble.append(NoEscape(r"\usepackage[utf8]{inputenc}"))
            doc.preamble.append(NoEscape(r"\usepackage[T1]{fontenc}"))
            doc.preamble.append(NoEscape(r"\usepackage[turkish]{babel}"))
            doc.preamble.append(NoEscape(r"\title{" + latex_escape("Weekly Activity Report") + "}"))
            doc.preamble.append(NoEscape(r"\date{" + now.strftime("%Y-%m-%d") + "}"))
            doc.append(NoEscape(r"\maketitle"))
            with doc.create(Section(latex_escape("Weekly Activity Counts Since Start of Year"))):
                with doc.create(Table()) as table:
                    header = [latex_escape("Week")] + [latex_escape(activity_type) for activity_type in activity_types]
                    with doc.create(Tabular("c" * len(header))) as tabular:
                        tabular.add_row(header)
                        tabular.add_hline()
                        for week in sorted(weekly_counts.keys()):
                            row = [latex_escape(week)] + [
                                latex_escape(weekly_counts[week][activity_type]) for activity_type in activity_types
                            ]
                            tabular.add_row(row)
            reports_dir = os.path.join(settings.BASE_DIR, "reports")
            os.makedirs(reports_dir, exist_ok=True)
            # todo: ASK! does file name need unique uuid prefix or file_name1 - file_name2 it's ok ?
            pdf_path = os.path.join(reports_dir, f"weekly_activity_report_{now.year}_{now.month:02d}")
            doc.generate_pdf(filepath=pdf_path, clean_tex=False)
            return {"status": "success", "file": pdf_path}
        except Exception as e:
            return {"status": "error", "message": str(e)}


class MonthlyActivityReportPdf(celery.Task):
    """
    Yıl başından itibaren aylık bazda, aktivite türüne göre kaç kayıt girildiğini hesaplar ve PDF olarak kaydeder.
    """

    name = "apps.flow.tasks.MonthlyActivityReportPdf"

    def run(self, *args, **kwargs):
        try:
            now = timezone.now()
            # todo: add early return if latex path does not exists
            # todo: add generic path like which pdflatex
            latex_compiler_path = "/usr/bin/pdflatex"
            logs = CandidateActivityLog.objects.select_related("activity").from_year_start()
            activity_types = list(Activity.objects.values_list("name", flat=True))
            # Aylık bazda gruplama
            monthly_counts = defaultdict(lambda: {atype: 0 for atype in activity_types})
            # todo: db level queries
            for log in logs:
                month = log.date_created.month
                activity_name = log.activity.name
                monthly_counts[month][activity_name] += 1

            doc = Document()
            doc.preamble.append(NoEscape(r"\usepackage[utf8]{inputenc}"))
            doc.preamble.append(NoEscape(r"\usepackage[T1]{fontenc}"))
            doc.preamble.append(NoEscape(r"\usepackage[turkish]{babel}"))
            doc.preamble.append(NoEscape(r"\title{" + latex_escape("Monthly Activity Report") + "}"))
            doc.preamble.append(NoEscape(r"\date{" + now.strftime("%Y-%m-%d") + "}"))
            doc.append(NoEscape(r"\maketitle"))
            with doc.create(Section(latex_escape("Monthly Activity Counts Since Start of Year"))):
                with doc.create(Table()) as table:
                    header = [latex_escape("Month")] + [latex_escape(activity_type) for activity_type in activity_types]
                    with doc.create(Tabular("c" * len(header))) as tabular:
                        tabular.add_row(header)
                        tabular.add_hline()
                        for month in sorted(monthly_counts.keys()):
                            month_name = calendar.month_name[month]
                            row = [latex_escape(month_name)] + [
                                latex_escape(monthly_counts[month][atype]) for atype in activity_types
                            ]
                            tabular.add_row(row)
            reports_dir = os.path.join(settings.BASE_DIR, "reports")
            os.makedirs(reports_dir, exist_ok=True)
            pdf_path = os.path.join(reports_dir, f"monthly_activity_report_{now.year}_{now.month:02d}")
            doc.generate_pdf(filepath=pdf_path, clean_tex=False)
            return {"status": "success", "file": pdf_path}
        except Exception as e:
            return {"status": "error", "message": str(e)}


app.register_task(WeeklyActivityReportPdf())
app.register_task(MonthlyActivityReportPdf())
