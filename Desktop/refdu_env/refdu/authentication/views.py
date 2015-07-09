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
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives, send_mail

def json_response(response_dict, status=200):
    response = HttpResponse(json.dumps(response_dict), content_type="application/json", status=status)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

def parse_token(token):
    options = { 'verify_exp': False }
    return jwt.decode(str(token), SECRET_KEY, options=options)

def token_required(func):
    def inner(request, *args, **kwargs):
        if request.method == 'OPTIONS':
            return func(request, *args, **kwargs)
        print request.META
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)
        print '-----------auth header-----------'
        print auth_header
        if auth_header is not None:
            tokens = auth_header.split(' ')
            print '-------tokens------'
            print tokens
            if len(tokens) == 2 and tokens[0] == 'Bearer':
                token = tokens[1]
            elif len(tokens)==1:
                token = tokens[0]
            else:
                return json_response({
                    'error': 'Token not found'
                }, status=401)
            try:
                request.token = Token.objects.get(token=token)
                print '-------request token--------'
                print request.token

                payload = parse_token(request.token)

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

class UserData(View):
    def get(self, request):
        print request.body
        return HttpResponse('method not allowed')

    def post(self,request):
        try:
            from django.db import connection
            cursor = connection.cursor()
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            query = 'select p.email, p.role,p.id, t.token from authentication_person p,authentication_token t where t.user_id = p.id and t.token ="'+body['token']+'";'
            cursor.execute(query)
            row = cursor.fetchone()
            person_obj = {
                "email": row[0],
                "role":  row[1],
                "id":    row[2],
                "token": row[3]
            }
            return HttpResponse(json.dumps(person_obj))
        except Exception as e:
            return HttpResponse('bad token')

def create_token(userid):
        payload = {
            'sub': str(userid),
            'iat': datetime.now(),
            'exp': datetime.now() + timedelta(seconds=50)
        }
        token = jwt.encode(payload, SECRET_KEY)
        return token.decode('unicode_escape')

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
                else:
                    return json_response({
                    'error': 'unable to process'
                }, status=400)


            except IntegrityError:
                return json_response({
                    'error': 'User already exists'
                }, status=400)

            token = Token.objects.create(user=obj)
            if not body['password_change']:
                send_activation_link(obj.id, obj.email, 'activate')
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
def send_activation_link(id=None, email=None, request_type=None):
    print '-------id--------', id, email
    token = create_token(id)
    subject = 'user activation information'
    content = 'please click ' \
              '<a href="http://127.0.0.1:8000/#/'+request_type+'/'+token+'">' \
              'here</a>' \
              'to activate your account'
    from_email = "refdu@gmail.com"
    to = email
    msg = EmailMultiAlternatives(subject,'user activation link', from_email, [to])
    msg.attach_alternative(content, "text/html")
    if msg.send():
        person_data = Person.objects.get(id=id)

        obj, created = Token.objects.get_or_create(user=person_data)
        print '--------token created----------'
        print obj, created
        

    else:
        return False



@csrf_exempt
def login(request):
    try:
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            email = body['email']
            password = body['password']

            if email is not None and password is not None:
                person_obj = Person.objects.get(email = body['email'])
                if person_obj is not None and not person_obj:
                    if check_password(password,  person_obj.password):
                        token, created = Token.objects.get_or_create(user=person_obj)
                        return json_response({
                            'token': token.token,
                            'email': person_obj.email,
                            'role': person_obj.role
                        })
                    else:
                        return json_response({
                            'error': 'Invalid Password'
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
    except Exception as e:
        print e
        return json_response({
                'error': 'account does not exits'
        }, status=405)

@token_required
def logout(request):
    if request.method == 'POST':
        print '--------request body---------'
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        token = body['token']
        delete_row = Token.objects.get(token = token)
        delete_row.delete()
        #print request.META.get('HTTP_AUTHORIZATION', None)
        #print request.token
        return json_response({
            'status': 'success'
        })
    elif request.method == 'OPTIONS':
        return json_response({})
    else:
        return json_response({
            'error': 'Invalid Method'
        }, status=405)

class Networkerror(RuntimeError):
   def __init__(self, arg):
      self.args = arg

@csrf_exempt
def activate_link(request):
    if request.method == 'POST':
        try:
            print '--------request body---------'
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            token = body['token']
            payload = parse_token(token)
            data = Person.objects.get(id=payload['sub'])

            if data.isActive == True:
                return json_response({
                'status': 'alredy activated'
                }, status=200)

            if datetime.fromtimestamp(payload['exp']) < datetime.now():
                send_activation_link(data.id, data.email, 'activate')
                return json_response({
                    'error': 'Signature has expired and new link send your email'+data.email
                }, status=401)
            #data = Person.objects.get(id=payload['sub'])
            if data.activate_token == token:
                data.isActive = True
                data.save()
                return json_response({
                    'status': 'activated successfully'
                }, status=200)

            return json_response({
                'error': 'token doesnot matched'
                }, status=401)

        except Exception as e:
            if str(e) == "Signature has expired":
                return json_response({
                    'error': 'Signature has expired'
                }, status=401)
            else:
                return json_response({
                'error': 'invalid token'
                }, status=401)

def send_forgot_link(request):
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        email = body['email']
        data = Person.objects.get(email=email)
        send_activation_link(data.id, data.email, 'activate_forgot')
        return json_response({
                    'status': 'the forgot password link send to this email id'+data.email
        }, status=200)

    except Exception as e:
        print e
        return json_response({
                    'error': 'no account found by this email'
        }, status=401)

def update_forgot_password(request):
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        password = body['password']
        token = body['token']
        payload = parse_token(token)
        print payload
        if payload:
            data = Token.objects.get(user_id=payload['sub'])
            print '----------------'
            print data.token
            print token
            rs = check_token(token, data, payload)
            print '---check token details--', rs
            if rs == 1:
                return json_response({
                        'error': 'the token did not match'
                }, status=401)
            if rs == 2:
                send_activation_link(data.id, data.email, 'activate_forgot')
                return json_response({
                        'error': 'token expired please check your mail new mail has been sent'
                }, status=401)
            if rs == 3:
                data.password = make_password(password)
                data.save()
                return json_response({
                        'status': 'password successfully updated'
                }, status=200)
    except Exception as e:
        print e
        return json_response({
                    'error': 'token mismatch'
        }, status=401)

def check_token(token, user_obj, payload):

    if user_obj.token != token:
        return 1    #token mismatch
    if datetime.fromtimestamp(payload['exp']) < datetime.now():
        return 2    #token expired
    return 3        # all is good
