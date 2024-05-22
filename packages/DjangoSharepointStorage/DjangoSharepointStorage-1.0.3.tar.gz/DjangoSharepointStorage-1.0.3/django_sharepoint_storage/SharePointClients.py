import os

from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext

from django.conf import settings

client_credentials = ClientCredential(getattr(settings, 'SHAREPOINT_APP_CLIENT_ID', 'client_id'),
                                      getattr(settings, 'SHAREPOINT_APP_CLIENT_SECRET', 'client_secret'))
ctx = ClientContext(getattr(settings, 'SHAREPOINT_URL', 'sharepoint_url')).with_credentials(client_credentials)