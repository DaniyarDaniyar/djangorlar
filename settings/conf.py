# Project modules
from decouple import config

#
#Env id
#
ENV_POSSIBLE-OPTIONS = (
    "local",
    "prod",
)
ENV_ID = config("DJANGORLAR_ENV_ID", cast=str)
SECRET_KEY = "django-insecure-&1=4@o8+8uj((o8!g973=@(n%334%3r*x(&n0-pc&#ja=er7%e"