RUN export FLASK_APP=main.py
RUN export FLASK_ENV=development
RUN export FLASK_RUN_PORT=5000
RUN export FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]
