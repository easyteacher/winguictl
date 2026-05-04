# 前置准备与全局配置

> 本指南基于 `pyweixin` 功能模块，将其转换为 `winguictl` 命令行操作形式，供 Agent 直接查阅和执行。
>
> - `pyweixin` 仓库：https://github.com/Hello-Mr-Crab/pywechat
> - 支持微信版本：4.1.6+ ~ 4.1.9+
> - 支持系统：Windows 10 / Windows 11
> - 语言支持：简体中文、English、繁體中文

---

## 1.1 环境要求

- Python 3.9+
- 安装依赖：`pip install pywinauto pyautogui psutil pycaw sounddevice soundfile packaging`
- 微信 4.0 版本已安装并登录
- 微信语言可在 `pyweixin` 中自动检测，若检测失败需手动设置

## 1.2 全局配置参数

`pyweixin` 中 `GlobalConfig` 的全局参数，在 `winguictl` 中需通过命令组合实现：

| 配置项 | 含义 | 默认值 | 对应操作 |
|--------|------|--------|----------|
| `is_maximize` | 微信主界面是否全屏 | `False` | `winguictl.py window --window-id <id> maximize` |
| `close_weixin` | 任务结束后是否关闭微信 | `True` | `winguictl.py window --window-id <id> close` |
| `load_delay` | 小程序/视频号/公众号加载时长 | `3.5` | 命令间 `Start-Sleep -Seconds 3.5` |
| `search_pages` | 会话列表查找好友时滚动次数 | `5` | 循环执行 `press-key --key "{PGDN}"` |
| `window_maximize` | 独立窗口是否全屏 | `False` | `winguictl.py window --window-id <id> maximize` |
| `send_delay` | 发送消息间隔 | `0.2` | 命令间 `Start-Sleep -Milliseconds 200` |
| `audio_length` | 语音长度限制 | `60` | 音频预处理参数 |
| `clear` | 发送前是否清除已有内容 | `True` | `hotkey --keys "{CTRL}" "{A}"` + `press-key --key "{DELETE}"` |
| `language` | 微信当前语言 | 自动检测 | 需根据语言调整查找文本 |
| `Version` | 微信版本 | 自动检测 | 影响部分 UI 定位逻辑 |

## 1.3 微信窗口特征

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
