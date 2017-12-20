# -*- coding: utf-8 -*-
from django.utils.deprecation import MiddlewareMixin


class FontSizeMiddleware(MiddlewareMixin):
    """
    Checks and sets a user's fontsize
    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated():
            if not hasattr(request.user, 'font_size'):
                if not request.session.get('font_size'):
                    request.session['font_size'] = '16px'
                request.user.font_size = request.session['font_size']
