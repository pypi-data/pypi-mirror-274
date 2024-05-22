import os
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from rest_framework.decorators import api_view, action
from rest_framework.response import Response 
from rest_framework import status, views, viewsets
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .utils import *
import requests
import json
from django.contrib import messages
from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout

from .models import Agents, CallLogs, Connectors, ConnectorToken, PhoneNumber

from django.contrib.auth import get_user_model
User = get_user_model()

domain = "https://c8d309b8046253366ce8fb9bbeabebdd.serveo.net"

def registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('manage_connectors')  # Redirect to home page after login
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
        if request.user.is_authenticated:
            return redirect('manage_connectors')
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


def home_view(request):

    if request.user.is_authenticated:
        user = request.user
        file_name = request.user.token_name
        file_exist = False

        if os.path.exists(f"token/{file_name}"):
            file_exist = True

        return render(request, 'home.html', context={"user": user, "file_exist" : file_exist})
    else:
        return redirect("login")

@login_required
def manage_connectors(request):
    connectors = Connectors.objects.filter(user = request.user)
    return render(request, 'connector.html', {'connectors': connectors})

@login_required
def add_connector(request):
    if request.method == 'POST':
        connector_name = request.POST.get('connectorName')
        connecting_to = request.POST.get('connectingTo')
        
        # Additional validation can be added here

        connector = Connectors(
            connector_name=connector_name,
            connecting_to=connecting_to,
            token_email=request.user.email,
            user=request.user
        )
        connector.save()
        messages.success(request, 'Connector added successfully')
        request.session["connector_id"] = connector.id

        return redirect('google_auth')  # Replace with your desired redirect URL

    return render(request, 'manage_connectors.html')


@login_required
def get_agent_details(request, agent_id):
    try:
        agent = Agents.objects.get(pk=agent_id)
        # Prepare the agent data to be sent as JSON
        agent_data = {
            'agentName': agent.agent_name,
            'agentType': agent.agent_type,
            'prompt': agent.prompt,
            'connector': agent.connector_id,
            'first_sentence' : agent.first_sentence
        }
        return JsonResponse({'success': True, 'agentData': agent_data})
    except Agents.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Agent not found'}, status=404)

@login_required
def delete_agent(request, agent_id):
    try:
        agent = Agents.objects.get(pk=agent_id)
        agent.delete()
        agents = Agents.objects.filter(user=request.user)
        connectors = Connectors.objects.filter(user=request.user)
        return render(request, 'manage_agents.html', {'agents': agents, 'connectors': connectors})
    except Agents.DoesNotExist:
        return messages.error(request, 'Agent not found.')


@login_required
def manage_agents(request):
    if request.method == 'POST':
        agent_name = request.POST.get('agentName')
        agent_type = request.POST.get('agentType')
        prompt = request.POST.get('prompt')
        connector_id = request.POST.get('connector')
        first_sentence = request.POST.get('firstSentence')

        if request.POST.get('agentId') != "":

            print(request.POST.get('agentId'), flush=True)
            # If agentId is present, it's an edit operation
            agent_id = request.POST.get('agentId')
            agent = Agents.objects.get(pk=agent_id)
            agent.agent_name = agent_name
            agent.agent_type = agent_type
            agent.prompt = prompt
            agent.connector = Connectors.objects.get(id=connector_id)
            agent.first_sentence = first_sentence
            agent.user = request.user
            agent.save()
        else:
            # Otherwise, it's a new agent creation
            agent = Agents.objects.create(
                agent_name=agent_name,
                agent_type=agent_type,
                prompt=prompt,
                user = request.user,
                first_sentence = first_sentence,
                connector=Connectors.objects.get(id=connector_id)
            )

        agents = Agents.objects.filter(user=request.user)
        connectors = Connectors.objects.filter(user=request.user)
        return redirect('manage_agents')
        # return render(request, 'manage_agents.html', {'agents': agents, 'connectors': connectors})
    else:
        agents = Agents.objects.filter(user=request.user)
        connectors = Connectors.objects.filter(user=request.user)
        return render(request, 'manage_agents.html', {'agents': agents, 'connectors': connectors})


@login_required
def manage_phonenumber(request):
    phone_numbers = PhoneNumber.objects.filter(user = request.user)
    return render(request, 'phone_number.html', {'phone_numbers': phone_numbers})


