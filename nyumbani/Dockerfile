FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV DEBUG 1
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin
RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

CMD python manage.py collectstatic --no-input -v 3
CMD python manage.py migrate
CMD gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 config.config.wsgi
