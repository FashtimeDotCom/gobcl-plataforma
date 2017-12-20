from django_cron import CronJobBase, Schedule

from .models import ChileAtiendeFile

from .chile_atiende import charge_data


class ChargeChileAtiendeServiceFile(CronJobBase):
    RUN_AT_TIMES = ['03:00']

    schedule = Schedule(
        run_at_times=RUN_AT_TIMES,
    )
    code = 'services.cron.ChargeChileAtiendeServiceFile'

    def do(self):
        charge_data()
        ChileAtiendeFile.update_visits()
