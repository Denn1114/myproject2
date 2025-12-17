FROM python:3.11-alpine

# ----- системні залежності -----
RUN apk add --no-cache gcc musl-dev sqlite

# ----- робоча папка -----
WORKDIR /app

# ----- requirements -----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ----- код -----
COPY . .

# ----- папка для SQLite -----
RUN mkdir -p instance && chmod 777 instance

# ----- ENV (ПІД app.py) -----
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV SQLITE_DB=instance/shop.db
ENV SECRET_KEY=super-secret-key

EXPOSE 5000

# ----- запуск -----
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]