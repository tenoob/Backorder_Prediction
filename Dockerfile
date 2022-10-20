FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirement.txt
EXPOSE $PORT
CMD gunicorn --worker=1 --bind 0.0.0.0:$PORT app:app
