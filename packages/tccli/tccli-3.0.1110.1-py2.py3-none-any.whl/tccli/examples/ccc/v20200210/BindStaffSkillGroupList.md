**Example 1: 绑定坐席所属技能组示例**



Input: 

```
tccli ccc BindStaffSkillGroupList --cli-unfold-argument  \
    --SdkAppId 1400000000 \
    --StaffEmail staff1@xxx.com \
    --StaffSkillGroupList.0.SkillGroupId 100 \
    --StaffSkillGroupList.0.Priority 1
```

Output: 
```
{
    "Response": {
        "RequestId": "48edd236-7ef1-45af-9e12-fc376ba355bf"
    }
}
```

