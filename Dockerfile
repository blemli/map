# Dockerfile

# Basis-Image mit Python 3.11
FROM python:3.11-slim

# Arbeitsverzeichnis
WORKDIR /app

# Unbuffered stdout/stderr
ENV PYTHONUNBUFFERED=1

# Virtual Environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Abhängigkeiten kopieren und installieren (inkl. pip-Upgrade)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Gesamten Anwendungscode kopieren
COPY . .

# Port freigeben
EXPOSE 5000

# Startkommando mit gunicorn (Produktivserver)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
