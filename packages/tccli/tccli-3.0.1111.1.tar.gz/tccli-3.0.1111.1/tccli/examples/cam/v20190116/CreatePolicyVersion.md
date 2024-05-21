**Example 1: 新增一个策略版本**

本示例将新增一个策略版本。

Input: 

```
tccli cam CreatePolicyVersion --cli-unfold-argument  \
    --PolicyId 17698703 \
    --PolicyDocument {"version":"2.0","statement":[{"effect":"allow","action":["name/cos:*"],"resource":["*"]}]} \
    --SetAsDefault true
```

Output: 
```
{
    "Response": {
        "VersionId": "4",
        "RequestId": "60e60a86-af67-4bbe-8377-7024a0e1d4c7"
    }
}
```

