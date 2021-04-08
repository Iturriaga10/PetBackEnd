FROM python:3.9.4-slim-buster

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

# ENV FLASK_APP main.py
# ENV FLASK_ENV development
# ENV FLASK_RUN_PORT 5000
# ENV FLASK_RUN_HOST 0.0.0.0

CMD ["flask", "run"]
