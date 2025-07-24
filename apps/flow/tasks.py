import calendar
from collections import defaultdict

from apps.flow.base_tasks import BaseActivityReportPdfTask
from apps.flow.helpers import latex_escape
from recruitment.celery import app


class WeeklyActivityReportPdf(BaseActivityReportPdfTask):
    name = "apps.flow.tasks.WeeklyActivityReportPdf"

    def get_grouped_counts(self, logs, activity_types):
        weekly_counts = defaultdict(lambda: {atype: 0 for atype in activity_types})
        for log in logs:
            week = log.date_created.isocalendar()[1]
            activity_name = log.candidate_flow.activity.name
            weekly_counts[week][activity_name] += 1
        return weekly_counts

    def get_title(self):
        return "Weekly Activity Report"

    def get_section_title(self):
        return "Weekly Activity Counts Since Start of Year"

    def get_header(self, activity_types):
        return [latex_escape("Week")] + [latex_escape(atype) for atype in activity_types]

    def get_row(self, week, activity_types, grouped_counts):
        return [latex_escape(week)] + [latex_escape(grouped_counts[week][atype]) for atype in activity_types]

    def get_pdf_filename(self, now):
        return f"weekly_activity_report_{now.year}_{now.month:02d}"


class MonthlyActivityReportPdf(BaseActivityReportPdfTask):
    name = "apps.flow.tasks.MonthlyActivityReportPdf"

    def get_grouped_counts(self, logs, activity_types):
        monthly_counts = defaultdict(lambda: {atype: 0 for atype in activity_types})
        for log in logs:
            month = log.date_created.month
            activity_name = log.activity.name
            monthly_counts[month][activity_name] += 1
        return monthly_counts

    def get_title(self):
        return "Monthly Activity Report"

    def get_section_title(self):
        return "Monthly Activity Counts Since Start of Year"

    def get_header(self, activity_types):
        return [latex_escape("Month")] + [latex_escape(atype) for atype in activity_types]

    def get_row(self, month, activity_types, grouped_counts):
        month_name = calendar.month_name[month]
        return [latex_escape(month_name)] + [latex_escape(grouped_counts[month][atype]) for atype in activity_types]

    def get_pdf_filename(self, now):
        return f"monthly_activity_report_{now.year}_{now.month:02d}"


app.register_task(WeeklyActivityReportPdf())
app.register_task(MonthlyActivityReportPdf())
