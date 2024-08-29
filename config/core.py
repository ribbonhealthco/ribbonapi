
from .infisical import inf_secret

# access_key is used as an authentication method for low-risk, misc endpoints that still
# require some form of authentication to prevent misuse of public APIs
# the key is simply similar to a password that can be used that endpoint
# the key is used here: misc.views.SendEmailView
ACCESS_KEY = inf_secret('ACCESS_KEY')
