from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Connectors)
admin.site.register(ConnectorToken)
admin.site.register(Agents)
admin.site.register(CallLogs)
admin.site.register(PhoneNumber)