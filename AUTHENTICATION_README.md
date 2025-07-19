# Authentication Endpoints

Bu proje hem JWT hem de Session authentication desteklemektedir.

## Endpoint'ler

### 1. JWT Authentication

#### Login (JWT)
```
POST /api/v1/auth/login/jwt
```

**Request Body:**
```json
{
    "email": "test@example.com",
    "password": "test123"
}
```

**Response:**
```json
{
    "user": {
        "id": 1,
        "name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "hr_company": 1,
        "client_companies": [],
        "is_active": true,
        "is_staff": false,
        "is_superuser": false
    },
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

#### Token Refresh
```
POST /api/v1/auth/refresh/jwt
```

**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### JWT ile API Kullanımı
JWT token'ı ile API çağrıları yaparken, Authorization header'ında Bearer token kullanın:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### 2. Session Authentication

#### Login (Session)
```
POST /api/v1/auth/login/session
```

**Request Body:**
```json
{
    "email": "test@example.com",
    "password": "test123"
}
```

**Response:**
```json
{
    "user": {
        "id": 1,
        "name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "hr_company": 1,
        "client_companies": [],
        "is_active": true,
        "is_staff": false,
        "is_superuser": false
    },
    "message": "Başarıyla giriş yapıldı"
}
```

#### Logout (Session)
```
POST /api/v1/auth/logout/session
```

**Response:**
```json
{
    "message": "Başarıyla çıkış yapıldı"
}
```

## Test Kullanıcısı Oluşturma

Test kullanıcısı oluşturmak için aşağıdaki komutu çalıştırın:

```bash
python manage.py create_test_user
```

Bu komut aşağıdaki test kullanıcısını oluşturacak:
- Email: test@example.com
- Şifre: test123

## Kurulum

1. Gerekli paketlerin yüklü olduğundan emin olun:
```bash
pip install djangorestframework-simplejwt
```

2. Migration'ları çalıştırın:
```bash
python manage.py migrate
```

3. Test kullanıcısı oluşturun:
```bash
python manage.py create_test_user
```

4. Sunucuyu başlatın:
```bash
python manage.py runserver
```

## Güvenlik Notları

- JWT token'ları 30 dakika geçerlidir
- Refresh token'ları 1 gün geçerlidir
- Session authentication için CSRF token gerekebilir
- Production ortamında SECRET_KEY'i değiştirmeyi unutmayın
