# -*- coding: utf-8 -*-


class FontSizeMiddleware(object):
    """
    Checks and sets a user's fontsize
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated():
            if not hasattr(request.user, 'font_size'):
                if not request.session.get('font_size'):
                    request.session['font_size'] = '16px'
                request.user.font_size = request.session['font_size']
