import celery
from django.db import transaction
from django.utils import timezone

from recruitment.celery import app
from apps.job_posting.models import JobPosting


class DeactivateExpiredJobPostings(celery.Task):
    """
    Kapanış tarihi geçmiş iş ilanlarını otomatik olarak pasif statüsüne çeker.
    Bu görev her 3 dakikada bir çalışacak şekilde ayarlanmalıdır.
    """

    def run(self, *args, **kwargs):
        today = timezone.now().date()
        expired_job_postings = JobPosting.objects.expired_active()

        if not expired_job_postings.exists():
            return {
                "message": "Pasif hale getirilecek iş ilanı bulunamadı.",
                "deactivated_count": 0,
                "execution_date": today.isoformat(),
            }

        with transaction.atomic():
            # todo: add chunk
            count = expired_job_postings.update(is_active=False)
            print(f"{count} adet süresi dolmuş iş ilanı pasif hale getirildi.")

        return {
            "message": f"{count} adet süresi dolmuş iş ilanı pasif hale getirildi.",
            "deactivated_count": count,
            "execution_date": today.isoformat(),
        }


app.register_task(DeactivateExpiredJobPostings())
