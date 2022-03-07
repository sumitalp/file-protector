release: python manage.py migrate

web: gunicorn file_protector.asgi --bind 0.0.0.0:8000 --chdir=/app -k uvicorn.workers.UvicornWorker