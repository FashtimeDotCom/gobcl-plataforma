from django_cron import CronJobBase, Schedule

from .models import Campaign


class UpdateCampaignsElasticsearchDocuments(CronJobBase):
    """
    Indexes campaigns if they're now active, and deindexes them if they're now
    inactive.
    """
    RUN_AT_TIMES = ['03:00']

    schedule = Schedule(
        run_at_times=RUN_AT_TIMES,
    )
    code = 'campaigns.cron.UpdateCampaignsElasticsearchDocuments'

    def do(self):
        Campaign.objects.update_elasticsearch_documents()
