# 窗口定位与微信主界面操作

## 打开/激活微信主界面

**重要，后续操作依赖微信主窗口**

### 后台运行时或微信窗口快照返回空白时

带参数运行程序激活微信主界面
```powershell
Start-Process "C:\Program Files (x86)\Tencent\Weixin\Weixin.exe" --scene=taskbarpins
```

### 已有微信窗口时

#### 恢复最小化窗口
```powershell
python scripts\winguictl.py window --window-id <wx_window_id> restore
```

#### 将窗口置于前台
```powershell
python scripts\winguictl.py window --window-id <wx_window_id> focus
```

## 查找微信窗口

### 列出所有可见窗口，识别微信窗口 ID

```powershell
python scripts\winguictl.py window list
```

### 微信窗口特征

微信主窗口的 UIA 特征：
- `class_name`: `mmui::MainWindow`
- `class_name` (登录界面): `mmui::LoginWindow`
- 通用 Qt 窗口类名：`Qt\d+QWindowIcon`
