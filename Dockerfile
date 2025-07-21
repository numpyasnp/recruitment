# Python 3.10 slim image kullan
FROM python:3.10-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-latex-recommended \
    texlive-publishers \
    texlive-science \
    texlive-lang-european \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını kopyala ve yükle
COPY pyproject.toml ./
COPY requirements.txt ./
RUN pip install uv && uv pip install --system -r pyproject.toml

# Uygulama kodlarını kopyala
COPY . .

# Django ayarlarını geçici olarak ayarla (collectstatic için)
ENV DJANGO_SETTINGS_MODULE=recruitment.settings

# Statik dosyaları topla (eğer STATIC_ROOT tanımlıysa)
RUN python manage.py collectstatic --noinput || echo "Static files collection skipped"

# Port 8000'i expose et
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Uygulamayı başlat
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
