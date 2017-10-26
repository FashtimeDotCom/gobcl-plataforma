# models
from .models import FooterLink


def footer_links(request):
    """
    Includes the footer links by
    structure government in the context
    """

    context = {
        'footer_links': FooterLink.objects.by_government_structure(
            request.government_structure
        )
    }

    return context
