Celery Setup for CRM Reports
This document outlines the steps to set up and run Celery and Celery Beat to generate weekly CRM reports.

1. Install Redis
Celery uses Redis as a message broker. You need to have it installed and running.

2. Install Python Dependencies
Make sure to install the required Python packages from the requirements.txt file.

pip install -r requirements.txt

3. Run Migrations
The django-celery-beat package requires database tables. Run migrations to create them.

python manage.py migrate

4. Start Celery Worker
The Celery worker processes the tasks. Start it by running the following command from your project's root directory:

celery -A crm worker -l info

5. Start Celery Beat
Celery Beat is the scheduler. It will trigger the generate_crm_report task based on the schedule defined in settings.py. Run this command in a separate terminal:

celery -A crm beat -l info

6. Verify Logs
After the scheduled time (Monday at 6:00 AM), check the log file to confirm the report was generated.

cat /tmp/crm_report_log.txt
