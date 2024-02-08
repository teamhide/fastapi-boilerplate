#!/bin/bash
# Switch environment
source ./.venv/bin/activate

echo "--- Checking PYTHON PATH --- "

echo "Current path $(pwd)"

echo "--- Checking python ---"
which python

echo "--- Checking python version ---"
python --version

echo "--- Checking environment to run migration --- "
echo "--- Set env: $APP_ENV ---"
if [ "$APP_ENV" != "production" ]; then
  echo "Halo, we are running migration"
  #python3 manage.py makemigrations
  #python3 manage.py migrate
  #python3 manage.py db_seed_email_templates
  #python3 manage.py db_seed_notification_setting

fi

#service supervisor start celery:*

python -m debugpy --listen 0.0.0.0:5678 --wait-for-client main.py