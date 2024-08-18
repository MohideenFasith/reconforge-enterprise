FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app
RUN addgroup --system reconforge && adduser --system --ingroup reconforge reconforge
COPY requirements.lock pyproject.toml README.md ./
RUN python -m pip install --no-cache-dir -r requirements.lock
COPY src ./src
RUN python -m pip install --no-cache-dir -e . --no-deps
USER reconforge
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/v1/health', timeout=2)"
CMD ["uvicorn", "reconforge.main:app", "--host", "0.0.0.0", "--port", "8000"]
