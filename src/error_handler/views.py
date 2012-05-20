#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

__author__ = "Caoilte Guiry"

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _

def csrf_failure(request, reason=""):
    """View to handle csrf failures."""
    resolution = "" # this will store suggestions to solve the problem
    if "cookie" in reason:
        resolution = _("Do you have cookies enabled?")
    
    return render_to_response("403.html", locals(),  context_instance=RequestContext(request))

