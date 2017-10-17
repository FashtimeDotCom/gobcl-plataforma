def add_government_to_context(request):
    """ Includes the current government in the context """

    context = {
        'government': request.government,
    }

    return context
