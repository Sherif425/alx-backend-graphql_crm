


RONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
]

# Note: The CRONJOBS setting tells django-crontab to run the
# `log_crm_heartbeat` function every 5 minutes.
# Make sure to run the following command to register the cron job with your system:
# python manage.py crontab add
