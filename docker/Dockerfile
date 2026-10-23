# scanet — portable container image for local and cloud deployments
FROM python:3.12-slim

LABEL description="scanet: Lightweight Web-Based Cybersecurity Toolkit"

# Scanner binaries are optional; the Python engines work without them.
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
        nmap mtr-tiny curl dnsutils ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /scanet

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOST=0.0.0.0 \
    PORT=8000

COPY backend/requirements.txt /scanet/requirements.txt
RUN python -m pip install --no-cache-dir --prefer-binary -r /scanet/requirements.txt

COPY backend/ /scanet/backend/
COPY frontend/ /scanet/frontend/
COPY wordlists/ /scanet/wordlists/

RUN mkdir -p /scanet/backend/data && \
    useradd --system --uid 10001 --create-home scanet && \
    chown -R scanet:scanet /scanet/backend/data

WORKDIR /scanet/backend
USER scanet

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD ["python", "-c", "import os, urllib.request; urllib.request.urlopen('http://127.0.0.1:%s/api/v1/system/health' % os.environ.get('PORT', '8000'), timeout=3)"]

CMD ["sh", "-c", "exec uvicorn main:app --host \"$HOST\" --port \"$PORT\""]
