**Example 1: 共享镜像**

共享镜像img-6pb6lrmy给账户1038493875

Input: 

```
tccli cvm ModifyImageSharePermission --cli-unfold-argument  \
    --AccountIds 1038493875 \
    --Permission SHARE \
    --ImageId img-6pb6lrmy
```

Output: 
```
{
    "Response": {
        "RequestId": "71e69b56-32be-4412-ab45-49eded6a87be"
    }
}
```

