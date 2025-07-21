from typing import List

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from apps.hr_company.models import HRCompany
from apps.client_company.models import ClientCompany
from faker import Faker
from apps.hr_user.models import HRUser
from apps.job_posting.models import JobPosting
from apps.candidate.models import Candidate, Education, WorkExperience
from django.utils import timezone
import random


class Command(BaseCommand):
    help = "Sahte (fake) İK, müşteri şirketi, İK kullanıcısı, iş ilanı, aday vb. verileri oluşturur."

    def _create_hr_companies(self, count: int, fake: Faker):
        hr_companies = [HRCompany(name=fake.company()) for _ in range(count)]
        HRCompany.objects.bulk_create(hr_companies, ignore_conflicts=False, batch_size=500)
        self.stdout.write(self.style.SUCCESS(f"{len(hr_companies)} adet İK Şirketi oluşturuldu."))
        return hr_companies

    def _create_client_company(self, count: int, fake: Faker):
        client_companies = [ClientCompany(name=fake.company()) for _ in range(count)]
        ClientCompany.objects.bulk_create(client_companies, ignore_conflicts=False, batch_size=500)
        self.stdout.write(self.style.SUCCESS(f"{len(client_companies)} adet Müşteri Şirketi oluşturuldu."))
        return client_companies

    def _create_hr_user(
        self, count: int, fake: Faker, hr_companies: List[HRCompany], client_companies: List[ClientCompany]
    ):
        hr_users = []
        for _ in range(count):
            hr_company = random.choice(hr_companies)
            name = fake.first_name()
            last_name = fake.last_name()
            email = fake.unique.email()
            plain_password = "test123"
            hashed_password = make_password(plain_password)
            user = HRUser.objects.create(
                hr_company=hr_company,
                name=name,
                last_name=last_name,
                email=email,
                is_active=True,
                password=hashed_password,
            )
            # Kullanıcıya rastgele müşteri şirketleri ata
            user.client_companies.set(random.sample(client_companies, k=random.randint(1, len(client_companies))))
            hr_users.append(user)
        self.stdout.write(self.style.SUCCESS(f"{len(hr_users)} adet İK Kullanıcısı oluşturuldu."))
        return hr_users

    def _create_job_posting(
        self, count: int, fake: Faker, hr_users: List[HRUser], client_companies: List[ClientCompany]
    ):
        job_postings = [
            JobPosting(
                hr_user=random.choice(hr_users),
                hr_company=random.choice(hr_users).hr_company,
                client_company=random.choice(client_companies),
                title=fake.job(),
                description=fake.text(max_nb_chars=300),
                closing_date=timezone.now().date() + timezone.timedelta(days=random.randint(7, 90)),
                is_active=True,
            )
            for _ in range(count)
        ]
        JobPosting.objects.bulk_create(job_postings, ignore_conflicts=False, batch_size=500)
        self.stdout.write(self.style.SUCCESS(f"{len(job_postings)} adet İş İlanı oluşturuldu."))
        return job_postings

    def _create_candidates(self, count: int, fake: Faker):
        candidates = [
            Candidate(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                phone=fake.phone_number()[:20],
            )
            for _ in range(count)
        ]
        Candidate.objects.bulk_create(candidates, ignore_conflicts=False, batch_size=500)
        self.stdout.write(self.style.SUCCESS(f"{len(candidates)} adet Aday oluşturuldu."))
        return candidates

    def _create_educations(self, fake: Faker, candidates: List[Candidate]):
        educations = [
            Education(
                candidate=candidate,
                school=fake.company() + " Üniversitesi",
                department=fake.job(),
                start_date=timezone.datetime(start_year := random.randint(2000, 2018), 9, 1),
                end_date=timezone.datetime(start_year + random.randint(2, 6), 6, 30),
            )
            for candidate in candidates
            for _ in range(random.randint(1, 3))
        ]
        Education.objects.bulk_create(educations, batch_size=500)
        self.stdout.write(self.style.SUCCESS(f"{len(educations)} adet Eğitim oluşturuldu."))
        return educations

    def _create_work_experiences(self, fake: Faker, candidates: List[Candidate]):
        work_experiences = [
            WorkExperience(
                candidate=candidate,
                company=fake.company(),
                position=fake.job(),
                tech_stack=", ".join(fake.words(nb=random.randint(2, 5))),
                start_date=timezone.datetime(
                    start_year := random.randint(2010, 2021), 1, 1
                ),  # Python 3.8+ Walrus operatörü
                end_date=timezone.datetime((start_year + random.randint(1, 5)), 12, 31),
            )
            for candidate in candidates
            for _ in range(random.randint(1, 3))
        ]
        WorkExperience.objects.bulk_create(work_experiences, batch_size=500)
        self.stdout.write(self.style.SUCCESS(f"{len(work_experiences)} adet İş Deneyimi oluşturuldu."))
        return work_experiences

    def handle(self, *args, **options):
        fake = Faker("tr_TR")
        HR_COMPANY_COUNT = 3
        CLIENT_COMPANIES_COUNT = 5
        HR_USERS_COUNT = 10
        JOB_POSTING_COUNT = 20
        CANDIDATE_COUNT = 50

        # 1. ik_company
        hr_companies = self._create_hr_companies(HR_COMPANY_COUNT, fake)
        # 2. client_company
        client_companies = self._create_client_company(CLIENT_COMPANIES_COUNT, fake)
        # 3. hr_user
        hr_users = self._create_hr_user(HR_USERS_COUNT, fake, hr_companies, client_companies)
        # 4. job post
        job_postings = self._create_job_posting(JOB_POSTING_COUNT, fake, hr_users, client_companies)
        # 5. candidate
        candidates = self._create_candidates(CANDIDATE_COUNT, fake)
        # 6. Education
        educations = self._create_educations(fake, candidates)
        # 7. WorkExperience
        work_experiences = self._create_work_experiences(fake, candidates)
