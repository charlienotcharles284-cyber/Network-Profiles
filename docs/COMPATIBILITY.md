# 版本兼容记录

## 发布通道

| 通道 | 文件 | 网络行为 |
|---|---|---|
| Stable | `JS/Runestone_Charlie.js` | 保留 Hako 的 DNS、TUN 与端口设置 |
| Beta | `JS/Runestone_Charlie_Beta.js` | 只把 `tun.stack` 改为 `mips` |
| Upstream | `JS/Runestone_V3.js` | 跟随 kiki 通用 V3，不应用个人排序 |

## 当前基线

| 日期 | Hako 客户端 | Mihomo | 脚本版本 | 静态测试 | 真机测试 |
|---|---|---|---|---|---|
| 2026-09-19 | iOS 1.0.9 / macOS 1.0.12 / tvOS 1.0.12（公告） | 1.19.31（公告） | 2026.09.19 | 待本提交 CI | 待填写 |
| 2026-09-22 | 同上；V2 上游默认 MIPS | 1.19.31（公告） | 2026.09.22 | 本地测试通过 | 待填写 |

公开源码与商店构建可能不同步。每次测试记录 App 内版本、build 号、系统版本、设备、网络栈、脚本 commit 和结果。

## 更新规则

1. 客户端只优化体积、界面或生命周期时，不修改脚本。
2. 内核新增可选能力时，先在 Beta 测试。
3. 配置字段或覆写执行顺序变化时，修改脚本并运行手动 Validate Action。
4. 真机测试通过后，更新此表并创建新的稳定 tag。
5. `main` 是持续更新通道；稳定用户可使用 tag 对应的 Raw URL。

## MIPS 关系

- V2 现在明确写入 `tun.stack: mips`，并覆盖整套 DNS/TUN 网络配置。
- Stable V3 不指定 stack；Hako 输入为 MIPS 时使用 MIPS，输入为 gVisor 时继续使用 gVisor。
- Beta V3 只把 stack 改为 MIPS，用于和 Stable 做同配置对照。
