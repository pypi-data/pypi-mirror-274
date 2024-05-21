# Lund Process Flow Modules

A Python library for converting office files to PDF using the iLovePDF API.

## Install the package

```python
pip install DjangoSharepointStorage
```

## Usage

Here's how to use DjangoSharepointStorage:

- You need to set following variables in your application's settings file:

```python
SHAREPOINT_APP_CLIENT_ID = "your_sharepoint_app_client_id"
SHAREPOINT_APP_CLIENT_SECRET = "your_sharepoint_app_client_secret"
SHAREPOINT_URL = "your_sharepoint_app_url"
SHAREPOINT_STATIC_DIR = "sharepoint_static_dir"
SHAREPOINT_MEDIA_DIR = "sharepoint_media_dir"
```
- Then, you need to assign the DjangoSharepointStorage as your application's storage backend:

```python
DEFAULT_FILE_STORAGE = 'django_sharepoint_storage.SharePointCloudStorageUtils.Media'
STATICFILES_STORAGE = 'django_sharepoint_storage.SharePointCloudStorageUtils.Static'
```

This project is licensed under the terms of the MIT license
