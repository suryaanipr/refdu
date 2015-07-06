from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View
import json
from models import Person
from django.contrib.auth.hashers import *

class Register(View):
    def get(self, request):
        return HttpResponseBadRequest('method not allowed')

    def post(self, request):
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            if body['email'] and body['password'] and body['account_type']:
                print make_password(body['password'])
                obj = Person(email = body['email'], password= make_password(body['password']),
                                role = body['account_type'])
                obj.save()
                return HttpResponse(json.dumps({'status':200}))
            else:
                return HttpResponse(json.dumps({'status':200}))
        except Exception as e:
            print e
            return  HttpResponseBadRequest(json.dumps({'status':501}))