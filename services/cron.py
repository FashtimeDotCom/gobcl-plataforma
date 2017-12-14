from django_cron import CronJobBase, Schedule

from .models import File


class GetAnalyticData(CronJobBase):
    RUN_AT_TIMES = ['03:00']

    schedule = Schedule(
        run_at_times=RUN_AT_TIMES,
    )
    code = 'services.cron.GetAnalyticData'

    def do(self):
        File.update_visits()
