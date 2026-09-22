# Changelog

## 2026.09.22

- 跟随上游将 V2 的 TUN stack 从 gVisor 切换为 MIPS。
- 同步 V1 的完整 Advertising 规则方案；V1 的拦截范围相应扩大。
- 将上游 V2 的 Amazon 策略组和精确商城域名移植到 V3、Stable 与 Beta。
- 不匹配整个 `amazonaws.com`，避免无关 AWS 服务被 Amazon 策略接管。
- 规则更新时从 AdvertisingLite Domain MRS 移除 `alicdn.com`，降低误拦截风险。
- Stable 继续继承 Hako 的 stack；Beta 继续显式设为 MIPS。

## 2026.09.19

- 将通用 V1/V2/V3 来源迁移到 `kiki-rgb-00/kiki`。
- 从新 V3 吸收 Microsoft 策略组与规则更新。
- 保留 `Runestone_Charlie.js` 作为稳定通道。
- 新增只覆盖 `tun.stack: mips` 的 `Runestone_Charlie_Beta.js`。
- 恢复仅手动触发的 `Validate Runestone` 工作流。
- 新增兼容记录、上游同步说明和 MIPS 真机测试矩阵。
