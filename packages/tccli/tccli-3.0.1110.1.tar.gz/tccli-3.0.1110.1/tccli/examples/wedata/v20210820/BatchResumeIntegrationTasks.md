**Example 1: BatchResumeIntegrationTasks**



Input: 

```
tccli wedata BatchResumeIntegrationTasks --cli-unfold-argument  \
    --ProjectId 17865298918277529 \
    --TaskIds 20220506145218687 20230506145218687 \
    --TaskType 201
```

Output: 
```
{
    "Response": {
        "SuccessCount": 1,
        "FailedCount": 1,
        "TotalCount": 2,
        "RequestId": "aasd-2343-2342-acef-35af"
    }
}
```

