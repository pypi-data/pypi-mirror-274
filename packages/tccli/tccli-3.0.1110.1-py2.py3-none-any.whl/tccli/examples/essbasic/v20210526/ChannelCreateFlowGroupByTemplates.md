**Example 1: 通过多模板创建有2个合同的合同组**

1. 入参中FlowFileInfos有2个元素, 表示2个合同组成此合同组
2. 每个合同都是B2C合同

Input: 

```
tccli essbasic ChannelCreateFlowGroupByTemplates --cli-unfold-argument  \
    --Agent.ProxyOperator.OpenId kev_8 \
    --Agent.ProxyOrganizationOpenId kev_open_organization_8 \
    --Agent.AppId 16fd2f7d7ae85d13ca5f8d501d57b5ec \
    --FlowGroupName 2023年张三入职合同组合 \
    --FlowInfos.0.FlowName 2023年张三入职合同 \
    --FlowInfos.0.FlowApprovers.0.OrganizationName 典子谦示例企业 \
    --FlowInfos.0.FlowApprovers.0.OrganizationOpenId kev_open_organization_8 \
    --FlowInfos.0.FlowApprovers.0.OpenId kev_8 \
    --FlowInfos.0.FlowApprovers.0.ApproverType ORGANIZATION \
    --FlowInfos.0.FlowApprovers.0.RecipientId yDwgKUUckp1jdybwUWptGKyGVpNME9fH \
    --FlowInfos.0.FlowApprovers.1.Name 张三 \
    --FlowInfos.0.FlowApprovers.1.Mobile 18888888888 \
    --FlowInfos.0.FlowApprovers.1.ApproverType PERSON \
    --FlowInfos.0.FlowApprovers.1.RecipientId yDwgKUUckp1jdybvUWptGKBD9TeupFMV \
    --FlowInfos.0.Deadline 1698202075 \
    --FlowInfos.0.TemplateId yDwgKUUckp1jdy4dUWptGKRavSGWt9cW \
    --FlowInfos.1.FlowName 2023年张三入职保密协议 \
    --FlowInfos.1.FlowApprovers.0.OrganizationName 典子谦示例企业 \
    --FlowInfos.1.FlowApprovers.0.OrganizationOpenId kev_open_organization_8 \
    --FlowInfos.1.FlowApprovers.0.OpenId kev_8 \
    --FlowInfos.1.FlowApprovers.0.ApproverType ORGANIZATION \
    --FlowInfos.1.FlowApprovers.0.RecipientId yDwgKUUckp1jdybwUWptGKyGVpNME9fH \
    --FlowInfos.1.FlowApprovers.1.Name 张三 \
    --FlowInfos.1.FlowApprovers.1.Mobile 18888888888 \
    --FlowInfos.1.FlowApprovers.1.ApproverType PERSON \
    --FlowInfos.1.FlowApprovers.1.RecipientId yDwgKUUckp1jdybvUWptGKBD9TeupFMV \
    --FlowInfos.1.Deadline 1698202075 \
    --FlowInfos.1.TemplateId yDRS4UUgygqdcj51UuO4zjEyWTmzsIAR
```

Output: 
```
{
    "Response": {
        "FlowGroupId": "yDwiwUUckpo0n304UuwJzdxCQJhOooyw",
        "FlowIds": [
            "yDwiwUUckpo0n30bUuwJzdxxvnaMZpxW",
            "yDwiwUUckpo0n30uUuwJzdxxwyCoXw1Z"
        ],
        "RequestId": "s1698201691021218250",
        "TaskInfos": [
            {
                "TaskId": "",
                "TaskStatus": ""
            },
            {
                "TaskId": "",
                "TaskStatus": ""
            }
        ]
    }
}
```

**Example 2: 通过多模板创建有2个合同的合同组，指定每个子合同第一方为动态签署方**

1. 入参中FlowFileInfos有2个元素, 表示2个合同组成此合同组
2. 每个合同都是B2C合同
4.指定子合同一方为动态签署方（即不指定具体签署人，FillType=1），可在发起后再进行补充。

Input: 

