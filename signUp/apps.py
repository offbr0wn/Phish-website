from django.apps import AppConfig


class SignupConfig(AppConfig):
    name = 'signUp'

    def ready(self):
        import signUp.signals
