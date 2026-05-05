# WeChat 4.x PC 版自动化操作指南（winguictl 命令行版）

本指南基于 `pyweixin` 功能模块，将其转换为 `winguictl` 命令行操作形式，供 Agent 直接查阅和执行。
- `pyweixin` 仓库：https://github.com/Hello-Mr-Crab/pywechat

## 通用前提条件

在执行任何微信自动化操作前，**必须先确保微信主窗口处于前台可见状态**。这是所有后续操作的基础。

详见：[窗口定位与微信主界面操作](./window.md)

---

## 目录

| 文件 | 描述 | 关键词 |
|------|------|--------|
| [window.md](./window.md) | 启动微信、激活微信窗口 | 窗口、定位、后台、启动、激活、前台 |
| [search.md](./search.md) | 搜索操作（联系人、群聊、聊天记录） | 搜索、查找、联系人、群聊、聊天记录、搜索框 |
| [messages.md](./messages.md) | 消息操作 | 消息、聊天、发送、接收、会话列表 |
| [contacts.md](./contacts.md) | 通讯录与联系人操作 | 通讯录、联系人、好友列表、资料 |
| [files.md](./files.md) | 导出文件操作 | 文件、导出、另存为、聊天文件 |
| [calls.md](./calls.md) | 语音与视频通话 | 语音、视频、通话、VoIP、拨打、接听、挂断 |
| [moments.md](./moments.md) | 朋友圈操作 | 朋友圈、发表、浏览、相机、动态 |
| [favorites.md](./favorites.md) | 收藏与笔记 | 收藏、笔记、保存 |
| [settings.md](./settings.md) | 微信设置 | 设置、通用、主题、外观、语言、深色模式、浅色模式 |
| [friend-settings.md](./friend-settings.md) | 好友设置 | 消息免打扰、置顶、折叠 |
| [auto-reply.md](./auto-reply.md) | 自动回复与消息监听 | 自动回复、监听、循环检查 |
| [system-tools.md](./system-tools.md) | 系统工具与辅助功能 | 安装路径、wxid、版本号、剪贴板、注册表 |
| [faq.md](./faq.md) | 常见问题与注意事项 + 多语言对照表 + 命令速查 | FAQ、常见问题、未启动、未登录、定位失败、坐标不准、频率限制、风控 |
