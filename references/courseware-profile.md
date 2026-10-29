# 课件配置（courseware-profile.json）

## 1. 为什么需要配置

统一规范保证系列感，但不同类型的课件不该被同一套组件绑死。用一份轻量配置把**通用底线**、**类型专属**、**可选功能**分开。

配置放在项目根目录：`courseware-profile.json`。没有配置文件时使用默认值。

## 2. 字段

| 字段 | 取值 | 默认 | 说明 |
|---|---|---|---|
| `type` | `process` / `anatomy` / `experiment` / `comparison` | `process` | 决定启用哪套类型规则 |
| `voiceMode` | `required` / `optional` / `disabled` | `required` | 语音强制程度 |
| `quantityChart` | `required` / `optional` / `disabled` | `required` | 数量曲线与数量表 |
| `interactionLevel` | `basic` / `standard` / `advanced` | `standard` | 交互复杂度 |
| `offlineRequired` | `true` / `false` | `true` | 是否要求断网可运行 |
| `params` | 字符串数组 | `["t","voice","simple"]` | 实际支持的 URL 参数 |
| `publishMode` | `local` / `ask` / `auto` | `local` | 发布方式 |
| `knowledgeBase` | 路径字符串 | `""` | 本地知识库路径（可选） |

## 3. 四种类型的推荐配置

```json
{ "type": "process",    "voiceMode": "required", "quantityChart": "required", "interactionLevel": "standard", "params": ["t","voice","simple","xo","arr"] }
{ "type": "anatomy",    "voiceMode": "optional", "quantityChart": "disabled", "interactionLevel": "advanced", "params": ["voice","simple","panel"] }
{ "type": "experiment", "voiceMode": "optional", "quantityChart": "required", "interactionLevel": "advanced", "params": ["voice","simple"] }
{ "type": "comparison", "voiceMode": "required", "quantityChart": "required", "interactionLevel": "advanced", "params": ["t","voice","simple"] }
```

## 4. 豁免规则

- `voiceMode: "disabled"`：必须在交付说明里写明理由（如纯测验、纯图表）
- `quantityChart: "disabled"`：解剖型/纯结构型可以关闭；过程型默认不应关闭
- `interactionLevel: "basic"`：只保留旋转、缩放、阶段切换；不要求爆炸视图/剖切
- 豁免不是"省事"，是"教学目标不需要"；写不清理由就不要豁免

## 5. 发布方式

| 值 | 行为 |
|---|---|
| `local`（默认） | 只落本地并校验，不创建远程仓库 |
| `ask` | 交付时询问一次是否发布 |
| `auto` | 自动创建仓库并开 Pages（仅限用户明确授权的工作流） |

**公开仓库或 Pages 前必须**：

1. 扫描密钥、个人信息、内部文件、未授权素材
2. 确认用户已授权公开
3. 用户指定私有仓库时，不得擅自改成公开
4. 交付时说明哪些内容已上传、哪些仍在本地

## 6. 校验脚本如何读取

```bash
python scripts/check_courseware.py "<项目目录>"                  # 自动读根目录 profile
python scripts/check_courseware.py "<项目目录>" --profile x.json  # 指定 profile
```

脚本会用配置决定：

- 语音缺失是阻断还是跳过
- 数量表缺失是否阻断
- 是否检查离线外链
- 哪些 URL 参数必须被处理
