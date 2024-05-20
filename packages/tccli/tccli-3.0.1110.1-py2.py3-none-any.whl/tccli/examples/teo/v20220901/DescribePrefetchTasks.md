**Example 1: 查询预热任务**

通过 CreatePrefetchTasks 提交预热任务后，通过该查询接口查询预热任务记录及执行进度。

Input: 

```
tccli teo DescribePrefetchTasks --cli-unfold-argument  \
    --ZoneId zone-z8m9mgx \
    --StartTime 2022-02-09T00:00:00+08:00 \
    --EndTime 2022-02-09T23:59:00+08:00 \
    --Limit 1 \
    --Offset 7
```

Output: 
```
{
    "Response": {
        "RequestId": "abc-afhhakf-24hkahf-2424",
        "Tasks": [
            {
                "JobId": "20g9wz8m9mgx",
                "Status": "success",
                "Target": "http://www.qq.com/a.txt",
                "Type": "prefetch_url",
                "CreateTime": "2022-02-09T02:28:43Z",
                "UpdateTime": "2022-02-09T02:28:52Z"
            }
        ],
        "TotalCount": 8
    }
}
```

