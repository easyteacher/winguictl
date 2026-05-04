# 前置准备与全局配置

> 本指南基于 `pyweixin` 功能模块，将其转换为 `winguictl` 命令行操作形式，供 Agent 直接查阅和执行。
>
> - `pyweixin` 仓库：https://github.com/Hello-Mr-Crab/pywechat
> - 支持微信版本：4.1.6+ ~ 4.1.9+
> - 支持系统：Windows 10 / Windows 11
> - 语言支持：简体中文、English、繁體中文

---

## 1.1 打开微信主窗口（重要，后续操作依赖微信主窗口）

即使微信已打开，也需要执行此步骤，确保窗口可见。

```powershell
Start-Process "C:\Program Files (x86)\Tencent\Weixin\Weixin.exe" --scene=taskbarpins
```

## 1.2 微信窗口特征

微信主窗口的 UIA 特征：
- `class_name`: `mmui::MainWindow`
- `class_name` (登录界面): `mmui::LoginWindow`
- 通用 Qt 窗口类名：`Qt\d+QWindowIcon`

获取微信窗口 ID：

```powershell
# 列出所有窗口，找到微信主窗口
python scripts\winguictl.py window list

# 通过窗口标题模糊查找（假设微信标题包含"微信"）
# 然后使用 snapshot 确认 class_name
python scripts\winguictl.py snapshot --window-id <window_id> uia --skip-actions
```
