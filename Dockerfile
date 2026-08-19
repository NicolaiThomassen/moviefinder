FROM python:3.12-slim

WORKDIR /app

COPY setup.py README.md CHANGELOG.txt /app/

RUN pip install --no-cache-dir .

COPY movieFinder/ ./movieFinder/

CMD ["python", "-m", "movieFinder.main"]