from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View
import json
from models import Person, Token
from django.contrib.auth.hashers import *
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from refdu.settings import FACEBOOK_SECRET, SECRET_KEY
import requests, jwt
from urlparse import parse_qs, parse_qsl
from datetime import datetime


def json_response(response_dict, status=200):
    response = HttpResponse(json.dumps(response_dict), content_type="application/json", status=status)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

def parse_token(req):
    print '------------parse token-----------'
    print req.headers
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, SECRET_KEY)

def token_required(func):
    def inner(request, *args, **kwargs):
        if request.method == 'OPTIONS':
            return func(request, *args, **kwargs)
        #print request.META.get('HTTP_AUTHORIZATION', None)
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)
        if auth_header is not None:
            tokens = auth_header.split(' ')
            print tokens
            if len(tokens) == 2 and tokens[0] == 'Bearer':
                token = tokens[1]
                print '-------------'
                print token
                try:
                    request.token = Token.objects.get(token=token)
                    payload = parse_token(request)
                    if datetime.fromtimestamp(payload['exp']) < datetime.now():
                        return json_response({
                        'error': 'Token Expired'
                        }, status=401)
                    return func(request, *args, **kwargs)
                except Token.DoesNotExist:
                    return json_response({
                        'error': 'Token not found'
                    }, status=401)
        return json_response({
            'error': 'Invalid Header'
        }, status=401)

    return inner
# gettering information of facebook account


class UserData(View):
    def get(self, request):
        print request.body
        return HttpResponse('method not allowed')

    def post(self,request):
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            token_pk_field = Token.objects.get(token= body['token']).values()
            print token_pk_field
            return HttpResponse('method not allowed')
        except Exception as e:
            return HttpResponse('bad token')

def register(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        email = body['email']
        password = body['password']
        account_type = body['account_type']

        if email is not None and password is not None and account_type is not None:
            try:
                if not body['password_change']:
                    obj = Person(email= email, password= make_password(password),role= account_type)
                    obj.save()
                elif body['password_change']:
                    rs = Person.objects.filter(email = email)
                    if rs:
                        obj = Person.objects.get(email = email)
                        obj.password = make_password(password)
                        obj.save()
                    else:
                        obj = Person(email= email, password= make_password(password),role= account_type)
                        obj.save()

            except IntegrityError:
                return json_response({
                    'error': 'User already exists'
                }, status=400)
            token = Token.objects.create(user=obj)
            return json_response({
                'token': token.token,
                'useremail': obj.email,
                'role': obj.role
            })
        else:
            return json_response({
                'error': 'Invalid Data'
            }, status=400)
    elif request.method == 'OPTIONS':
        return json_response({})
    else:
        return json_response({
            'error': 'Invalid Method'
        }, status=405)




@csrf_exempt
def login(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        email = body['email']
        password = body['password']

        if email is not None and password is not None:
            person_obj = Person.objects.filter(email = body['email'])
                #
            from django.core import serializers
            data = json.loads(serializers.serialize('json',person_obj,
                                                    fields=('email','password', 'role', 'id')))

            if person_obj is not None:
                if check_password(password, data[0]['fields']['password']):
                    token, created = Token.objects.get_or_create(user=person_obj)
                    return json_response({
                        'token': token.token,
                        'email': data[0]['fields']['email'],
                        'role': data[0]['fields']['role']
                    })
                else:
                    return json_response({
                        'error': 'Invalid Username/Password'
                    }, status=400)
            else:
                return json_response({
                    'error': 'Invalid User'
                }, status=400)


        else:
            return json_response({
                'error': 'Invalid Data'
            }, status=400)

    elif request.method == 'OPTIONS':
        return json_response({})
    else:
        return json_response({
            'error': 'Invalid Method'
        }, status=405)


@csrf_exempt
@token_required
def logout(request):
    if request.method == 'POST':
        request.token.delete()
        return json_response({
            'status': 'success'
        })
    elif request.method == 'OPTIONS':
        return json_response({})
    else:
        return json_response({
            'error': 'Invalid Method'
        }, status=405)

@token_required
def testing_on_token(request):
    print 'this is now old better then the gaminsdf'
    return HttpResponse('so this token workking is corect')