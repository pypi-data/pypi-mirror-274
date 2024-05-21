**Example 1: 根据层级查找开发态上下游任务节点**

根据层级查找开发态上下游任务节点

Input: 

```
tccli wedata DescribeDependTasksDevDs --cli-unfold-argument  \
    --TaskId abc \
    --Deep 1 \
    --Up 1 \
    --ProjectId abc \
    --WorkflowId abc
```

Output: 
```
{
    "Response": {
        "Data": {
            "TasksList": [
                {
                    "TaskId": "abc",
                    "TaskName": "abc",
                    "WorkflowId": "abc",
                    "WorkflowName": "abc",
                    "ProjectName": "abc",
                    "ProjectIdent": "abc",
                    "Status": "abc",
                    "TaskTypeId": 1,
                    "TaskTypeDesc": "abc",
                    "ProjectId": "abc",
                    "FolderName": "abc",
                    "FolderId": "abc",
                    "FirstSubmitTime": "abc",
                    "FirstRunTime": "abc",
                    "ScheduleDesc": "abc",
                    "InCharge": "abc",
                    "CycleUnit": "abc",
                    "LeftCoordinate": 0,
                    "TopCoordinate": 0,
                    "VirtualFlag": true,
                    "TaskAction": "abc",
                    "DelayTime": 1,
                    "ExecutionStartTime": "abc",
                    "ExecutionEndTime": "abc",
                    "Layer": "abc",
                    "SourceServiceId": "abc",
                    "SourceServiceType": "abc",
                    "TargetServiceId": "abc",
                    "TargetServiceType": "abc",
                    "AlarmType": "abc",
                    "CreateTime": "abc",
                    "UserId": "abc",
                    "OwnerId": "abc",
                    "TenantId": "abc"
                }
            ],
            "LinksList": [
                {
                    "TaskTo": "abc",
                    "TaskFrom": "abc",
                    "LinkType": "abc",
                    "LinkId": "abc"
                }
            ]
        },
        "RequestId": "abc"
    }
}
```

