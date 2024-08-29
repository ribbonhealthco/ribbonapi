
from config.infisical import inf_secret

EMAIL_API_TOKEN = inf_secret('EMAIL_API_TOKEN', default='')
EMAIL_SENDER_NAME = inf_secret('EMAIL_SENDER_NAME', default='')
EMAIL_SENDER_ADDRESS = inf_secret('EMAIL_SENDER_ADDRESS', default='')

SMTP_HOST = inf_secret('EMAIL_HOST')
SMTP_PORT = inf_secret('EMAIL_PORT')
SMTP_USER = inf_secret('EMAIL_HOST_USER')
SMTP_PASSWORD = inf_secret('EMAIL_HOST_PASSWORD')
SMTP_FROM_EMAIL = inf_secret('EMAIL_SENDER_ADDRESS')
