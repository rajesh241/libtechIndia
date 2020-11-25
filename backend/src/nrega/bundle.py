import os
import requests
import datetime
import shutil
import boto3
import pandas as pd
from django.conf import settings


def create_bundle(instance, objs):
    save_to_s3 = True
    if instance.filename is not None:
      zip_file_name = f"/tmp/{instance.id}_{instance.filename}"
    else:
      zip_file_name = f"/tmp/{instance.id}"
    if ".zip" in zip_file_name:
        zip_file_name = zip_file_name.rstrip(".zip")
    download_dir = None
    report_urls = []
    for obj in objs:
        if ((instance.report_format == "csv") or (instance.report_format =="both")):
            report_urls.append(obj.report_url)
        if ((instance.report_format == "excel") or (instance.report_format =="both")):
            report_urls.append(obj.excel_url) 
    if download_dir is None:
        current_timestamp = str(datetime.datetime.now().timestamp())
        download_dir = f"/tmp/{current_timestamp}"
    if zip_file_name is None:
        zip_file_name = f"/tmp/{current_timestamp}"
    for url in report_urls:
        download_save_file(url, dest_folder=download_dir)
    shutil.make_archive(zip_file_name, 'zip', download_dir)
    if save_to_s3 == True:
        with open(f"{zip_file_name}.zip", "rb") as f:
            filedata = f.read()
        content_type = 'binary/octet-stream'
        filename = zip_file_name.split('/')[-1].replace(" ", "_")
        filename = f"temp_archives/{filename}.zip"
        file_url = upload_s3(filename, filedata, content_type=content_type)
        print(f"bundle url is {file_url}")
        return file_url
    else:
        return f"{zip_file_name}.zip"

def download_save_file(url, dest_folder=None):
    """This function will download file from internet and save it to
    destination folder"""
    if dest_folder is None:
        current_timestamp = str(ts = datetime.datetime.now().timestamp())
        dest_folder = f"/tmp/{current_timestamp}"
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print(f"saving to {os.path.abspath(file_path)}")
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))

def upload_s3(filename, data, bucket_name=None, content_type=None):
    """
    This function will upload to amazon S3, it can take data either as
    string or as data frame
       filename: filename along with file path where file needs tobe created
       for example abcd/efg/hij.csv
       data : content can be a string or pandas data frame
       bucket: Optional bucket name, in which file needs to be created else
       will default to the AWS_DATA_BUCKET
    """
    s3_instance = aws_init()
    if bucket_name is None:
        bucket_name = settings.AWS_DATA_BUCKET
    bucket = s3_instance.Bucket(bucket_name)
    if isinstance(data, pd.DataFrame):
        #If the data passed is a pandas dataframe
        data['lastUpdateDate'] = datetime.datetime.now().date()
        csv_buffer = StringIO()
        data.to_csv(csv_buffer, encoding='utf-8-sig', index=False)
        filedata = csv_buffer.getvalue()
        content_type = 'text/csv'
        put_object_s3(bucket, filename, filedata, content_type)
        excelfilename = filename.rstrip('csv')+"xlsx"
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter',  options={'strings_to_urls': False})
        data.to_excel(writer, index=False)
        writer.save()
        filedata = output.getvalue()
        content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        put_object_s3(bucket, excelfilename, filedata, content_type)
    else:
        if content_type is None:
            content_type = 'text/html'
        filedata = data
        put_object_s3(bucket, filename, filedata, content_type)

    report_url = f"https://{bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{filename}"

    return report_url

def aws_init(use_env="1"):
    """Initializes the AWS bucket. It can either pick up AWS credentials from
    the environment variables or it can pick up from the profile in the .aws
    directory location in HOME Directory"""
    aws_access_key_id = settings.AWS_ACCESS_KEY
    aws_secret_access_key = settings.AWS_SECRET_KEY
    region = settings.AWS_REGION 
    boto3.setup_default_session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region
        )

    s3_instance = boto3.resource('s3', region_name=settings.AWS_REGION)
    return s3_instance

def put_object_s3(bucket, filename, filedata, content_type):
    """Putting object in amazon S3"""
    bucket.put_object(
        Body=filedata,
        Key=filename,
        ContentType=content_type,
        ACL='public-read'
        )


