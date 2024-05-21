import platform
from django.core.files.storage import Storage
import os
from office365.sharepoint.files.file import File
from io import BytesIO
from django.conf import settings
from django.db import connection

from django_sharepoint_storage.SharePointClients import ctx, client_credentials
from django_sharepoint_storage.SharePointFile import SharePointFile

DB_NAME = connection.settings_dict['NAME']
class SharePointStorage(Storage):
    sharepoint_url = getattr(settings, 'SHAREPOINT_URL', 'sharepoint_url')
    client_id = getattr(settings, 'SHAREPOINT_APP_CLIENT_ID', 'client_id')
    client_secret = getattr(settings, 'SHAREPOINT_APP_CLIENT_SECRET', 'client_secret')

    def __init__(self, location='uploads', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location = location

    @classmethod
    @staticmethod
    def print_failure(retry_number, ex):
        Logger.logger_msg(f"{retry_number}: {ex}")

    def _open(self, name, mode='rb'):
        from django_sharepoint_storage.SharePointCloudStorageUtils import get_server_relative_path
        if mode in ['r', 'rb']:
            file_url = self.url(name)
            file = ctx.web.get_file_by_server_relative_path(get_server_relative_path(file_url)).execute_query_retry(max_retry=5, timeout_secs=5, failure_callback=SharePointStorage.print_failure)
            binary_file = file.open_binary(ctx, get_server_relative_path(file_url))
            bytesio_object = BytesIO(binary_file.content)
            return bytesio_object
        elif mode in ['w', 'wb']:
            return SharePointFile(name, mode, self)
        else:
            raise ValueError(f"Unsupported file mode: {mode}")

    def _save(self, name, content):
        # Here, name will have the format 'upload_to/filename.ext'
        folder_path = f"Shared Documents/{os.getenv('DEPLOYMENT_ENVIRONMENT', 'LOCAL')}-{os.getenv('K8S_NAMESPACE', 'ENV')}/{os.getenv('KEYCLOAK_INTERNAL_CLIENT_ID', 'Local')}/{os.getenv('INSTANCE_RESOURCE_IDENTIFIER', f'{platform.node()}/{DB_NAME}')}/{self.location}/{os.path.dirname(name)}"
        target_folder = ctx.web.ensure_folder_path(folder_path).get().select(["ServerRelativePath"]).execute_query_retry(max_retry=5, timeout_secs=5, failure_callback=SharePointStorage.print_failure)

        file_content = content.read()

        target_folder.upload_file(os.path.basename(name), file_content).execute_query_retry(max_retry=5, timeout_secs=5, failure_callback=SharePointStorage.print_failure)

        return name

    def delete(self, name):
        file = File.from_url(self.url(name)).with_credentials(client_credentials).execute_query_retry(max_retry=5, timeout_secs=5, failure_callback=SharePointStorage.print_failure)
        file.delete_object().execute_query_retry(max_retry=5, timeout_secs=5, failure_callback=SharePointStorage.print_failure)

    def exists(self, name):
        return False

    def url(self, name):
        # Use the dirname of name as your upload_to equivalent
        return f"{self.sharepoint_url}/Shared Documents/{os.getenv('DEPLOYMENT_ENVIRONMENT', 'LOCAL')}-{os.getenv('K8S_NAMESPACE', 'ENV')}/{os.getenv('KEYCLOAK_INTERNAL_CLIENT_ID', 'Local')}/{os.getenv('INSTANCE_RESOURCE_IDENTIFIER', f'{platform.node()}/{DB_NAME}')}/{self.location}/{name}"