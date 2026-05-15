# 路径导航与地址栏操作

## 地址栏操作

### 聚焦地址栏

```powershell
# 方法1：快捷键 Ctrl+L
python winguictl.py action --window-id <id> hotkey --keys "{CTRL}" "{L}"

# 方法2：查找地址栏控件
python winguictl.py find --window-id <id> uia --automation-id "Address Band Root"
```

### 输入路径

```powershell
# 方法1：快捷键 + 输入（推荐）
python winguictl.py action --window-id <id> hotkey --keys "{CTRL}" "{L}"
python winguictl.py action --window-id <id> type --text "D:\Projects{ENTER}"

# 方法2：直接设置地址栏文本
python winguictl.py uia-control --window-id <id> --element-id "<address_bar_id>" set-text "D:\Projects"
python winguictl.py action --window-id <id> press-key --key "{ENTER}"
```

## 快速导航

### 返回上级目录

```powershell
# 方法1：快捷键 Alt+Up（推荐）
python winguictl.py action --window-id <id> hotkey --keys "{ALT}" "{UP}"

# 方法2：工具栏"向上"按钮
python winguictl.py find --window-id <id> uia --text "向上" --control-type Button
python winguictl.py action --window-id <id> click --element-id <up_button_id>
```

### 返回上一步/前进

```powershell
# 后退
python winguictl.py action --window-id <id> hotkey --keys "{ALT}" "{LEFT}"

# 前进
python winguictl.py action --window-id <id> hotkey --keys "{ALT}" "{RIGHT}"
```

### 切换视图模式

```powershell
python winguictl.py find --window-id <id> uia --text "视图" --control-type SplitButton
python winguictl.py action --window-id <id> click --element-id <view_button_id>
```

## 导航窗格

### 点击快速访问项

```powershell
# 桌面
python winguictl.py find --window-id <id> uia --text "桌面" --control-type TreeItem
python winguictl.py uia-control --window-id <id> --element-id <desktop_id> select

# 下载
python winguictl.py find --window-id <id> uia --text "下载" --control-type TreeItem
python winguictl.py uia-control --window-id <id> --element-id <downloads_id> select

# 此电脑
python winguictl.py find --window-id <id> uia --text "此电脑" --control-type TreeItem
python winguictl.py uia-control --window-id <id> --element-id <this_pc_id> select
```

## 常用路径快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+L` | 聚焦地址栏 |
| `Alt+Up` | 返回上级目录 |
| `Alt+Left` | 后退 |
| `Alt+Right` | 前进 |
| `Ctrl+N` | 新建文件夹（部分对话框） |
| `F2` | 重命名选中项 |

## 示例：导航到指定路径

```powershell
# 完整流程：打开对话框 -> 导航到 D:\Projects

# 1. 聚焦对话框
python winguictl.py window --window-id <id> focus

# 2. 聚焦地址栏
python winguictl.py action --window-id <id> hotkey --keys "{CTRL}" "{L}"

# 3. 输入路径并确认
python winguictl.py action --window-id <id> type --text "D:\Projects{ENTER}"
```
