# 消息操作

---

## 3.1 打开好友/群聊聊天窗口

### 方式A：通过顶部搜索栏搜索

### 步骤1：确保微信主界面在前台

```powershell
python scripts\winguictl.py window --window-id <wx_window_id> focus
```

### 步骤2：点击顶部搜索框（需先 snapshot 获取搜索框坐标）

```powershell
python scripts\winguictl.py snapshot --window-id <wx_window_id> uia
# 找到 control_type="Edit" 的搜索输入框，记录其 relative_rect和runtime_id
```

### 步骤3：清空并输入好友名称

```powershell
python scripts\winguictl.py uia-control --window-id <wx_window_id> --element-id <search_edit_runtime_id> set-text "好友备注名"
```

### 步骤4：点击搜索框

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> click --relative-x <search_x> --relative-y <search_y>
```

### 步骤5：等待搜索结果（sleep 1秒）

```powershell
Start-Sleep -Seconds 1
```

### 步骤6：点击第一个搜索结果（需先 find 定位）

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "好友备注名" --control-type ListItem
# 获取结果坐标后点击
python scripts\winguictl.py action --window-id <wx_window_id> click --relative-x <result_x> --relative-y <result_y>
```

### 方式B：在会话列表中查找

### 步骤1：点击左侧"微信"按钮（会话列表）

```powershell
# 先 snapshot 找到 Sidebar 中"微信"按钮的位置
python scripts\winguictl.py snapshot --window-id <wx_window_id> uia
# 找到 title="微信" 或对应语言的 Button
```

### 步骤2：点击该按钮

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> click --relative-x <weixin_btn_x> --relative-y <weixin_btn_y>
```

### 步骤3：在会话列表中滚动查找好友

```powershell
# 获取会话列表区域，使用 PGDN 滚动
python scripts\winguictl.py action --window-id <wx_window_id> press-key --key "{PGDN}"
# 每次滚动后使用 find ocr 或 snapshot 检查是否出现目标好友
```

### 步骤4：找到后点击好友 ListItem

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "好友备注名" --control-type ListItem
python scripts\winguictl.py action --window-id <wx_window_id> click --relative-x <friend_x> --relative-y <friend_y>
```

## 3.2 发送文本消息

> 前提：已打开好友聊天窗口

### 步骤1：定位输入框（Edit 控件）

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --control-type Edit --action set-text
# 或使用 OCR 找到输入框区域
```

### 步骤2：点击输入框

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> click --relative-x <edit_x> --relative-y <edit_y>
```

### 步骤3：清除已有内容（若 clear=True）

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> hotkey --keys "{CTRL}" "{A}"
python scripts\winguictl.py action --window-id <wx_window_id> press-key --key "{DELETE}"
```

### 步骤4：输入消息内容

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> type --text "你好，这是测试消息"
```

### 步骤5：发送（Alt+S 或点击发送按钮）

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> hotkey --keys "{ALT}" "{S}"
# 或点击发送按钮
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "发送" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --relative-x <send_btn_x> --relative-y <send_btn_y>
```

**长文本处理（超过2000字）**：

```powershell
# 若消息超过2000字，需先转换为 txt 文件发送
# 使用 PowerShell 创建临时文件
$longText = "...超过2000字的文本..."
$tempFile = "$env:TEMP\LongText.txt"
$longText | Out-File -FilePath $tempFile -Encoding UTF8

# 将文件复制到剪贴板（需借助 Python 脚本或外部工具）
# 然后粘贴到微信输入框
python scripts\winguictl.py action --window-id <wx_window_id> hotkey --keys "{CTRL}" "{V}"
python scripts\winguictl.py action --window-id <wx_window_id> hotkey --keys "{ALT}" "{S}"
```

## 3.3 发送文件

### 步骤1：将文件复制到剪贴板（CF_HDROP 格式）

```powershell
# 需借助 Python 脚本实现，参考 pyweixin WinSettings.copy_files_to_clipboard
```

### 步骤2：在聊天窗口中粘贴

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> hotkey --keys "{CTRL}" "{V}"
```

### 步骤3：等待文件加载后发送

```powershell
Start-Sleep -Seconds 1
python scripts\winguictl.py action --window-id <wx_window_id> hotkey --keys "{ALT}" "{S}"
```

## 3.4 发送语音（4.1.9+ 版本支持）

### 步骤1：打开聊天窗口

```powershell
```

### 步骤2：找到"发语音"按钮并点击

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "发语音" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --relative-x <audio_btn_x> --relative-y <audio_btn_y>
```

### 步骤3：播放音频到虚拟音频设备（需配置 VB-Cable 等虚拟声卡）

```powershell
# 使用 sounddevice 播放音频，同时微信录制
```

### 步骤4：点击结束录音（再次点击语音按钮或等待自动结束）

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> click --relative-x <audio_btn_x> --relative-y <audio_btn_y>
```

## 3.5 @群成员

```powershell
# 在群聊输入框中输入 @ 符号
python scripts\winguictl.py action --window-id <wx_window_id> type --text "@"

# 等待弹出成员选择框
Start-Sleep -Seconds 0.5

# 输入成员昵称筛选
python scripts\winguictl.py action --window-id <wx_window_id> type --text "成员昵称"

# 按 Enter 选择
python scripts\winguictl.py action --window-id <wx_window_id> press-key --key "{ENTER}"

# @所有人
python scripts\winguictl.py action --window-id <wx_window_id> type --text "@所有人"
python scripts\winguictl.py action --window-id <wx_window_id> press-key --key "{ENTER}"
```

## 3.6 发起接龙

### 步骤1：打开群聊窗口

```powershell
```

### 步骤2：输入 #接龙

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> type --text "#接龙"
```

### 步骤3：按 Down + Enter 触发接龙窗口

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> press-key --key "{DOWN}"
python scripts\winguictl.py action --window-id <wx_window_id> press-key --key "{ENTER}"
```

### 步骤4：等待接龙窗口弹出，填写内容

```powershell
Start-Sleep -Seconds 1
# 使用 snapshot 找到接龙窗口，填写主题、示例、描述等
```

## 3.7 获取聊天记录

### 步骤1：打开好友聊天窗口

```powershell
```

### 步骤2：点击右上角"聊天记录"按钮

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "聊天记录" --control-type Button
python scripts\winguictl.py action --window-id <wx_window_id> click --relative-x <history_btn_x> --relative-y <history_btn_y>
```

### 步骤3：等待聊天记录窗口弹出

```powershell
Start-Sleep -Seconds 1
```

### 步骤4：使用 snapshot 或 find 遍历聊天记录列表

```powershell
python scripts\winguictl.py snapshot --window-id <history_window_id> uia
```

### 步骤5：滚动加载更多记录

```powershell
python scripts\winguictl.py action --window-id <history_window_id> press-key --key "{PGDN}"
```

## 3.8 检查新消息

### 步骤1：确保在会话列表界面

```powershell
python scripts\winguictl.py window --window-id <wx_window_id> focus
```

### 步骤2：使用 OCR 扫描左侧会话列表中的新消息提示

```powershell
python scripts\winguictl.py snapshot --window-id <wx_window_id> ocr
# 查找包含 "[数字]条" 或 "[数字]" 的文本（根据语言不同）
```

### 步骤3：点击有新消息的好友

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> ocr "[3条]"
python scripts\winguictl.py action --window-id <wx_window_id> click --relative-x <msg_x> --relative-y <msg_y>
```
