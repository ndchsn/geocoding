# Gunakan image Python dari Docker Hub
FROM python:3.9-slim

# Tentukan direktori kerja
WORKDIR /app

# Salin file requirement dan app ke dalam container
COPY requirements.txt /app/requirements.txt
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 untuk Cloud Run
EXPOSE 8080

# Tentukan perintah untuk menjalankan aplikasi
CMD ["python", "app.py"]
