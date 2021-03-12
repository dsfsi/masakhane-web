from google.cloud import storage
from google.oauth2 import service_account
import pathlib, io, ipdb

# credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

client = storage.Client(
    project="dsfsi-232208",
    # credentials=credentials
)


from google.cloud import storage
from zipfile import ZipFile, ZipInfo

def upload():
    source_dir = pathlib.Path("../../models/joeynmt/en-lua/")

    archive = io.BytesIO()
    with ZipFile(archive, 'w') as zip_archive:
        for file_path in source_dir.iterdir():
            # ipdb.set_trace()
            with open(file_path, 'r') as file:
                zip_entry_name = file_path.name
                zip_file = ZipInfo(zip_entry_name)
                zip_archive.writestr(zip_file, file.read())
            
    ipdb.set_trace()
    archive.seek(0)

    object_name = 'super-important-data-v1'
    bucket = client.bucket("maskhane-web-test")

    blob = storage.Blob(object_name, bucket)
    blob.upload_from_file(archive, content_type='application/zip')

upload()