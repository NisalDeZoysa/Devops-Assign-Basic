import boto3
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize EC2 client
ec2_client = boto3.client("ec2", region_name="us-east-1")


def stop_instances(instance_ids):
    """
    Stop EC2 instances with the provided instance IDs.
    """
    try:
        response = ec2_client.stop_instances(InstanceIds=instance_ids)
        logger.info("Instances stopped successfully.")
        return response
    except Exception as e:
        logger.error(f"Error stopping instances: {e}")
        return None


def get_all_instances():
    """
    Retrieve all running and terminated EC2 instances.
    """
    try:
        response = ec2_client.describe_instances(
            Filters=[
                {"Name": "instance-state-name", "Values": ["running", "terminated"]}
            ]
        )
        instances = []
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                instance_id = instance["InstanceId"]
                instance_type = instance["InstanceType"]
                instance_state = instance["State"]["Name"]

                instances.append(
                    {
                        "InstanceID": instance_id,
                        "InstanceType": instance_type,
                        "InstanceState": instance_state,
                    }
                )
        return instances
    except Exception as e:
        logger.error(f"Error retrieving instances: {e}")
        return []


def disable_running_instances():
    """
    Disable running instances.
    """
    instances = get_all_instances()
    instance_ids = [instance["InstanceID"] for instance in instances]
    if instance_ids:
        response = stop_instances(instance_ids)
        return response
    else:
        logger.info("No running instances found.")
        return None


def main():
    """
    Main function to list and disable instances.
    """
    logger.info("==================== Your Instances =====================")
    instances = get_all_instances()
    for instance in instances:
        logger.info(f"Instance ID: {instance['InstanceID']}")
        logger.info(f"Instance Type: {instance['InstanceType']}")
        logger.info(f"Instance State: {instance['InstanceState']}")
        logger.info("-" * 50)
    if not instances:
        logger.info("No instances found")
        return
    logger.info("==================== Disabling Instances =====================")
    response = disable_running_instances()
    if response:
        logger.info(response)


if __name__ == "__main__":
    main()
