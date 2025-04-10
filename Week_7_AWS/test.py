import boto3

s3 = boto3.resource('s3')
for i in s3.buckets.all():
    print(i.name)

with open('new.jpg', 'rb') as data:
    try:
        s3.Bucket('ttn-bucket-prakhar').put_object(Key='new.jpg', Body=data)
    except:
        print("file not uploaded+ ")








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