**Example 1: 修改数据库账号密码**

修改数据库账号密码

Input: 

```
tccli cynosdb ResetAccountPassword --cli-unfold-argument  \
    --ClusterId cynosdbpg-on5xw0ni \
    --AccountName root \
    --AccountPassword abc@2018
```

Output: 
```
{
    "Response": {
        "RequestId": "148561"
    }
}
```

