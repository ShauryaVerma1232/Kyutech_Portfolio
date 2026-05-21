# #sets, tuples and comprehensions for boto3 pipelines processing hundereds of aws resources
# # sets are unordered collections of unique elements
# sg_1_ports = {22, 80, 443, 3306}
# sg_2_ports = {80, 8080, 443, 3306, 5432}
# sg3_ports = {22, 443, 5432}

# #all unique ports exposed across entire infrastructure
# all_exposed_ports = sg_1_ports | sg_2_ports | sg3_ports
# print("all exposed ports:", all_exposed_ports)

# #ports open in all 3 groups 
# open_ports = sg_1_ports & sg_2_ports & sg3_ports
# print("ports open in all 3 groups:", open_ports)

# #ports only in sg1 
# unique_sg1_ports = sg_1_ports - sg_2_ports - sg3_ports
# print("ports only in sg1:", unique_sg1_ports)

# tuples for fixed configurations like AWS regions or instance types
regions = [ ("ap-northeast-1", "Asia Pacific (Tokyo)"), ("us-west-2", "US West (Oregon)"), ("eu-west-1", "EU (Ireland)") ]
for region, az in regions:
    print(f"Region: {region}, Availability Zone: {az}")

regions[0] = ("us-west-1", "us-west-1a")


first_region = ("us-west-1", "us-east-1")
# first_region[0] = "east-asia-1" gives out error due to immutable anture of tuples 


#list and dict comprehensions for processing AWS resource data
instances = [{"instanceid": "i-1234567890abcdef0", "state": "running", "type": "t2.micro"}, {"instanceid": "i-1234567890abcdef1", "state": "stopped", "type": "t2.small"}, {"instanceid": "i-1234567890abcdef2", "state": "running", "type": "t2.medium"}]

#old way
running = []
for i in instances:
    if i["state"] == "running":
        running.append(i["instanceid"])

# comrpehension way _identical output faster execution 
running_fast = [i["instanceid"] for i in instances if i["state"] == "running"]

print(running)
print(running_fast)

#Dict comprehension- buold an id to type lookup table
id_to_type = {i["instanceid"]: i["type"] for i in instances}
print(id_to_type)

unique_types = {i["type"] for i in instances}
print(unique_types)

