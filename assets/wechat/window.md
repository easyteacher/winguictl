# 窗口定位与微信主界面操作

---

## 2.1 查找微信窗口

```powershell
# 列出所有可见窗口，识别微信窗口 ID
python scripts\winguictl.py window list
```

## 2.2 打开/激活微信主界面

```powershell
# 如果微信已最小化，恢复窗口
python scripts\winguictl.py window --window-id <wx_window_id> restore

# 将微信窗口置于前台
python scripts\winguictl.py window --window-id <wx_window_id> focus

# 最大化微信窗口（对应 is_maximize=True）
python scripts\winguictl.py window --window-id <wx_window_id> maximize
```

## 2.3 移动窗口到屏幕中央

```powershell
# 获取窗口当前位置和大小（从 window list 或 snapshot 获取）
# 计算屏幕中央坐标后移动
# 屏幕宽度/高度可通过系统 API 获取，或使用 PowerShell:
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.WorkingArea

# 移动窗口（假设窗口大小为 1000x800）
$newX = ($screen.Width - 1000) / 2
$newY = ($screen.Height - 800) / 2
python scripts\winguictl.py window --window-id <wx_window_id> move --x $newX --y $newY
```

## 2.4 关闭微信窗口

```powershell
# 关闭窗口（对应 close_weixin=True）
python scripts\winguictl.py window --window-id <wx_window_id> close
```

## 2.5 取消窗口置顶

微信主界面操作后可能需要取消置顶，以便独立窗口正常显示：

```powershell
# 使用 Win32 API SetWindowPos HWND_NOTOPMOST
# winguictl 暂不支持直接设置窗口 Z-Order，需借助外部脚本或 pywinauto
# 替代方案：最小化再恢复主窗口
python scripts\winguictl.py window --window-id <wx_window_id> minimize
python scripts\winguictl.py window --window-id <wx_window_id> restore
```
