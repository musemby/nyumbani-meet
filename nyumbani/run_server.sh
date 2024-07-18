python manage.py collectstatic --no-input -v 3
python manage.py migrate --no-input
gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 config.wsgi