def save_credentials_to_db(credentials):
    token_info = credentials.to_json()
    token_entry = ConnectorToken.objects.create(
        credentials = token_info
    )

    return token_entry

def google_callback(request):
    
    # Verify state token to prevent CSRF attacks
    state = request.session.get('oauth2_state')
    if state is None or state != request.GET.get('state'):
        return HttpResponseBadRequest('Invalid state token')

    SCOPES = [
        "openid",
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/userinfo.profile", 
        "https://www.googleapis.com/auth/userinfo.email"
        ]

    flow = Flow.from_client_secrets_file(
        "token/credentials.json", SCOPES, redirect_uri="https://localhost/api/google/callback")

    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    # Once tokens are obtained,
    #  you can use them as needed
    credentials = flow.credentials

    token_obj = save_credentials_to_db(credentials)

    r = requests.get(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            params={'access_token': credentials.token})
    user_email = r.json()["email"]

    connector_id = request.session.get('connector_id')
    connector = Connectors.objects.filter(id = connector_id)

    if connector:
        connector[0].token = token_obj
        connector[0].token_email = user_email
        connector[0].save()
    else:
        messages.error(request, f"An error occurred: Connector Creation UnSuccessfull")

    print(connector, flush=True)
    
    return redirect("manage_connectors")

def google_auth(request):

    SCOPES = [
        "openid",
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/userinfo.profile", 
        "https://www.googleapis.com/auth/userinfo.email"
        ]

    flow = Flow.from_client_secrets_file(
        "token/credentials.json", SCOPES, redirect_uri="https://localhost/api/google/callback")

    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true', prompt='select_account')
    
    # Store the state token in session for later verification
    request.session['oauth2_state'] = state

    return redirect(authorization_url)


def invoke_call(request):

    headers = {
        'Authorization': 'sk-j2fcbtj7ecq0mhzxh4decxfku64d9pg6j8c2x511dymrnnyx6ozyrvdym6hpnfe969'
    }

    if request.method == 'POST':
        phone_number = request.POST.get('phoneNumber')
        agent_id = request.POST.get('agentId')

    url = "https://api.bland.ai/v1/calls"

    SCOPES = [
        "openid",
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/userinfo.profile", 
        "https://www.googleapis.com/auth/userinfo.email"
        ]

    agent_obj = Agents.objects.get(id=agent_id)

    credentials = Credentials.from_authorized_user_info(json.loads(agent_obj.connector.token.credentials), SCOPES)

    events = get_event(credentials)
    print(phone_number, agent_id, flush=True)

    data ={
        "phone_number": phone_number,
        "task": agent_obj.prompt + " \n- Current Calendar {{current_calender_information}} ",
        "voice": "maya",
        "wait_for_greeting": False,
        "record": False,
        "local_dialing": False,
        "answered_by_enabled": True,
        "interruption_threshold": 100,
        "temperature": None,
        "transfer_phone_number": None,
        "first_sentence": agent_obj.first_sentence, #"Hey I'm Call Schedular for iCloudNow, How may I help you?",
        "analysis_schema": {
            "name": "string",
            "email" : "string",
            "wants_to_book_appointment": "boolean",
            "appointment_time": "YYYY-MM-DD HH:MM:SS",
            "schedule_reschedule_cancel" : "string",
            "meeting_id" : "string",
            "new_time_reschedule" : "YYYY-MM-DD HH:MM:SS",
        },
        "max_duration": "5",
        "model": "enhanced",
        "language": "eng",
        "start_time": None,
        "pronunciation_guide": [],
        "calendly_url": None,
        "webhook": domain + "/api/handle_webhook/",
        "request_data": [
            {
            "key": "current_calender_information",
            "value": json.dumps(events).replace('"',"'")
            }
        ]
    }

    resp = requests.post(url, json=data, headers=headers)
    print(resp.text)

    call_id = json.loads(resp.text)["call_id"]

    CallLogs.objects.create(
        call_id = call_id,
        connector = agent_obj.connector
    )


    if resp.status_code == 200:
        messages.success(request, f'Call Invoked to {phone_number}')
    else:
        messages.error(request, f'Error while invoking call to {phone_number}', resp.text)

    return redirect("manage_agents")

