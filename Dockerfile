FROM python:3.13.0-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
RUN python manage.py migrate
RUN python manage.py test
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "backend.wsgi"]

