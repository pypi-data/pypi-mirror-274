**Example 1: 七层离线日志**



Input: 

```
tccli teo DownloadL4Logs --cli-unfold-argument  \
    --Limit 10 \
    --Offset 0 \
    --StartTime 2020-09-22T00:00:00+00:00 \
    --EndTime 2020-09-22T00:00:00+00:00 \
    --ZoneIds zone-2mzegj4vln5f
```

Output: 
```
{
    "Response": {
        "RequestId": "8b6a2aa9-46ef-46e5-ba87-c0e96326adfe",
        "Data": [
            {
                "Area": "mainland",
                "LogPacketName": "20220811-10-proxy-1491-11ed-9792-525400655ede",
                "LogTime": 1660212000,
                "LogStartTime": "2023-07-26T06:00:00+08:00",
                "LogEndTime": "2023-07-26T07:00:00+08:00",
                "ProxyId": "proxy-1491-11ed-9792-525400655ede",
                "Size": 20761,
                "Url": "https://log-down04-cn.edgeone.qcloud.com/20220811/2022081110-proxy-1491-11ed-9792-52we0655ede.log.gz"
            }
        ],
        "TotalCount": 128
    }
}
```

