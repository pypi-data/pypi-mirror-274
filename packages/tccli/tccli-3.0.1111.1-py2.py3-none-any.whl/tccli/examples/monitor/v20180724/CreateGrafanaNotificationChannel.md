**Example 1: 创建 Grafana 告警通道**

创建 Grafana 告警通道

Input: 

```
tccli monitor CreateGrafanaNotificationChannel --cli-unfold-argument  \
    --InstanceId grafana-abcdefgh \
    --ChannelName test \
    --OrgId 0 \
    --Receivers abc
```

Output: 
```
{
    "Response": {
        "ChannelId": "abc",
        "RequestId": "abc"
    }
}
```

