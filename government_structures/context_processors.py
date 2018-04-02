def add_government_structure_to_context(request):
    """ Includes the current government_structure in the context """

    try:
        government_structure = request.government_structure
    except:
        return {}

    context = {
        'government_structure': government_structure,
    }

    return context
