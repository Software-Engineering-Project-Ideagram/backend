echo "--> Starting web process"
echo "--> Waiting for Postgrsql to start"
bash ./scripts/wait-for-it.sh postgres:5432

echo "--> Migrating the database"
python manage.py migrate

echo "--> Collecting static files"
python manage.py collectstatic --no-input --clear
echo "--> Starting gunicorn"


python -m gunicorn config.wsgi:application -b 0.0.0.0:8000
