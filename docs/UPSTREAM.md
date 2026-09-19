# 上游迁移与同步策略

## 当前来源

- 当前上游：`https://github.com/kiki-rgb-00/kiki.git`
- 旧上游：`https://github.com/Sydney-Moses/Network-Profiles.git`
- 本 Fork：`https://github.com/charlienotcharles284-cyber/Network-Profiles.git`
- 首次迁移基线：`kiki/main@408cf598dfdbc38dc37f293c8842f66e47ab6aca`

新仓库使用独立 Git 历史，因此不把它与旧 Fork 强行合并。同步时只审查并引入需要的文件，保留本 Fork 的个人脚本、测试、文档和远程规则地址。

## 本地 remote

```bash
git remote add kiki https://github.com/kiki-rgb-00/kiki.git
git fetch kiki main
```

如果 `kiki` 已存在，直接执行 `git fetch kiki main`。同步时先比较：

```bash
git diff --stat main..kiki/main
git diff main..kiki/main -- JS/Runestone_V1.js JS/Runestone_V2.js JS/Runestone_V3.js
```

确认后按文件引入 V1/V2/V3、规则同步脚本和正式工作流，再运行：

```bash
node scripts/build-personal.cjs
node scripts/build-personal.cjs --check
node --test tests/runestone.test.cjs
python -m unittest tests/test_sync_services.py
```

不要用上游 README 覆盖本 Fork 文档，也不要删除 `Runestone_Charlie*.js`、`tests/` 或手动验证工作流。
