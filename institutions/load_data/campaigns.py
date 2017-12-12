from django.utils.translation import activate
from django.utils.text import slugify

from cms.models.titlemodels import Title

from campaigns.models import Campaign


def create_campaign(row, government_structure):

    campaign = []

    for cell in row[:7]:
        value = cell.value
        if value == 'Título (EN)':
            return
        campaign.append(value)

    if campaign[0] is None:
        return

    external_url = campaign[4]

    data = {
        'title': campaign[1],
        'description': campaign[2],
        'external_url': external_url,
    }

    if external_url.startswith('http://www.gob.cl'):
        del data['external_url']

    activate('es')

    campaign_obj = Campaign.objects.create(**data)

    activate('en')

    campaign_obj = Campaign.objects.get(pk=campaign_obj.pk)

    title_en = campaign[0]
    campaign_obj.title = title_en
    campaign_obj.save()

    if campaign_obj.page:
        Title.objects.create(
            title=title_en,
            page=campaign_obj.page,
            language='en',
            slug=slugify(title_en),
            published=True,
        )
