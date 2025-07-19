# IK API Kullanım Kılavuzu

## Genel Bilgiler

- **Base URL**: `http://localhost:8000`
- **API Version**: v1
- **Authentication**: JWT Token (Bearer)
- **Content-Type**: `application/json`

## Kurulum

### 1. Postman Collection'ı İçe Aktarma
1. Postman'i açın
2. "Import" butonuna tıklayın
3. `IK_API_Postman_Collection.json` dosyasını seçin
4. Collection'ı içe aktarın

### 2. Environment Variables Ayarlama
Collection'da aşağıdaki değişkenleri ayarlayın:
- `base_url`: `http://localhost:8000`
- `access_token`: (Login sonrası otomatik doldurulacak)
- `refresh_token`: (Login sonrası otomatik doldurulacak)

## Authentication

### Login
```http
POST {{base_url}}/api/v1/auth/login/
Content-Type: application/json

{
    "email": "hr@example.com",
    "password": "password123"
}
```

**Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Token Yenileme
```http
POST {{base_url}}/api/v1/auth/refresh/
Content-Type: application/json

{
    "refresh": "{{refresh_token}}"
}
```

## HR Users API

### HR Kullanıcıları Listele
```http
GET {{base_url}}/api/v1/hr-users/
Authorization: Bearer {{access_token}}
```

### HR Kullanıcısı Oluştur
```http
POST {{base_url}}/api/v1/hr-users/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "name": "Ahmet",
    "last_name": "Yılmaz",
    "email": "ahmet.yilmaz@example.com",
    "password": "password123",
    "hr_company": 1,
    "client_companies": [1, 2]
}
```

### HR Kullanıcısı Getir
```http
GET {{base_url}}/api/v1/hr-users/1/
Authorization: Bearer {{access_token}}
```

### HR Kullanıcısı Güncelle
```http
PUT {{base_url}}/api/v1/hr-users/1/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "name": "Ahmet",
    "last_name": "Yılmaz",
    "email": "ahmet.yilmaz@example.com",
    "hr_company": 1,
    "client_companies": [1, 2]
}
```

### HR Kullanıcısı Sil
```http
DELETE {{base_url}}/api/v1/hr-users/1/
Authorization: Bearer {{access_token}}
```

## Job Postings API

### İş İlanlarını Listele
```http
GET {{base_url}}/api/v1/job-postings/
Authorization: Bearer {{access_token}}
```

### Filtrelenmiş İş İlanları
```http
GET {{base_url}}/api/v1/job-postings/?hr_company=1&is_active=true
Authorization: Bearer {{access_token}}
```

**Filtreleme Seçenekleri:**
- `hr_company`: HR şirket ID'si
- `client_company`: Client şirket ID'si
- `is_active`: Aktiflik durumu (true/false)

### İş İlanı Oluştur
```http
POST {{base_url}}/api/v1/job-postings/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "hr_company": 1,
    "client_company": 1,
    "title": "Senior Python Developer",
    "description": "Deneyimli Python geliştirici arıyoruz. Django, PostgreSQL bilgisi gerekli.",
    "closing_date": "2024-12-31",
    "is_active": true
}
```

### İş İlanı Getir
```http
GET {{base_url}}/api/v1/job-postings/1/
Authorization: Bearer {{access_token}}
```

### İş İlanı Güncelle
```http
PUT {{base_url}}/api/v1/job-postings/1/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "hr_company": 1,
    "client_company": 1,
    "title": "Senior Python Developer (Updated)",
    "description": "Deneyimli Python geliştirici arıyoruz. Django, PostgreSQL bilgisi gerekli. React bilgisi tercih sebebi.",
    "closing_date": "2024-12-31",
    "is_active": true
}
```

### İş İlanı Sil
```http
DELETE {{base_url}}/api/v1/job-postings/1/
Authorization: Bearer {{access_token}}
```

### İş İlanını Aktifleştir
```http
POST {{base_url}}/api/v1/job-postings/1/activate/
Authorization: Bearer {{access_token}}
```

### İş İlanını Pasifleştir
```http
POST {{base_url}}/api/v1/job-postings/1/deactivate/
Authorization: Bearer {{access_token}}
```

## Candidates API

### Adayları Listele
```http
GET {{base_url}}/api/v1/candidates/
Authorization: Bearer {{access_token}}
```

### Filtrelenmiş Adaylar
```http
GET {{base_url}}/api/v1/candidates/?first_name=Ahmet&email=ahmet
Authorization: Bearer {{access_token}}
```

**Filtreleme Seçenekleri:**
- `first_name`: İsim (içerir arama)
- `last_name`: Soyad (içerir arama)
- `email`: E-posta (içerir arama)

### Aday Oluştur
```http
POST {{base_url}}/api/v1/candidates/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "first_name": "Ahmet",
    "last_name": "Yılmaz",
    "email": "ahmet.yilmaz@example.com",
    "phone": "+90 555 123 4567"
}
```

### Aday Getir
```http
GET {{base_url}}/api/v1/candidates/1/
Authorization: Bearer {{access_token}}
```

### Aday Güncelle
```http
PUT {{base_url}}/api/v1/candidates/1/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "first_name": "Ahmet",
    "last_name": "Yılmaz",
    "email": "ahmet.yilmaz@example.com",
    "phone": "+90 555 987 6543"
}
```

