# Gunakan Python 3.11 (Versi stabil untuk AI/YOLO)
FROM python:3.11-slim

# Install library sistem pendukung OpenCV (Mengatasi error libGL)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set folder kerja
WORKDIR /app

# Copy requirements dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy sisa kode
COPY . .

# Jalankan aplikasi
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--timeout", "120"]



CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "8", "--timeout", "0"]