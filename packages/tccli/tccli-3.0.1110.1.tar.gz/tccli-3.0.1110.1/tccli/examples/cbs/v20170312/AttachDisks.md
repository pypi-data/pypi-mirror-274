**Example 1: 挂载云硬盘**

将云硬盘disk-lzrg2pwi挂载到子机ins-dyzmimrw上

Input: 

```
tccli cbs AttachDisks --cli-unfold-argument  \
    --DiskIds disk-lzrg2pwi \
    --InstanceId ins-dyzmimrw
```

Output: 
```
{
    "Response": {
        "RequestId": "e0f140e5-14d6-c4a1-91e0-5a1f7f05a68a"
    }
}
```

