import os


class S3Sync:
    # this method will sync and upload the folders like artifact and saved_model to s3 bucket
    # folder is thr path of the folder which you want to upload
    def sync_folder_to_s3(self, folder, aws_bucket_url):
        # uses aws cli to sync the folder to s3 bucket
        command = f"aws s3 sync {folder} {aws_bucket_url}"
        os.system(command)

    # this method will sync and download the folders like artifact and saved_model from s3 bucket
    # folder is thr path of the folder where you want to download the files
    def sync_folder_from_s3(self, folder, aws_bucker_url):
        # uses aws cli to sync the folder from s3 bucket
        command = f"aws s3 sync {aws_bucker_url} {folder}."
        os.system(command)
