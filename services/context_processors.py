from .models import ChileAtiendeFile


def get_chile_atiende_files(request):

    context = {
        'chile_atiende_files': ChileAtiendeFile.objects.all()[:6]
    }

    return context
