# 另存为对话框特有操作

另存为对话框与打开对话框类似，但有一些特有的操作场景。

## 对话框特征

| 属性 | 值 |
|------|-----|
| 标题 | "另存为"、"Save As" |
| 确认按钮 | "保存" (automation_id: `1`) |

## 设置保存文件名

```powershell
python winguictl.py uia-control --window-id <id> --element-id "FileNameControlHost" set-text "new_document.txt"
```

## 选择保存位置

### 方法1：地址栏输入路径（推荐）

```powershell
python winguictl.py action --window-id <id> hotkey --keys "{CTRL}" "{L}"
python winguictl.py action --window-id <id> type --text "D:\Backup{ENTER}"
```

### 方法2：导航窗格选择

```powershell
python winguictl.py find --window-id <id> uia --text "桌面" --control-type TreeItem
python winguictl.py uia-control --window-id <id> --element-id "<desktop_id>" select
```

## 选择保存格式

```powershell
# 展开文件类型下拉框
python winguictl.py uia-control --window-id <id> --element-id "FileTypeControlHost" expand

# 选择格式
python winguictl.py uia-control --window-id <id> --element-id "FileTypeControlHost" combo-select "文本文件 (*.txt)"
```

## 处理文件已存在提示

当保存的文件名已存在时，系统会弹出确认对话框：

```powershell
# 等待确认对话框
python winguictl.py wait window "确认另存为" --class "#32770" --timeout 5

# 点击"是"覆盖 (automation_id: CommandButton_6)
python winguictl.py uia-control --window-id <confirm_id> --element-id "CommandButton_6" invoke

# 或点击"否"取消 (automation_id: CommandButton_7)
python winguictl.py uia-control --window-id <confirm_id> --element-id "CommandButton_7" invoke
```

## 完整示例：另存为新文件

```powershell
# 1. 等待另存为对话框
python winguictl.py wait window "另存为" --class "#32770" --timeout 10

# 2. 获取对话框 ID
python winguictl.py window list
# 假设对话框 ID 为 123456

# 3. 设置保存路径
python winguictl.py action --window-id 123456 hotkey --keys "{CTRL}" "{L}"
python winguictl.py action --window-id 123456 type --text "D:\Output{ENTER}"

# 4. 设置文件名
python winguictl.py uia-control --window-id 123456 --element-id "FileNameControlHost" set-text "export_2025.txt"

# 5. 选择文件格式
python winguictl.py uia-control --window-id 123456 --element-id "FileTypeControlHost" expand
python winguictl.py uia-control --window-id 123456 --element-id "FileTypeControlHost" combo-select "所有文件 (*.*)"

# 6. 点击保存
python winguictl.py uia-control --window-id 123456 --element-id "1" invoke

# 7. 处理可能的覆盖确认
python winguictl.py wait window "确认另存为" --class "#32770" --timeout 3
python winguictl.py window list
# 假设确认对话框 ID 为 789012
python winguictl.py uia-control --window-id 789012 --element-id "CommandButton_6" invoke
```

## 常见问题

### 文件名包含特殊字符

Windows 文件名不能包含以下字符：`\ / : * ? " < > |`。如果文件名包含这些字符，保存会失败。

### 路径不存在

如果指定的保存路径不存在，需要先创建：

```powershell
# 使用 PowerShell 创建目录
New-Item -ItemType Directory -Path "D:\NewFolder" -Force
```

### 权限不足

如果保存到受保护的位置（如 `C:\`），会弹出权限错误。选择用户目录或其他有权限的位置。
