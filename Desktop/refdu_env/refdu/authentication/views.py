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
                print (body['password'])
                obj = Person(email = body['email'], password= make_password(body['password']),
                                role = body['account_type'])
                obj.save()
                return HttpResponse(json.dumps({'status':200}))
            else:
                return HttpResponse(json.dumps({'status':401, 'error': 'missing credentials'}))
        except Exception as e:
            print e
            return  HttpResponse(json.dumps({'status':401, 'error': 'email alredy registered'}))

class Login(View):
    def get(self, request):
        return HttpResponseBadRequest('method not allowed')

    def post(self, request):
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)

            if body['email'] and body['password']:
                person_obj = Person.objects.filter(email = body['email'])
                #
                from django.core import serializers
                data = json.loads(serializers.serialize('json',person_obj,
                                                        fields=('email','password', 'role', 'id')))
                if check_password(body['password'], data[0]['fields']['password']):
                    return HttpResponse(json.dumps({'status':200, 'person': data}))
                else:
                    return HttpResponse(json.dumps({'status':401, 'error': 'wrong password'}))
            else:
                return HttpResponse(json.dumps({'status':401, 'error': 'missing credentials'}))
        except Exception as e:
            print e
            return  HttpResponse(json.dumps({'status':401, 'error': 'email is  not found'}))

