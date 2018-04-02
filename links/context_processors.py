# models
from .models import FooterLink


def footer_links(request):
    """
    Includes the footer links by
    structure government in the context
    """

    try:
        government_structure = request.government_structure
    except:
        return {}

    context = {
        'footer_links': FooterLink.objects.by_government_structure(
            government_structure
        )
    }

    return context
