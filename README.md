# IK Recruitment Platform

Bu proje, Django, Celery, PostgreSQL, Redis ve Flower ile geliştirilmiş bir işe alım (recruitment) platformudur. Tüm servisler Docker ile kolayca ayağa kaldırılabilir.

## Başlangıç

### 1. Gerekli Araçlar
- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/)

### 2. Projeyi Klonla
```bash
git clone <repo-url>
cd IK
```

### 3. Docker Servislerini Başlat
```bash
docker compose up -d --build
```
Bu komut aşağıdaki servisleri başlatır:
- Django Web (8000)
- PostgreSQL (5432)
- Redis (6379)
- Celery Worker
- Celery Beat
- Flower (5555)

### 4. Migration'ları Uygula
```bash
docker compose exec web python manage.py migrate
```

### 5. Süper Kullanıcı (Admin) Oluştur
```bash
docker compose exec web python manage.py createsuperuser
```
Komut satırındaki yönergeleri takip edin.

### 6. Uygulamaya Erişim
- Django Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)
- Health Check: [http://localhost:8000/health/](http://localhost:8000/health/)
- Flower (Celery Monitoring): [http://localhost:5555](http://localhost:5555)

### 7. Logları İzleme
```bash
docker compose logs -f
```
Belirli bir servisin loglarını izlemek için:
```bash
docker compose logs -f celery_worker
```

### 8. Servisleri Durdurmak
```bash
docker compose down
```

## Notlar
- Tüm ayarlar `.env` veya `docker-compose.yml` içindeki environment değişkenleriyle yönetilir.
- Migration'ları ve statik dosya toplama işlemlerini gerektiğinde manuel olarak çalıştırabilirsiniz.
- Celery görevlerini ve zamanlamalarını Flower arayüzünden izleyebilirsiniz.

---

Herhangi bir sorunla karşılaşırsanız logları kontrol edin veya `docker compose ps` ile servis durumlarını inceleyin.
