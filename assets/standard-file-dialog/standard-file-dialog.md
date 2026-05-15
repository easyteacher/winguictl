# Windows 标准文件对话框操作指南

本指南介绍如何使用 `winguictl` 操作 Windows 系统标准的"打开"和"另存为"对话框。

## 对话框特征

| 属性 | 值 |
|------|-----|
| 标题 | "打开"、"另存为"、"Select Folder" 等 |
| 类名 | `#32770` |
| UIA 支持 | 完整支持（Win32 + UIA） |

## 快速开始

### 1. 定位对话框

```powershell
# 方法1：列出所有窗口，查找 class_name="#32770"
python winguictl.py window list

# 方法2：等待对话框出现
python winguictl.py wait window "另存为" --class "#32770" --timeout 10
```

### 2. 获取对话框结构

```powershell
python winguictl.py snapshot --window-id <dialog_id> uia
```

### 3. 常用控件 automation_id

| 控件 | automation_id | 说明 |
|------|---------------|------|
| 文件名输入框 | `FileNameControlHost` | 文件名 ComboBox |
| 文件名编辑框 | `1001` | 文件名 Edit（ComboBox 内部） |
| 文件类型下拉框 | `FileTypeControlHost` | 文件类型 ComboBox |
| 打开/保存按钮 | `1` | 确认按钮 |
| 取消按钮 | `2` | 取消按钮 |

**重要**: 不同 Windows 版本的 automation_id 可能不同。始终使用 `snapshot` 或 `find` 确认，优先使用 `runtime_id`。

## 核心操作

### 设置文件名

```powershell
python winguictl.py uia-control --window-id <id> --element-id "FileNameControlHost" set-text "filename.txt"
```

### 选择文件类型

```powershell
# 展开下拉框
python winguictl.py uia-control --window-id <id> --element-id "FileTypeControlHost" expand

# 选择文件类型（展开后）
python winguictl.py uia-control --window-id <id> --element-id "FileTypeControlHost" combo-select "所有文件 (*.*)"
```

### 导航到路径

```powershell
# 方法1：快捷键 Ctrl+L 聚焦地址栏
python winguictl.py action --window-id <id> hotkey --keys "{CTRL}" "{L}"
python winguictl.py action --window-id <id> type --text "D:\Projects{ENTER}"

# 方法2：直接设置地址栏
python winguictl.py uia-control --window-id <id> --element-id "<address_bar_id>" set-text "D:\Projects"
python winguictl.py action --window-id <id> press-key --key "{ENTER}"
```

### 确认操作

```powershell
# 点击保存/打开按钮
python winguictl.py uia-control --window-id <id> --element-id "1" invoke

# 点击取消按钮
python winguictl.py uia-control --window-id <id> --element-id "2" invoke

# 或使用快捷键
python winguictl.py action --window-id <id> press-key --key "{ENTER}"  # 确认
python winguictl.py action --window-id <id> press-key --key "{ESC}"    # 取消
```

## 完整示例

### 另存为新文件

```powershell
# 1. 等待对话框
python winguictl.py wait window "另存为" --class "#32770" --timeout 10

# 2. 获取对话框 ID
python winguictl.py window list
# 假设对话框 ID 为 123456

# 3. 导航到目标路径
python winguictl.py action --window-id 123456 hotkey --keys "{CTRL}" "{L}"
python winguictl.py action --window-id 123456 type --text "D:\Output{ENTER}"

# 4. 设置文件名
python winguictl.py uia-control --window-id 123456 --element-id "FileNameControlHost" set-text "export.txt"

# 5. 点击保存
python winguictl.py uia-control --window-id 123456 --element-id "1" invoke
```

### 打开文件

```powershell
# 1. 等待对话框
python winguictl.py wait window "打开" --class "#32770" --timeout 10

# 2. 获取对话框 ID
python winguictl.py window list
# 假设对话框 ID 为 789012

# 3. 导航到目标路径
python winguictl.py action --window-id 789012 hotkey --keys "{CTRL}" "{L}"
python winguictl.py action --window-id 789012 type --text "D:\Documents{ENTER}"

# 4. 选择文件（双击）
python winguictl.py find --window-id 789012 uia --text "report.docx" --control-type ListItem
python winguictl.py uia-control --window-id 789012 --element-id "<file_id>" double-click
```

## 注意事项

1. **automation_id 可能变化**: 不同 Windows 版本或应用程序自定义对话框时，automation_id 可能不同。优先使用 `snapshot` 确认。

2. **工具栏按钮**: 对话框工具栏（视图切换、返回上级等）通常是 `SplitButton` 或 `ToolBar`，应使用 `action click --element-id` 而非 `uia-control click`。

3. **等待对话框**: 使用 `wait window` 等待对话框出现。

4. **文件列表操作**: 文件列表是标准 `List` 控件，支持 `list-select`、`list-items` 等操作。

5. **处理覆盖确认**: 当文件已存在时，系统会弹出确认对话框，需要额外处理。

## 相关文档

| 文件 | 描述 |
|------|------|
| [dialog.md](./dialog.md) | 对话框定位与基本操作 |
| [navigation.md](./navigation.md) | 路径导航与地址栏操作 |
| [file-selection.md](./file-selection.md) | 文件选择与确认 |
| [save-dialog.md](./save-dialog.md) | 另存为对话框特有操作 |