```
tccli essbasic ChannelCreateFlowGroupByTemplates --cli-unfold-argument  \
    --Agent.ProxyOperator.OpenId kev_8 \
    --Agent.ProxyOrganizationOpenId kev_open_organization_8 \
    --Agent.AppId 16fd2f7d7ae85d13ca5f8d501d57b5ec \
    --FlowGroupName 2023年张三入职合同组合 \
    --FlowInfos.0.FlowName 2023年张三入职合同 \
    --FlowInfos.0.FlowApprovers.0.ApproverOption.FillType 1 \
    --FlowInfos.0.FlowApprovers.0.ApproverType ORGANIZATION \
    --FlowInfos.0.FlowApprovers.0.RecipientId yDwgKUUckp1jdybwUWptGKyGVpNME9fH \
    --FlowInfos.0.FlowApprovers.1.Name 张三 \
    --FlowInfos.0.FlowApprovers.1.Mobile 18888888888 \
    --FlowInfos.0.FlowApprovers.1.ApproverType PERSON \
    --FlowInfos.0.FlowApprovers.1.RecipientId yDwgKUUckp1jdybvUWptGKBD9TeupFMV \
    --FlowInfos.0.Deadline 1698202075 \
    --FlowInfos.0.TemplateId yDwgKUUckp1jdy4dUWptGKRavSGWt9cW \
    --FlowInfos.1.FlowName 2023年张三入职保密协议 \
    --FlowInfos.1.FlowApprovers.0.ApproverOption.FillType 1 \
    --FlowInfos.1.FlowApprovers.0.ApproverType ORGANIZATION \
    --FlowInfos.1.FlowApprovers.0.RecipientId yDwgKUUckp1jdybwUWptGKyGVpNME9fH \
    --FlowInfos.1.FlowApprovers.1.Name 张三 \
    --FlowInfos.1.FlowApprovers.1.Mobile 18888888888 \
    --FlowInfos.1.FlowApprovers.1.ApproverType PERSON \
    --FlowInfos.1.FlowApprovers.1.RecipientId yDwgKUUckp1jdybvUWptGKBD9TeupFMV \
    --FlowInfos.1.Deadline 1698202075 \
    --FlowInfos.1.TemplateId yDRS4UUgygqdcj51UuO4zjEyWTmzsIAR
```

Output: 
```
{
    "Response": {
        "Approvers": [
            {
                "Approvers": [
                    {
                        "ApproverRoleName": "",
                        "RecipientId": "yDSx0UUckptqcu0rUuvGhoq88RKQezmP",
                        "SignId": "yDCVHUUckpwbqurqUuyXGHS1da6wB7v2"
                    },
                    {
                        "ApproverRoleName": "",
                        "RecipientId": "yDCVHUUckpwbqurlUuyXGHSChXDgrj1C",
                        "SignId": "yDCVHUUckpwbqurgUuyXGHS1cwtnpm8o"
                    }
                ],
                "FlowId": "yDCVHUUckpwbqur3UuyXGHSxpj1wPeJn"
            },
            {
                "Approvers": [
                    {
                        "ApproverRoleName": "",
                        "RecipientId": "yDSx0UUckptqcu0rUuvGhoq88RKQezmP",
                        "SignId": "yDCVHUUckpwbqursUuyXGHSCOm804z86"
                    },
                    {
                        "ApproverRoleName": "",
                        "RecipientId": "yDCVHUUckpwbqurrUuyXGHS8cOo8z4Vc",
                        "SignId": "yDCVHUUckpwbqulcUuyXGHSSvCaqc6He"
                    }
                ],
                "FlowId": "yDCVHUUckpwbqur1UuyXGHS1JCWpHawy"
            }
        ],
        "FlowGroupId": "yDCVHUUckpwbqurkUuyXGHS89Y9LLM4x",
        "FlowIds": [
            "yDCVHUUckpwbqur3UuyXGHSxpj1wPeJn",
            "yDCVHUUckpwbqur1UuyXGHS1JCWpHawy"
        ],
        "RequestId": "s1711352113176693412",
        "TaskInfos": [
            {
                "TaskId": "",
                "TaskStatus": ""
            },
            {
                "TaskId": "",
                "TaskStatus": ""
            }
        ]
    }
}
```

