import boto3

def list_ec2(resource):
    try:
        allen = list(resource.instances.all())
        if allen:
            for instance in allen:
                print(f"Instance ID: {instance.id} | State: {instance.state['Name']}")
        else:
            print("No instances available")
    except Exception as e:
        print(f"Exception Occurred: {e}")

def start_ec2(resource, instance_id):
    try:
        instance=resource.instances(instance_id=instance_id)
        instance.start()
        print("Instance has been started")
    except Exception as e:
        print(f"Exception Occurred: {e}")

def stop_ec2(resource, instance_id):
    try:
        instance=resource.instances(instance_id=instance_id)
        instance.stop()
        print("Instance has been stopped")
    except Exception as e:
        print(f"Exception Occurred: {e}")


def main():
    ec2 = boto3.resource("ec2")
    list_ec2(ec2)


if __name__ == "__main__":
    main()
