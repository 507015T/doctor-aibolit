
FROM python:3.13.0-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python3.13 manage.py runserver 0.0.0.0:8000"]

