# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from ipware.ip import get_real_ip
from django.shortcuts import render_to_response
from django.template import RequestContext

def trust(request):
  x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
  if x_forwarded_for:
    ip = x_forwarded_for.split(',')[0]
  else:
    ip = request.META.get('REMOTE_ADDR')
  userAgent = request.META.get('HTTP_USER_AGENT')
  meta = request.META
  with open("/home/mehltret/Desktop/test.txt", mode = "wt") as testFile:
    testFile.write("%s + %s\n%s" % (str(ip), userAgent, str(meta)))
  testFile.close() 
