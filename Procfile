release: python manage.py migrate

web: gunicorn file_protector.asgi --chdir=/app -k uvicorn.workers.UvicornWorker