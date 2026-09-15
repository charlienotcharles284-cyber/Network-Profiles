# Charlie 个人预设

导入 URL：
https://raw.githubusercontent.com/charlienotcharles284-cyber/Network-Profiles/main/JS/Runestone_Charlie.js

先阅读 [V3 导入与回退](RUNESTONE_V3.md)。该版本待真实订阅验收，本机应用识别为 1.0.10（52）；没有更改正在使用的 Hako 配置。

| 服务 | 新配置初始选择 |
|---|---|
| 国内命中规则 | DIRECT |
| Facebook / Instagram / Threads | 各自优先新加坡 Auto |
| WhatsApp / Telegram / LinkedIn | 新加坡 Auto |
| Pixiv / X / YouTube / GitHub | 日本 Auto |
| ChatGPT / Claude / Gemini / Google（含 Gmail） | 日本 Auto |
| Spotify | 马来西亚 Auto 优先；首次导入务必按账号实际地区选择 |
| Apple / Apple Push | DIRECT 优先，Push 保留代理回退 |

以上只从实际存在的组中选择；不存在首选地区时按备选排序。已有客户端记忆选择可能覆盖新的排序，升级后检查一次。Auto 会根据测速在同一地区内选择节点。

澳洲、印度、马来西亚均可在服务组中选择。服务组的列表顺序不是跨国自动故障切换。所有地区仅保留 Auto 组，Meta 服务各自选择地区。Pixiv、LinkedIn、Threads 紧接 Speedtest 排列。

AI 组保留手动选择其他出口的能力；排序不代表服务地区资格保证。Spotify 默认马来西亚只是历史偏好预设，不会修改账号地区、付款地区或会员资格。YouTube 默认日本，若需要匹配现有会员地区请手动调整。

V1/V2 仅修复 Fork MRS 地址，作为旧行为回退入口。V3 通用版与个人版统一来源：

```
node scripts/build-personal.cjs
node scripts/build-personal.cjs --check
node --test tests/runestone.test.cjs
```

只编辑 Runestone_V3.js，再生成个人版本，避免重复维护逻辑。