@api_view(["POST"])
def handle_webhook(request):

    data = request.data
    print(f"incoming call data {data}")
    call_id = data["call_id"]
    call_obj = CallLogs.objects.filter(
        call_id = call_id
    )[0]

    number = data["from"]

    num_obj = PhoneNumber.objects.get(number = number)

    if num_obj:
        agents = num_obj.agents_set.first()
        conn_obj = agents.connector


    elif call_obj:

        call_obj.analysis = data["analysis"]
        call_obj.save()

        conn_obj = call_obj.connector

    SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/userinfo.profile", 
    "https://www.googleapis.com/auth/userinfo.email"
    ]

    credentials = Credentials.from_authorized_user_info(json.loads(conn_obj.token.credentials), SCOPES)

    summary = data.get('summary', 'No summary available')
    print(summary)

    analysis = data["analysis"]
    if analysis["schedule_reschedule_cancel"] == "cancel":
        meeting_id = analysis["meeting_id"]
        cancel_event(meeting_id, credentials)

    elif analysis["schedule_reschedule_cancel"] == "schedule":
        try:
            name = analysis["name"]
            email = analysis["email"].replace(" ","")
        except:
            pass

        appointment_time_start = datetime.strptime(analysis["appointment_time"], "%Y-%m-%d %H:%M:%S")
        appointment_time_end = datetime.strptime(analysis["appointment_time"], "%Y-%m-%d %H:%M:%S") + timedelta(minutes=30)

        event = {
                "summary": "Meeting with "+ name,
                "location": "Virtual Meeting",
                "description": summary,
                "attendees" : [{"email" : email}],
                "start": {
                        "dateTime": appointment_time_start.strftime("%Y-%m-%dT%H:%M:%S"),
                        "timeZone": "Asia/Kolkata",
                },
                "end": {
                        "dateTime": appointment_time_end.strftime("%Y-%m-%dT%H:%M:%S"),
                    "timeZone": "Asia/Kolkata",
                },
                "reminders": {
                        "useDefault": True,
                }
            }
        schedule_event(event, credentials)
    elif analysis["schedule_reschedule_cancel"] == "reschedule":
        
        appointment_time_start = datetime.strptime(analysis["new_time_reschedule"], "%Y-%m-%d %H:%M:%S")
        appointment_time_end = datetime.strptime(analysis["new_time_reschedule"], "%Y-%m-%d %H:%M:%S") + timedelta(minutes=30)
        
        meeting_id = analysis["meeting_id"]
        new_end_time = appointment_time_end.strftime("%Y-%m-%dT%H:%M:%S")
        new_meeting_time = appointment_time_start.strftime("%Y-%m-%dT%H:%M:%S")

        reschedule_event(meeting_id, new_meeting_time, new_end_time, credentials)

    return JsonResponse({"resp":"Webhook received!"})


def update_incoming_calls(request, agent_id):

    agent_obj = Agents.objects.get(id=agent_id)
    connector_obj = agent_obj.connector
    phone_number = "+19106599096"

    data = {
            "prompt": agent_obj.prompt+"\n- Current Calendar {{current_calender_information}}",
            "voice": "Alexa",
            "pathway_id": None,
            "interruption_threshold": 50,
            "first_sentence": agent_obj.first_sentence,
            "max_duration": 30,
            "model": "enhanced",
            "temperature": None,
            "dynamic_data": [
                {
                "url": f"{domain}/check_calendar/{int(connector_obj.id)}/",
                "method": "GET",
                "body": [],
                "headers": [
                    {
                    "key": "Content-Type",
                    "value": "application/json"
                    }
                ],
                "query": [],
                "cache": True,
                "response_data": [
                    {
                    "name": "current_calender_information",
                    "data": "$.data",
                    "context": "Calendar Information"
                    }
                ]
                }
            ],
            "webhook": domain + "/api/handle_webhook/",
            }

    url = "https://api.bland.ai/v1/inbound/"+phone_number

    headers = {
        'Authorization': 'sk-j2fcbtj7ecq0mhzxh4decxfku64d9pg6j8c2x511dymrnnyx6ozyrvdym6hpnfe969'
    }

    resp = requests.post(url, json=data, headers=headers)

    return JsonResponse({"response": resp.text})


@api_view(["GET"])
def check_calendar(request, connector_id):

    conn_obj = Connectors.objects.get(id=connector_id)
    
    SCOPES = [
        "openid",
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/userinfo.profile", 
        "https://www.googleapis.com/auth/userinfo.email"
        ]

    credentials = Credentials.from_authorized_user_info(json.loads(conn_obj.token.credentials), SCOPES)
    data = get_event(credentials)

    return JsonResponse({"data" : data})
