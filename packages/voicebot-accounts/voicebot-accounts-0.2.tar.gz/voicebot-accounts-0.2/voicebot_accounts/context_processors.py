from django.conf import settings

def template_base(request):
    return {'TEMPLATE_BASE': settings.TEMPLATE_BASE}
