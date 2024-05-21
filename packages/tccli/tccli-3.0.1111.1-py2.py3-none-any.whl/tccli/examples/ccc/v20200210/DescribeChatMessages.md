**Example 1: 查询聊天记录示例**

获取指定服务记录的文本消息记录。

Input: 

```
tccli ccc DescribeChatMessages --cli-unfold-argument  \
    --SdkAppId 1400000000 \
    --SessionId d6253538-7c28-477b-998a-919059801899
```

Output: 
```
{
    "Response": {
        "RequestId": "48edd236-7ef1-45af-9e12-fc376ba355bf",
        "TotalCount": 2,
        "Messages": [
            {
                "Timestamp": 1600007226,
                "From": "John",
                "Messages": [
                    {
                        "Type": "Text",
                        "Content": "Hello, how are you?"
                    },
                    {
                        "Type": "Image",
                        "Content": "https://example.com/image.jpg"
                    }
                ]
            },
            {
                "Timestamp": 1400753150,
                "From": "Alice",
                "Messages": [
                    {
                        "Type": "Text",
                        "Content": "Hi there!"
                    }
                ]
            }
        ]
    }
}
```

