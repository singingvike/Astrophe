import boto3
import io
import zipfile
import mimetypes

s3 = boto3.resource('s3')

website_bucket = s3.Bucket('website.astropheenterprises.com')
websitebuild_bucket = s3.Bucket('websitebuild.astropheenterprises.com')

website_zip = io.BytesIO()
websitebuild_bucket.download_fileobj('websitebuild.zip', website_zip)

with zipfile.ZipFile(website_zip) as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm)
        website_bucket.upload_fileobj(obj, nm, ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
        website_bucket.Object(nm).Acl().put(ACL='public-read')
