# 对话框定位与基本操作

## 定位对话框

### 方法1：通过窗口列表

```powershell
python winguictl.py window list
```

查找 `class_name="#32770"` 且标题为"打开"或"另存为"的窗口。

### 方法2：等待对话框出现

```powershell
python winguictl.py wait window "另存为" --class "#32770" --timeout 10
```

### 方法3：通过父窗口查找

对话框会作为父窗口的子窗口出现在窗口列表中（缩进显示）。

## 获取对话框结构

```powershell
python winguictl.py snapshot --window-id <dialog_id> uia
```

**注意**: Windows 10 及更早版本的 automation_id 可能不同。始终使用 `snapshot` 确认。

## 对话框基本操作

### 聚焦对话框

```powershell
python winguictl.py window --window-id <dialog_id> focus
```

### 关闭对话框

```powershell
# 方法1：点击取消按钮
python winguictl.py uia-control --window-id <id> --element-id "2" invoke

# 方法2：发送 ESC 键
python winguictl.py action --window-id <id> press-key --key "{ESC}"

# 方法3：关闭窗口
python winguictl.py window --window-id <id> close
```

### 移动对话框

```powershell
python winguictl.py window --window-id <id> move --x 100 --y 100
```

### 调整对话框大小

```powershell
python winguictl.py window --window-id <id> resize --width 900 --height 600
```

## 常见问题

### 对话框未找到

1. 确认对话框已弹出（可能需要等待）
2. 检查对话框是否被其他窗口遮挡
3. 使用 `--exact` 参数精确匹配标题

```powershell
python winguictl.py wait window "打开" --exact --class "#32770" --timeout 10
```

### automation_id 不匹配

不同应用程序可能自定义对话框，automation_id 可能不同。始终使用 `snapshot` 确认当前对话框的控件 ID。
