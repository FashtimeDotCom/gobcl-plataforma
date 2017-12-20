from .models import Contingency


def get_contingencies(request):
    """ Includes the current government_structure in the context """

    contingencies = Contingency.objects.active()

    context = {
        'contingency': contingencies.first(),
        'exists_contingency': contingencies.exists(),
    }

    return context
