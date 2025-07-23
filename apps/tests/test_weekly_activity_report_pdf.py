import os
from django.test import TestCase, override_settings
from model_bakery import baker
from django.utils import timezone
from apps.flow.models import Activity, CandidateActivityLog
from apps.flow.tasks import WeeklyActivityReportPdf
from libs.tests import create_candidate_flow


TEST_REPORTS_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../reports_test_output"))


class WeeklyActivityReportPdfTaskTest(TestCase):
    def setUp(self):
        self.activities = [
            baker.make(Activity, name="Telefon Görüşmesi"),
            baker.make(Activity, name="Mülakat"),
        ]
        self.candidate_flow = create_candidate_flow()
        now = timezone.now()
        for week, activity in enumerate(self.activities, start=1):
            for i in range(3):
                log_date = now - timezone.timedelta(weeks=(2 - week), days=i)
                baker.make(
                    CandidateActivityLog,
                    candidate_flow=self.candidate_flow,
                    activity=activity,
                    date_created=log_date,
                )

    @override_settings(BASE_DIR=TEST_REPORTS_BASE)
    def test_weekly_activity_report_pdf_task(self):
        task = WeeklyActivityReportPdf()
        result = task.run()
        self.assertEqual(result["status"], "success")
        pdf_path = result["file"] + ".pdf"
        tex_path = result["file"] + ".tex"
        self.assertTrue(os.path.exists(pdf_path))
        self.assertGreater(os.path.getsize(pdf_path), 0)
        os.remove(pdf_path)
        os.remove(tex_path)
