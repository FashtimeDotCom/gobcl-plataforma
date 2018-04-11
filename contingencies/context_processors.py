from .models import Contingency


def get_contingencies(request):
    """ Includes the current government_structure in the context """

    contingencies = Contingency.objects.active().prefetch_related(
        'events',
        'informations',
    )[:3]

    context = {
        'contingencies': contingencies,
        'exists_contingency': contingencies.exists(),
    }

    return context
