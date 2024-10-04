FROM python:3.11-alpine

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Project files
COPY web_app web_app

EXPOSE 5000
ENTRYPOINT ["python", "web_app/app.py"]
