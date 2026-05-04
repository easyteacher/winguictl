# 语音与视频通话

---

## 6.1 拨打语音电话

### 步骤1：打开好友聊天窗口（不支持群聊）

```powershell
```

### 步骤2：点击"语音聊天"按钮

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "语音聊天" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --relative-x <voice_btn_x> --relative-y <voice_btn_y>
```

### 微信 4.1.8+ 版本语音和视频按钮合并

```powershell
# 点击后需按 Down + Enter 选择语音
python scripts\winguictl.py action --window-id <wx_window_id> press-key --key "{DOWN}"
python scripts\winguictl.py action --window-id <wx_window_id> press-key --key "{ENTER}"
```

### 步骤3：等待通话窗口弹出

```powershell
Start-Sleep -Seconds 1
```

### 步骤4：获取通话窗口并居中

```powershell
python scripts\winguictl.py window list
python scripts\winguictl.py window --window-id <voip_window_id> focus
```

## 6.2 拨打视频电话

### 步骤1：打开好友聊天窗口

```powershell
```

### 步骤2：点击"视频聊天"按钮（4.1.8+ 需从合并菜单选择）

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "语音聊天" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --relative-x <call_btn_x> --relative-y <call_btn_y>
```

### 4.1.8+ 版本按两次 Down + Enter 选择视频

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> press-key --key "{DOWN}"
python scripts\winguictl.py action --window-id <wx_window_id> press-key --key "{DOWN}"
python scripts\winguictl.py action --window-id <wx_window_id> press-key --key "{ENTER}"
```

## 6.3 接听/挂断电话

### 接听

```powershell
python scripts\winguictl.py find --window-id <voip_window_id> uia --text "接听" --control-type Button
python scripts\winguictl.py action --window-id <voip_window_id> click --relative-x <answer_x> --relative-y <answer_y>
```

### 挂断

```powershell
python scripts\winguictl.py find --window-id <voip_window_id> uia --text "拒绝" --control-type Button
python scripts\winguictl.py action --window-id <voip_window_id> click --relative-x <decline_x> --relative-y <decline_y>
```
