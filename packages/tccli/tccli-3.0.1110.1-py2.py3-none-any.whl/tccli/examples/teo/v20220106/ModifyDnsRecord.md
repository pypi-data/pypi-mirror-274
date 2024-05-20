**Example 1: 修改 DNS 记录**



Input: 

```
tccli teo ModifyDnsRecord --cli-unfold-argument  \
    --Priority 0 \
    --Name xx \
    --ZoneId xx \
    --Content xx \
    --Mode xx \
    --Ttl 0 \
    --Type xx \
    --Id xx
```

Output: 
```
{
    "Response": {
        "Status": "xx",
        "Priority": 0,
        "Locked": true,
        "Name": "xx",
        "CreatedOn": "2020-09-22T00:00:00+00:00",
        "ZoneId": "xx",
        "Content": "xx",
        "Cname": "xx",
        "RequestId": "xx",
        "Ttl": 0,
        "ModifiedOn": "2020-09-22T00:00:00+00:00",
        "Mode": "xx",
        "Type": "xx",
        "Id": "xx",
        "ZoneName": "xx"
    }
}
```

