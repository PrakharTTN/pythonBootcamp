import boto3
import os

# s3 = boto3.resource('s3')
# for i in s3.buckets.all():
#     print(i.name)

# with open('new.jpg', 'rb') as data:
#     try:
#         s3.Bucket('ttn-bucket-prakhar').put_object(Key='new.jpg', Body=data)
#     except:
#         print("file not uploaded+ ")
# import boto3


def list_all_buckets(resource):
    for i in resource.buckets.all():
        print(i.name)


def create_bucket(resource, bucket_name):

    try:
        resource.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "ap-south-1"},
        )
        print(f"Bucket {bucket_name} created successfully.")

    except Exception as e:
        print(f"Error creating: {e}")


def delete_bucket(resource, bucket_name):

    try:
        bucket = resource.Bucket(bucket_name)
        bucket.objects.all().delete()
        bucket.delete()
        print(f"Bucket {bucket_name} deleted successfully.")

    except Exception as e:
        print(f"Error in deleteing the bucket {bucket_name}: {e}")


def add_file_to_bucket(file_path, resource, bucket_name):
    file_name = file_path.split("/", -1)[-1]
    try:
        # resource.upload_file(file_path, bucket_name, file_name) --> using client
        # resource.Bucket(bucket_name).put_object(Key=file_name, Body=file_name) --> another low-level way to upload
        resource.Bucket(bucket_name).upload_file(file_path, file_name)
        print("file uploaded sucessfully")
    except Exception as e:
        print(f"error in uploading {e}")


def download_bucket_file(resource, bucket_name, file_name):
    try:
        download_dir = os.path.join(os.getcwd(), "media")
        download_path = os.path.join(download_dir, file_name)
        resource.Bucket(bucket_name).download_file(file_name, download_path)
        print(f"File '{file_name}' downloaded successfully to '{download_path}'.")
    except Exception as e:
        print(f"Error in download {file_name} from bucket {bucket_name}: {e}")


def delete_bucket_file(resource, bucket_name, file_name):
    try:
        resource.Object(bucket_name, file_name).delete()
        print(f"File {file_name} deleted successfully.")
    except Exception as e:
        print(f"Error occurred: {e}")


def main():
    s3 = boto3.resource("s3")
    file_dir = "/home/prakhar/Desktop/Bootcamp/Python/Week_7_AWS/new.jpg"
    bucket_name = "new-boto-bocket"
    create_bucket(s3, bucket_name)
    list_all_buckets(s3)
    add_file_to_bucket(file_dir, s3, bucket_name)
    download_bucket_file(s3, bucket_name, "new.jpg")
    delete_bucket_file(s3, bucket_name, "new.jpg")
    delete_bucket(s3, bucket_name)


if __name__ == "__main__":
    main()

# ec2 = boto3.resource('ec2')

# instance = ec2.create_instances(
#     ImageId='ami-0e35ddab05955cf57',
#     MinCount=1,
#     MaxCount=1,
#     InstanceType='t2.micro',
#     KeyName='NewKeyPair',
#     SecurityGroupIds=['sg-xxxxxxxx'],
#     SubnetId='subnet-xxxxxxxx',
#     TagSpecifications=[{
#         'ResourceType': 'instance',
#         'Tags': [{
#             'Key': 'Name',
#             'Value': 'MyFirstEC2Instance'
#         }]
#     }]
# )

# print(f'EC2 Instance created with ID: {instance[0].id}')
