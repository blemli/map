FROM python:3.11-slim

# Install cron and required dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libboost-dev \
    libexpat1-dev \
    zlib1g-dev \
    libbz2-dev \
    cron \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy application files
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Modify the extraction script to save to the correct location
RUN sed -i 's|output_path = os.path.join(BASE_DIR, "winterthur.osm.pbf")|output_path = "/data/winterthur.osm.pbf"|g' extract-winterthur.py

# Create a wrapper script that runs the extraction once
RUN echo '#!/bin/bash\n\
python /app/extract-winterthur.py >> /data/extraction.log 2>&1\n\
' > /app/run-extraction.sh && chmod +x /app/run-extraction.sh

# Set up the cron job to run at 2 AM every day
RUN echo "0 2 * * * root /app/run-extraction.sh" > /etc/cron.d/extraction-cron && \
    chmod 0644 /etc/cron.d/extraction-cron && \
    crontab /etc/cron.d/extraction-cron

# Run extraction once on startup to ensure data is available immediately
RUN echo '#!/bin/bash\n\
echo "Running initial extraction..."\n\
/app/run-extraction.sh\n\
echo "Starting cron service..."\n\
cron -f\n\
' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Set the entrypoint to our script
ENTRYPOINT ["/app/entrypoint.sh"]