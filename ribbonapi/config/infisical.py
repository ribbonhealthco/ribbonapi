
from environs import Env

from infisical_client import ClientSettings, InfisicalClient, GetSecretOptions, AuthenticationOptions, UniversalAuthMethod

env = Env()
env.read_env()

inf_client = InfisicalClient(ClientSettings(
    auth=AuthenticationOptions(
      universal_auth=UniversalAuthMethod(
        client_id=env.str('INFISICAL_CLIENT_ID'),
        client_secret=env.str('INFISICAL_CLIENT_SECRET'),
      )
    )
))

inf_env = env.str('INFISICAL_ENV')
inf_project_id = env.str('INFISICAL_PROJECT_ID')

def inf_secret(key: str, env: str=inf_env, project_id: str=inf_project_id) -> str:
    secret = inf_client.getSecret(options=GetSecretOptions(
       environment=env,
       project_id=project_id,
       secret_name=key
    ))

    return secret.secret_value
