**Example 1: 创建专业版实例**

创建峰值带宽为 20MB/s，硬盘大小 200GB 的专业版实例

Input: 

```
tccli ckafka CreateInstancePost --cli-unfold-argument  \
    --InstanceName test45 \
    --VpcId vpc-xxxxxxxx \
    --SubnetId subnet-xxxxxxxx \
    --KafkaVersion 2.4.2 \
    --SpecificationsType profession \
    --DiskType CLOUD_BASIC \
    --BandWidth 20 \
    --DiskSize 200 \
    --Partition 400 \
    --TopicNum 200 \
    --ZoneId 450001
```

Output: 
```
{
    "Response": {
        "Result": {
            "ReturnCode": "abc",
            "ReturnMessage": "abc",
            "Data": {
                "FlowId": 0,
                "RouteDTO": {
                    "RouteId": 0
                }
            }
        },
        "RequestId": "abc"
    }
}
```

