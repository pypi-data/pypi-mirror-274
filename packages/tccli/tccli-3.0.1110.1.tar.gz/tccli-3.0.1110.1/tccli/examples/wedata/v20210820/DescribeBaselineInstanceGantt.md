**Example 1: 查询基线实例甘特图**

查询基线实例甘特图

Input: 

```
tccli wedata DescribeBaselineInstanceGantt --cli-unfold-argument  \
    --BaselineInstanceId 0 \
    --ProjectId abc
```

Output: 
```
{
    "Response": {
        "Data": {
            "Id": 0,
            "BaselineId": 0,
            "BaselineName": "abc",
            "BaselineType": "abc",
            "BaselineDataTime": "2020-09-22 00:00:00",
            "CreateTime": "2020-09-22T00:00:00+00:00",
            "EstimatedEndTime": "2020-09-22T00:00:00+00:00",
            "BaselineInstanceStatus": "abc",
            "InChargeUin": "abc",
            "InChargeName": "abc",
            "WarningMargin": 0,
            "PromiseTime": "2020-09-22T00:00:00+00:00",
            "AlarmLevel": "abc",
            "ProjectId": "abc",
            "IsReady": "abc",
            "BaselineTaskInstances": null,
            "ShardKey": "abc",
            "ExceptionalTaskInstances": [
                {
                    "CriticalDependency": null,
                    "Id": 0,
                    "BaselineInstanceId": 0,
                    "BaselineType": "abc",
                    "BaselineDataTime": "abc",
                    "UpstreamInstanceIds": "abc",
                    "DownstreamInstanceIds": "abc",
                    "IsPromiseTask": true,
                    "TaskId": "abc",
                    "CurRunDate": "2020-09-22T00:00:00+00:00",
                    "TaskName": "abc",
                    "InCriticalPath": 0,
                    "InFirstLevel": true,
                    "EstimatedCostTime": 0,
                    "ActualCostTime": 0,
                    "LatestStartTime": "2020-09-22T00:00:00+00:00",
                    "ActualStartTime": "2020-09-22T00:00:00+00:00",
                    "EstimatedEndTime": "2020-09-22T00:00:00+00:00",
                    "LatestEndTime": "2020-09-22T00:00:00+00:00",
                    "ActualEndTime": "2020-09-22T00:00:00+00:00",
                    "TaskInstanceStatus": "abc",
                    "ProjectId": "abc",
                    "ShardKey": "abc",
                    "CreateTime": "abc",
                    "UpdateTime": "abc",
                    "UserUin": "abc",
                    "OwnerUin": "abc",
                    "AppId": "abc"
                }
            ],
            "TaskInstances": [
                {
                    "CriticalDependency": null,
                    "Id": 0,
                    "BaselineInstanceId": 0,
                    "BaselineType": "abc",
                    "BaselineDataTime": "abc",
                    "UpstreamInstanceIds": "abc",
                    "DownstreamInstanceIds": "abc",
                    "IsPromiseTask": true,
                    "TaskId": "abc",
                    "CurRunDate": "2020-09-22T00:00:00+00:00",
                    "TaskName": "abc",
                    "InCriticalPath": 0,
                    "InFirstLevel": true,
                    "EstimatedCostTime": 0,
                    "ActualCostTime": 0,
                    "LatestStartTime": "2020-09-22T00:00:00+00:00",
                    "ActualStartTime": "2020-09-22T00:00:00+00:00",
                    "EstimatedEndTime": "2020-09-22T00:00:00+00:00",
                    "LatestEndTime": "2020-09-22T00:00:00+00:00",
                    "ActualEndTime": "2020-09-22T00:00:00+00:00",
                    "TaskInstanceStatus": "abc",
                    "ProjectId": "abc",
                    "ShardKey": "abc",
                    "CreateTime": "abc",
                    "UpdateTime": "abc",
                    "UserUin": "abc",
                    "OwnerUin": "abc",
                    "AppId": "abc"
                }
            ],
            "CriticalStartTime": "2020-09-22T00:00:00+00:00",
            "CriticalTaskInstances": [
                {
                    "CriticalDependency": null,
                    "Id": 0,
                    "BaselineInstanceId": 0,
                    "BaselineType": "abc",
                    "BaselineDataTime": "abc",
                    "UpstreamInstanceIds": "abc",
                    "DownstreamInstanceIds": "abc",
                    "IsPromiseTask": true,
                    "TaskId": "abc",
                    "CurRunDate": "2020-09-22T00:00:00+00:00",
                    "TaskName": "abc",
                    "InCriticalPath": 0,
                    "InFirstLevel": true,
                    "EstimatedCostTime": 0,
                    "ActualCostTime": 0,
                    "LatestStartTime": "2020-09-22T00:00:00+00:00",
                    "ActualStartTime": "2020-09-22T00:00:00+00:00",
                    "EstimatedEndTime": "2020-09-22T00:00:00+00:00",
                    "LatestEndTime": "2020-09-22T00:00:00+00:00",
                    "ActualEndTime": "2020-09-22T00:00:00+00:00",
                    "TaskInstanceStatus": "abc",
                    "ProjectId": "abc",
                    "ShardKey": "abc",
                    "CreateTime": "abc",
                    "UpdateTime": "abc",
                    "UserUin": "abc",
                    "OwnerUin": "abc",
                    "AppId": "abc"
                }
            ],
            "UpdateTime": "2020-09-22T00:00:00+00:00",
            "AppId": "abc",
            "OwnerUin": "abc",
            "UserUin": "abc"
        },
        "RequestId": "abc"
    }
}
```

