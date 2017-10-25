# models
from .models import FooterLink


def footer_links(request):
    context = {
        'footer_links': FooterLink.objects.by_government_structure(
            request.government_structure
        )
    }

    return context
