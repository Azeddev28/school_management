import os


def setup_environment():
    environment = os.environ.get('APP_ENVIRONMENT', 'local')
    environment_supported = ['production', 'local']
    if environment not in environment_supported:
        raise Exception(
            'Please set environment variable APP_ENV from %s' % environment_supported)

    settings_mapping = {
        'production': 'config.settings.production',
        'local': 'config.settings.local',
    }
    os.environ['DJANGO_SETTINGS_MODULE'] = settings_mapping[environment]
