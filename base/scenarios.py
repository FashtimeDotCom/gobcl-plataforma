from django.utils import timezone

from base.mockups import Mockup

from government_structures.models import GovernmentStructure


def create_government_structure(date=None):
    m = Mockup()
    if date is None:
        date = timezone.datetime.now()
    return m.create_government_structure(
        publication_date=date,
        current_government=True
    )


def create_ministry(date=None, quantity=10):
    m = Mockup()
    government_structures = GovernmentStructure.objects.filter(
        current_government=True)
    if government_structures.exists():
        government_structure = government_structures.first()
    else:
        government_structure = create_government_structure(date)

    for x in range(quantity):
        minister = m.create_public_servant(
            government_structure=government_structure,
        )
        m.create_ministry(
            minister=minister,
            government_structure=government_structure,
        )
