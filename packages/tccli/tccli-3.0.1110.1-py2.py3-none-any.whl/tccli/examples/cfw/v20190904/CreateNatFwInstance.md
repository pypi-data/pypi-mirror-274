**Example 1: 创建防火墙实例--新增模式**

新增模式示例

Input: 

```
tccli cfw CreateNatFwInstance --cli-unfold-argument  \
    --Name test \
    --Width 20 \
    --Mode 1 \
    --CrossAZone 1 \
    --NewModeItems.VpcList vpc-xxx \
    --NewModeItems.Eips xx.xx.xx.xx \
    --NewModeItems.AddCount 1 \
    --Zone ap-shanghai-4 \
    --ZoneBak ap-shanghai-3
```

Output: 
```
{
    "Response": {
        "CfwInsId": "xxx",
        "RequestId": "3c140219-cfe9-470e-b241-907877d6fb03"
    }
}
```

**Example 2: 创建NAT防火墙实例（Region参数必填）**

创建NAT防火墙实例（Region参数必填）

Input: 

```
tccli cfw CreateNatFwInstance --cli-unfold-argument  \
    --Name test \
    --Width 20 \
    --Mode 0 \
    --CrossAZone 1 \
    --NatGwList nat-xxx nat-xxx \
    --Zone ap-shanghai-4 \
    --ZoneBak ap-shanghai-3
```

Output: 
```
{
    "Response": {
        "CfwInsId": "xxx",
        "RequestId": "3c140219-cfe9-470e-b241-907877d6fb03"
    }
}
```

