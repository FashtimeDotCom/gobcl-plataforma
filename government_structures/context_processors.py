def add_government_structure_to_context(request):
    """ Includes the current government_structure in the context """

    context = {
        'government_structure': request.government_structure,
    }

    return context
