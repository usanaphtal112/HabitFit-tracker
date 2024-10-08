from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HabitFit_project.settings")

app = Celery("HabitFit_project")

# Using a string here means the worker will not have to
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))


app.conf.beat_schedule = {
    "generate-weekly-reports": {
        "task": "fittracker.tasks.generate_weekly_report_for_all_users",
        "schedule": crontab(hour=0, minute=0, day_of_week="mon"),
        # "schedule": crontab(minute="*/1"),  # Generate report every minute
    },
}
