# # AWS returns EC2 instance data in a dictionary this is a simulation of one 
# ec2_instance = {"InstanceID": "i-1234567890abcdef0", "InstanceType": "t2.micro", "State": "running", "Region": "ap_northeast-1"}

# print(ec2_instance["InstanceID"])
# print(ec2_instance["State"])


# instances = [{"instanceid": "i-1234567890abcdef0", "state": "running"}, {"instanceid": "i-1234567890abcdef1", "state": "stopped"}, {"instanceid": "i-1234567890abcdef2", "state": "running"}]

# for instance in instances:
#     if instance["state"] == "running":
#         print(instance["instanceid"])


# #mutate a dictionary
# ec2_instance["LaunchTime"] = "2024-06-01T12:00:00Z"
# ec2_instance["State"] = "stopped"
# print(ec2_instance)

# #nested dictionaries 
# aws_response = {"Instance": {"instanceid": "i-1234567890abcdef0", "state": {"code": 16, "name": "running"}, "Tags": [{"Key": "Name", "Value": "MyInstance"}, {"Key": "Environment", "Value": "Production"}]}}

# print(aws_response["Instance"]["instanceid"])
# print(aws_response["Instance"]["state"]["name"])
# for tag in aws_response["Instance"]["Tags"]:
#     print(tag["Key"], ":", tag["Value"])


# consolidation block for day 1 
s3_bucket = {"BucketName": "my-bucket", "CreationDate": "2024-06-01T12:00:00Z", "Region": "us-west-2", "accesslevel": "private"}
print(s3_bucket["BucketName"], s3_bucket["CreationDate"])

s3_bucket["versioningEnabled"] = True
print(s3_bucket)

list_s3_buckets = [{"BucketName": "my-bucket-1", "CreationDate": "2024-06-01T12:00:00Z", "accesslevel": "private"}, {"BucketName": "my-bucket-2", "CreationDate": "2024-06-02T12:00:00Z", "accesslevel": "public"}, {"BucketName": "my-bucket-3", "CreationDate": "2024-06-03T12:00:00Z", "accesslevel": "private"}]
for i in list_s3_buckets:
    if i["accesslevel"] == "public":
        print(i["BucketName"])
