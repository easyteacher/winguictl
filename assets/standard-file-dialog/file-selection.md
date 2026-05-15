# 文件选择与确认

## 文件列表操作

### 获取文件列表

```powershell
python winguictl.py find --window-id <id> uia --control-type List
python winguictl.py uia-control --window-id <id> --element-id "<list_id>" list-items
```

### 选择文件

```powershell
# 方法1：通过文件名选择
python winguictl.py find --window-id <id> uia --text "document.txt" --control-type ListItem
python winguictl.py uia-control --window-id <id> --element-id "<file_id>" select

# 方法2：通过列表索引选择
python winguictl.py uia-control --window-id <id> --element-id "<list_id>" list-select 0
```

### 双击打开文件

```powershell
python winguictl.py find --window-id <id> uia --text "document.txt" --control-type ListItem
python winguictl.py uia-control --window-id <id> --element-id "<file_id>" double-click
```

## 文件名输入

### 直接输入文件名

```powershell
python winguictl.py uia-control --window-id <id> --element-id "FileNameControlHost" set-text "myfile.txt"
```

### 追加/修改文件名

```powershell
# 获取当前文件名
python winguictl.py uia-control --window-id <id> --element-id "FileNameControlHost" get-text

# 清空后输入新文件名
python winguictl.py action --window-id <id> hotkey --keys "{CTRL}" "{A}"
python winguictl.py action --window-id <id> type --text "newfile.txt"
```

## 文件类型选择

### 展开文件类型下拉框

```powershell
python winguictl.py uia-control --window-id <id> --element-id "FileTypeControlHost" expand
```

### 选择文件类型

```powershell
# 方法1：通过索引选择
python winguictl.py uia-control --window-id <id> --element-id "FileTypeControlHost" combo-select 0 --index

# 方法2：通过文本选择
python winguictl.py uia-control --window-id <id> --element-id "FileTypeControlHost" combo-select "所有文件 (*.*)"
```

## 确认操作

### 点击"打开"或"保存"按钮

```powershell
# 方法1：使用 invoke（推荐）
python winguictl.py uia-control --window-id <id> --element-id "1" invoke

# 方法2：使用 click
python winguictl.py uia-control --window-id <id> --element-id "1" click

# 方法3：快捷键 Enter
python winguictl.py action --window-id <id> press-key --key "{ENTER}"
```

### 点击"取消"按钮

```powershell
python winguictl.py uia-control --window-id <id> --element-id "2" invoke
```

## 新建文件夹

```powershell
# 方法1：工具栏"新建文件夹"按钮
python winguictl.py find --window-id <id> uia --text "新建文件夹" --control-type Button
python winguictl.py action --window-id <id> click --element-id "<new_folder_id>"

# 方法2：快捷键 Ctrl+Shift+N
python winguictl.py action --window-id <id> hotkey --keys "{CTRL}" "{SHIFT}" "n"
```

## 完整示例：选择并打开文件

```powershell
# 1. 等待对话框出现
python winguictl.py wait window "打开" --class "#32770" --timeout 10

# 2. 获取对话框 ID
python winguictl.py window list
# 假设对话框 ID 为 123456

# 3. 导航到目标目录
python winguictl.py action --window-id 123456 hotkey --keys "{CTRL}" "{L}"
python winguictl.py action --window-id 123456 type --text "D:\Documents{ENTER}"

# 4. 选择文件
python winguictl.py find --window-id 123456 uia --text "report.docx" --control-type ListItem
python winguictl.py uia-control --window-id 123456 --element-id "<file_id>" select

# 5. 确认打开
python winguictl.py uia-control --window-id 123456 --element-id "1" invoke
```
