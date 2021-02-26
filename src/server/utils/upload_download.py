from os import name, path
from google.cloud.storage import Blob
from google.cloud import storage


client = storage.Client(project="dsfsi-232208")
bucket = client.get_bucket("maskhane-web-test")
encryption_key = "c7f32af42e45e85b9848a6a14dd2a8f6"
 
# blob = Blob("secure-data", bucket, encryption_key=encryption_key)
blob = Blob("secure-data", bucket)



# Download
# blob.upload_from_string("my secret message.")
# with open("/tmp/my-secure-file", "wb") as file_obj:
#     client.download_to_file(blob, file_obj)

if __name__ == "__main__":
    path_to_file_for_upload = "../../data/external/available_models.tsv"
    # if (path.exists(path_to_file_for_upload)):
    #     # Upload
    #     with open(path_to_file_for_upload, "rb") as my_file:
    #         print("yes")
    #         blob.upload_from_file(my_file)

    where_to_download = "../../data/"
    with open(where_to_download, "wb") as file_obj:
        client.download_to_file(blob, file_obj)