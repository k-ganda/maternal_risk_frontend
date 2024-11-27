FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/

# Upgrade pip and setuptools to the latest version
RUN pip install --upgrade pip setuptools

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV FLASK_APP=app.py

ENV FLASK_ENV=development

ENV PYTHONBUFFERED=1

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]