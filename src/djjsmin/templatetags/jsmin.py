# -*- coding: utf-8 -*-

import os.path

from django import template
from django.conf import settings

from djjsmin import utils

register = template.Library()

@register.tag
def javascripts(parser, token):
    return JavascriptsNode()

class JavascriptsNode(template.Node):
    
    def render(self, context):
        root = utils.get_root(settings)
        input_files, temp_files = utils.resolve_patterns(settings.JSMIN_INPUT, root)
        
        make_relative = lambda f: os.path.relpath(f, settings.MEDIA_ROOT)
        input_files = map(make_relative, input_files)
        temp_files = map(make_relative, temp_files)
        
        html = ""
        for f in input_files + temp_files:
            html += """<script src="%s%s" type="text/javascript" charset="utf-8"></script>\n""" % (settings.MEDIA_URL, f)
        
        return html
    


