# scanet — Docker Container
# Lightweight Python base with Alpine for minimal image size.
FROM python:3.12-slim

LABEL maintainer="mjishaan59-cell"
LABEL description="scanet: Lightweight Web-Based Cybersecurity Toolkit"
LABEL version="0.1.0"

# System packages: nmap, mtr, curl, wget, dig, unzip
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
        nmap mtr-tiny curl wget dnsutils unzip ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Create scanet tool binary directory
RUN mkdir -p /opt/scanet/bin
ENV PATH="/opt/scanet/bin:${PATH}"

# Set work directory
WORKDIR /scanet

# Install Python dependencies
COPY backend/requirements.txt /scanet/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ /scanet/backend/

# Copy frontend
COPY frontend/ /scanet/frontend/

# Copy wordlists
COPY wordlists/ /scanet/wordlists/

# Create data directory
RUN mkdir -p /scanet/backend/data

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s \
    CMD curl -f http://localhost:8000/api/v1/system/health || exit 1

# Start server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
