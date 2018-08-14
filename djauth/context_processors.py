from django.conf import settings


def global_settings(request):
    # return any necessary values
    return {
        'GOOGLE_MAP_API_KEY': settings.GOOGLE_MAP_API_KEY,
        'APP_NAME': settings.APP_NAME,

    }