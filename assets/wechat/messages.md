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

### 步骤5：等待搜索结果

```powershell
python scripts\winguictl.py wait sleep 1000
# 或等待搜索结果出现
python scripts\winguictl.py wait uia --window-id <wx_window_id> --text "好友备注名" --control-type ListItem --timeout 3
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
> 参考：pyweixin 中 `Messages.send_messages_to_friend` 的实现

### 步骤1：定位聊天输入框

聊天输入框的特征：
- `control_type="Edit"`
- `class="mmui::ChatInputField"`
- `automation_id="chat_input_field"`

```powershell
# 方式A：通过 automation_id 查找（推荐）
python scripts\winguictl.py find --window-id <wx_window_id> uia --automation-id chat_input_field

# 方式B：通过 class 查找
python scripts\winguictl.py snapshot --window-id <wx_window_id> uia --class ChatInputField
# 查找 class="mmui::ChatInputField" 的 Edit 控件，记录其 runtime_id
```

### 步骤2：等待输入框可用

```powershell
# 等待聊天输入框出现（通过 automation_id）
python scripts\winguictl.py wait uia --window-id <wx_window_id> --automation-id chat_input_field --timeout 3
```

### 步骤3：设置消息内容

```powershell
# 方式A：使用 uia-control set-text（推荐）
python scripts\winguictl.py uia-control --window-id <wx_window_id> --element-id <chat_input_runtime_id> set-text "你好，这是测试消息"

# 方式B：先点击输入框，再输入
python scripts\winguictl.py action --window-id <wx_window_id> click --relative-x <edit_x> --relative-y <edit_y>
python scripts\winguictl.py action --window-id <wx_window_id> type --text "你好，这是测试消息"
```

### 步骤4：发送消息

```powershell
# 使用快捷键 Alt+S 发送（推荐，invoke无法正常发送消息）
python scripts\winguictl.py action --window-id <wx_window_id> hotkey --keys "{ALT}" "{S}"

```

### 步骤5：等待消息发送完成

```powershell
# 等待消息出现在聊天记录中（OCR 方式）
python scripts\winguictl.py wait text --window-id <wx_window_id> "你好，这是测试消息" --timeout 5
```

#### 完整示例：向文件传输助手发送消息

```powershell
# 1. 获取微信主窗口ID
python scripts\winguictl.py window list
# 假设微信窗口ID为 4399352

# 2. 聚焦微信窗口
python scripts\winguictl.py window --window-id 4399352 focus

# 3. 获取UIA快照，找到文件传输助手
python scripts\winguictl.py snapshot --window-id 4399352 uia --skip-actions --skip-state
# 找到 session_item_文件传输助手 的 runtime_id

# 4. 点击文件传输助手打开聊天窗口
python scripts\winguictl.py uia-control --window-id 4399352 --element-id <file_transfer_runtime_id> invoke

# 5. 等待聊天输入框出现
python scripts\winguictl.py wait uia --window-id 4399352 --automation-id chat_input_field --timeout 3

# 6. 获取聊天输入框的 runtime_id
python scripts\winguictl.py find --window-id 4399352 uia --automation-id chat_input_field
# 假设 runtime_id 为 42-4399352-4--2147482732

# 7. 设置消息内容
python scripts\winguictl.py uia-control --window-id 4399352 --element-id "42-4399352-4--2147482732" set-text "收到"

# 8. 发送消息
python scripts\winguictl.py action --window-id 4399352 hotkey --keys "{ALT}" "{S}"

# 9. 等待消息发送完成
python scripts\winguictl.py wait uia --window-id 4399352 --text "收到" --control-type ListItem --timeout 5
```

#### 长文本处理（超过2000字）

```powershell
# 若消息超过2000字，需先转换为 txt 文件发送
# 使用 PowerShell 创建临时文件
$longText = "...超过2000字的文本..."
$tempFile = "$env:TEMP\LongText.txt"
$longText | Out-File -FilePath $tempFile -Encoding UTF8

# 将文件复制到剪贴板（需借助 Python 脚本或外部工具）
# 然后粘贴到微信输入框
python scripts\winguictl.py action --window-id <wx_window_id> hotkey --keys "{CTRL}" "{V}"

# 等待文件加载
python scripts\winguictl.py wait sleep 1000

# 发送
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
python scripts\winguictl.py wait sleep 1000
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
python scripts\winguictl.py wait sleep 500

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
python scripts\winguictl.py wait sleep 1000
# 或等待接龙窗口出现
python scripts\winguictl.py wait window "接龙" --timeout 3
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
python scripts\winguictl.py wait uia --window-id <wx_window_id> --text "搜索" --control-type Edit --timeout 3
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

### 步骤4：等待新消息出现

```powershell
# 等待新消息提示出现（OCR 方式）
python scripts\winguictl.py wait ocr --window-id <wx_window_id> "[1条]" --timeout 60

# 等待新消息提示消失（表示已读）
python scripts\winguictl.py wait ocr --window-id <wx_window_id> "[1条]" --disappear --timeout 5
```

## 3.9 等待消息发送完成

```powershell
# 发送消息后，等待输入框清空
python scripts\winguictl.py action --window-id <wx_window_id> type --text "测试消息"
python scripts\winguictl.py action --window-id <wx_window_id> hotkey --keys "{ALT}" "{S}"

# 等待消息出现在聊天记录中
python scripts\winguictl.py wait text --window-id <wx_window_id> "测试消息" --timeout 5
```