### Aday Sil
```http
DELETE {{base_url}}/api/v1/candidates/1/
Authorization: Bearer {{access_token}}
```

### Adayın Eğitim Bilgilerini Getir
```http
GET {{base_url}}/api/v1/candidates/1/educations/
Authorization: Bearer {{access_token}}
```

### Adaya Eğitim Bilgisi Ekle
```http
POST {{base_url}}/api/v1/candidates/1/educations/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "school": "İstanbul Teknik Üniversitesi",
    "department": "Bilgisayar Mühendisliği",
    "start_date": "2018-09-01",
    "end_date": "2022-06-30"
}
```

### Adayın İş Deneyimi Bilgilerini Getir
```http
GET {{base_url}}/api/v1/candidates/1/work_experiences/
Authorization: Bearer {{access_token}}
```

### Adaya İş Deneyimi Bilgisi Ekle
```http
POST {{base_url}}/api/v1/candidates/1/work_experiences/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "company": "TechCorp",
    "position": "Python Developer",
    "tech_stack": "Python, Django, PostgreSQL, React",
    "start_date": "2022-07-01",
    "end_date": "2024-01-31"
}
```

## Educations API

### Eğitim Bilgilerini Listele
```http
GET {{base_url}}/api/v1/educations/
Authorization: Bearer {{access_token}}
```

### Filtrelenmiş Eğitim Bilgileri
```http
GET {{base_url}}/api/v1/educations/?candidate=1
Authorization: Bearer {{access_token}}
```

### Eğitim Bilgisi Oluştur
```http
POST {{base_url}}/api/v1/educations/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "candidate": 1,
    "school": "Boğaziçi Üniversitesi",
    "department": "Matematik",
    "start_date": "2019-09-01",
    "end_date": "2023-06-30"
}
```

### Eğitim Bilgisi Getir
```http
GET {{base_url}}/api/v1/educations/1/
Authorization: Bearer {{access_token}}
```

### Eğitim Bilgisi Güncelle
```http
PUT {{base_url}}/api/v1/educations/1/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "candidate": 1,
    "school": "Boğaziçi Üniversitesi",
    "department": "Bilgisayar Mühendisliği",
    "start_date": "2019-09-01",
    "end_date": "2023-06-30"
}
```

### Eğitim Bilgisi Sil
```http
DELETE {{base_url}}/api/v1/educations/1/
Authorization: Bearer {{access_token}}
```

## Work Experiences API

### İş Deneyimi Bilgilerini Listele
```http
GET {{base_url}}/api/v1/work-experiences/
Authorization: Bearer {{access_token}}
```

### Filtrelenmiş İş Deneyimi Bilgileri
```http
GET {{base_url}}/api/v1/work-experiences/?candidate=1
Authorization: Bearer {{access_token}}
```

### İş Deneyimi Bilgisi Oluştur
```http
POST {{base_url}}/api/v1/work-experiences/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "candidate": 1,
    "company": "StartupXYZ",
    "position": "Full Stack Developer",
    "tech_stack": "Python, Django, React, PostgreSQL, Docker",
    "start_date": "2023-02-01",
    "end_date": "2024-01-31"
}
```

### İş Deneyimi Bilgisi Getir
```http
GET {{base_url}}/api/v1/work-experiences/1/
Authorization: Bearer {{access_token}}
```

### İş Deneyimi Bilgisi Güncelle
```http
PUT {{base_url}}/api/v1/work-experiences/1/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "candidate": 1,
    "company": "StartupXYZ",
    "position": "Senior Full Stack Developer",
    "tech_stack": "Python, Django, React, PostgreSQL, Docker, Kubernetes",
    "start_date": "2023-02-01",
    "end_date": "2024-01-31"
}
```

### İş Deneyimi Bilgisi Sil
```http
DELETE {{base_url}}/api/v1/work-experiences/1/
Authorization: Bearer {{access_token}}
```

## Hata Kodları

| Kod | Açıklama |
|-----|----------|
| 200 | Başarılı |
| 201 | Oluşturuldu |
| 400 | Hatalı İstek |
| 401 | Yetkisiz Erişim |
| 403 | Yasaklı |
| 404 | Bulunamadı |
| 500 | Sunucu Hatası |

## Örnek Kullanım Senaryoları

### 1. Yeni İş İlanı Oluşturma ve Aday Ekleme
1. Login olun
2. İş ilanı oluşturun
3. Aday oluşturun
4. Adaya eğitim bilgisi ekleyin
5. Adaya iş deneyimi bilgisi ekleyin

### 2. Aday Arama ve Filtreleme
1. Adayları listele
2. İsme göre filtrele
3. E-posta adresine göre filtrele
4. Adayın detaylarını görüntüle

### 3. İş İlanı Yönetimi
1. Aktif iş ilanlarını listele
2. İş ilanını güncelle
3. İş ilanını pasifleştir
4. İş ilanını aktifleştir

## Notlar

- Tüm tarih formatları: `YYYY-MM-DD`
- JWT token'lar 30 dakika geçerlidir
- Refresh token'lar 1 gün geçerlidir
- Tüm endpoint'ler authentication gerektirir
- Filtreleme parametreleri opsiyoneldir
