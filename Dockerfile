FROM python:3.9.4-slim-buster

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["flask", "run"]
