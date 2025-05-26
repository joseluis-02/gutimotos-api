# Boto3
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    location = 'static'  # Los archivos estáticos se guardarán en s3://<bucket>/static/
    default_acl = None
    file_overwrite = True

class MediaStorage(S3Boto3Storage):
    location = 'media'   # Los archivos multimedia se guardarán en s3://<bucket>/media/
    file_overwrite = False
    default_acl = None
    file_overwrite = True