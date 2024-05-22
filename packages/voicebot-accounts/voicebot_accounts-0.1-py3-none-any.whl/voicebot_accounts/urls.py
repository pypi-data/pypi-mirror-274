from django.urls import path

from . import views


urlpatterns = [
    path('register', views.registration_view, name='register'),
    path('login', views.login_view, name='login'),
    path('home', views.home_view, name='home'),
    path('google_auth', views.google_auth, name='google_auth'),
    path('google/callback', views.google_callback, name='google_callback'),
    path('invoke_call/', views.invoke_call, name='invoke_call'),
    path('update_incoming_calls/<int:agent_id>/', views.update_incoming_calls, name='update_incoming_calls'),

    ### API Handlers
    path('handle_webhook/', views.handle_webhook, name='handle_webhook'),
    path('check_calendar/<int:connector_id>/', views.check_calendar, name='check_calendar'),

    
    path('manage_phonenumber/', views.manage_phonenumber, name='manage_phonenumber'),
    path('manage-connectors/', views.manage_connectors, name='manage_connectors'),
    path('add-connector/', views.add_connector, name='add_connector'),
    path('manage_agents/', views.manage_agents, name='manage_agents'),
    path('get_agent_details/<int:agent_id>/', views.get_agent_details, name='get_agent_details'),
    path('delete_agent/<int:agent_id>/', views.delete_agent, name='delete_agent'),
    path('logout/', views.logout_view, name='logout')

]