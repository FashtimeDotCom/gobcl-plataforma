from django_cron import CronJobBase, Schedule

from .models import ChileAtiendeFile


class GetAnalyticData(CronJobBase):
    RUN_AT_TIMES = ['03:00']

    schedule = Schedule(
        run_at_times=RUN_AT_TIMES,
    )
    code = 'services.cron.GetAnalyticData'

    def do(self):
        ChileAtiendeFile.update_visits()
