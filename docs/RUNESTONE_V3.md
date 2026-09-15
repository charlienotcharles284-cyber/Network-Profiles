# Runestone V3（首版，待真实订阅验收）

V3 从 V2 演进，适用于 Hako 合并节点来源之后的 JavaScript 覆写阶段。保留 V1/V2；原有 YAML 配置不会自动升级为 V3。

## 导入与回退

1. 保留当前可用配置/脚本作为回退入口。
2. 在脚本库通过 **Raw JavaScript 文件 URL** 导入 V3，保存为新脚本。
3. 给测试配置选择节点来源，使用合并后脚本位置。不要同时启用旧全局脚本和新合并后脚本。
4. 检查生成的地区组，确认规则资源下载成功，再启用配置。
5. 若出现 no materialized nodes，说明脚本输入中没有展开的 `config.proxies`：检查节点来源和执行阶段。仅含 proxy-providers 的输入不会被误当作成功。
6. 回退时重新选择旧脚本/旧配置。不要删除订阅。

URL 导入保存的是脚本文本快照。更新 JS 后需要重新导入；rule-providers 的规则数据更新独立进行。仓库 main 源码与 App Store 版本不是同一发行物，界面名称可能不同。

## 改动边界

- 新增马来西亚、澳洲、印度；没有对应节点不生成该地区组。
- 每个识别地区都有 Auto（测速）和 Manual（手选）组。
- 补齐 Pixiv、LinkedIn、Threads 的核心域名；这些不是完整域名全集。
- 无节点、非法节点对象、重名、provider/组冲突、指向被移除组的 dialer-proxy 会报错。
- 未识别地区的节点保留在 All-Nodes；APNs-Fallback 在没有地区组时使用这些节点，避免空组。
- 保留输入的 DNS、TUN、端口、节点对象、proxy-providers 等字段；替换 proxy-groups、rules、rule-providers，设置 rule 模式及 store-selected。
- 不继承订阅自带的服务规则和策略组；依赖它们的复杂链式代理配置需先适配。
- 规则精确去重；移除 google/copilot/grok 的宽泛关键词，保留明确域名及最终代理兜底。
- 保留现有广告/Apple 规则顺序；不宣称已解决所有登录误拦截。后续应基于连接日志加入精确例外。

`RUNESTONE.repository` 集中控制项目 MRS 地址；其他第三方规则仍有各自来源。基础脚本的 `personal: false` 保留通用选择习惯。开启 personal 才应用个人地区排序。

## 验证与限制

2026-09-15：Node.js 行为测试通过；个人版本在 macOS JavaScriptCore（JXA）中执行成功。这不是 Hako 签名应用的完整运行测试。

检查了 Hako-Client 的 ScriptEngine/ScriptLibrary，以及 Hako 的 outboundgroup/parser.go、bind/hako/mrs_validation.go、config_pipeline.go。Hako 基于 Mihomo v1.19.30；Apple 层还有独立资源和配置校验，不能用普通 Mihomo 语法通过代替 Hako 实测。

真实订阅验收项目：节点合并、规则下载、配置启动、国内直连、目标服务命中、Telegram/WhatsApp 通话、Apple 推送、休眠唤醒和更新后恢复。未运行这些项目，不宣称能绕过服务地区限制或保证节点解锁。

测试：`node --test tests/runestone.test.cjs`。覆盖输入保护、网络设置保留、地区识别、空组、引用完整性、组循环、重复规则、幂等性与个人默认值。

## 长期维护

1. 规则同步工作流已存在；Fork 必须确认 Actions 已启用及最近运行成功。
2. 固定转换器版本，并补充下载校验、规则数量突变检查和失败时保留上次产物。
3. 当前 Rules YAML 来自完整 classical 上游，与 Domain/IP MRS 可能重叠。先量化再拆分，不能直接删除某一部分。
4. 每次脚本变更运行测试，每次 Hako 升级记录应用版本与源码提交并复测。
5. 重要账号固定地区/节点；Auto 的延迟探测不等于吞吐、UDP 或业务可用性检测。
6. 后续将服务域名逐步迁移为维护中的规则集，个人例外单独维护，避免多个列表长期漂移。

来源：
- https://github.com/TokenPLS/Hako-Client
- https://github.com/TokenPLS/Hako
- https://github.com/Sydney-Moses/Network-Profiles
- https://github.com/blackmatrix7/ios_rule_script
