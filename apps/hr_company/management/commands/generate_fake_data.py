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

    def handle(self, *args, **options):
        fake = Faker("tr_TR")

        # 1. İK Şirketleri
        hr_companies = []
        for _ in range(3):
            company = HRCompany.objects.create(name=fake.company())
            hr_companies.append(company)
        self.stdout.write(self.style.SUCCESS(f"{len(hr_companies)} adet İK Şirketi oluşturuldu."))

        # 2. Müşteri Şirketleri
        client_companies = []
        for _ in range(5):
            company = ClientCompany.objects.create(name=fake.company())
            client_companies.append(company)
        self.stdout.write(self.style.SUCCESS(f"{len(client_companies)} adet Müşteri Şirketi oluşturuldu."))

        # 3. İK Kullanıcıları
        hr_users = []
        for _ in range(10):
            hr_company = random.choice(hr_companies)
            name = fake.first_name()
            last_name = fake.last_name()
            email = fake.unique.email()
            user = HRUser.objects.create(
                hr_company=hr_company,
                name=name,
                last_name=last_name,
                email=email,
                is_active=True,
            )
            # Kullanıcıya rastgele müşteri şirketleri ata
            user.client_companies.set(random.sample(client_companies, k=random.randint(1, len(client_companies))))
            hr_users.append(user)
        self.stdout.write(self.style.SUCCESS(f"{len(hr_users)} adet İK Kullanıcısı oluşturuldu."))

        # 4. İş İlanları
        job_postings = []
        for _ in range(20):
            hr_user = random.choice(hr_users)
            hr_company = hr_user.hr_company
            client_company = random.choice(client_companies)
            title = fake.job()
            description = fake.text(max_nb_chars=300)
            closing_date = timezone.now().date() + timezone.timedelta(days=random.randint(7, 90))
            job = JobPosting.objects.create(
                hr_user=hr_user,
                hr_company=hr_company,
                client_company=client_company,
                title=title,
                description=description,
                closing_date=closing_date,
                is_active=True,
            )
            job_postings.append(job)
        self.stdout.write(self.style.SUCCESS(f"{len(job_postings)} adet İş İlanı oluşturuldu."))

        # 5. Adaylar
        candidates = []
        for _ in range(50):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.unique.email()
            phone = fake.phone_number()[:20]
            candidate = Candidate.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
            )
            candidates.append(candidate)
        self.stdout.write(self.style.SUCCESS(f"{len(candidates)} adet Aday oluşturuldu."))

        # 6. Eğitimler
        educations = []
        for candidate in candidates:
            for _ in range(random.randint(1, 3)):
                school = fake.company() + " Üniversitesi"
                department = fake.job()
                start_year = random.randint(2000, 2018)
                end_year = start_year + random.randint(2, 6)
                edu = Education.objects.create(
                    candidate=candidate,
                    school=school,
                    department=department,
                    start_date=timezone.datetime(start_year, 9, 1),
                    end_date=timezone.datetime(end_year, 6, 30),
                )
                educations.append(edu)
        self.stdout.write(self.style.SUCCESS(f"{len(educations)} adet Eğitim oluşturuldu."))

        # 7. İş Deneyimleri
        work_experiences = []
        for candidate in candidates:
            for _ in range(random.randint(1, 3)):
                company = fake.company()
                position = fake.job()
                start_year = random.randint(2010, 2021)
                end_year = start_year + random.randint(1, 5)
                tech_stack = ", ".join(fake.words(nb=random.randint(2, 5)))
                work = WorkExperience.objects.create(
                    candidate=candidate,
                    company=company,
                    position=position,
                    tech_stack=tech_stack,
                    start_date=timezone.datetime(start_year, 1, 1),
                    end_date=timezone.datetime(end_year, 12, 31),
                )
                work_experiences.append(work)
        self.stdout.write(self.style.SUCCESS(f"{len(work_experiences)} adet İş Deneyimi oluşturuldu."))
