**Example 1: 查询最近上报的训练自定义指标**



Input: 

```
tccli tione DescribeLatestTrainingMetrics --cli-unfold-argument  \
    --TaskId taskid-xyz
```

Output: 
```
{
    "Response": {
        "RequestId": "123fa8123",
        "TaskId": "taskid-xyz",
        "Metrics": [
            {
                "MetricName": "loss",
                "Values": [
                    {
                        "Timestamp": 1641002400,
                        "Value": 182.06
                    },
                    {
                        "Timestamp": 1641002410,
                        "Value": 176.06
                    }
                ]
            }
        ]
    }
}
```

