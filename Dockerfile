FROM python:3.8-alpine
EXPOSE 80
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
ENTRYPOINT ["./docker-entrypoint.sh"]