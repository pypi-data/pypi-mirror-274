**Example 1: 获取PerformanceProject信息**



Input: 

```
tccli rum DescribeDataPerformanceProject --cli-unfold-argument  \
    --ExtSecond 自定义2 \
    --Engine ie2 \
    --IsAbroad 1 \
    --Area 中国 \
    --NetType 2 \
    --CostType avg \
    --Level 1 \
    --Os apple \
    --Brand apple \
    --Isp 中国移动 \
    --VersionNum 版本 \
    --Platform 2 \
    --ExtThird 自定义3 \
    --ExtFirst 自定义1 \
    --StartTime 1625444040 \
    --Device 三星 \
    --From index.html \
    --EndTime 1625454840 \
    --Type pagepv \
    --ID 1 \
    --Browser ie
```

Output: 
```
{
    "Response": {
        "Result": "xxxx",
        "RequestId": "65a8fec7-2b39-4b11-893f-3715279d235f"
    }
}
```

