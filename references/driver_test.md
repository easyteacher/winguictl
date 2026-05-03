# Driver Test Steps

This document describes how to test the Win32Driver and UIADriver functionality.

---

## Preparation

### Launch Test Applications

```powershell
# Launch Calculator
Start-Process calc

# Launch Notepad
Start-Process notepad
```

### Get Window IDs

```powershell
python scripts\winguictl.py window list
```

Output example:
```
- "Calculator" [window_id="4727732" bounds=(32,35 600x800) pid="35540" process="ApplicationFrameHost.exe"]
- "Untitled - Notepad" [window_id="533514" bounds=(78,78 894x805) pid="37836" process="Notepad.exe"]
```

---

## Window Management Tests

### List Windows

```powershell
python scripts\winguictl.py window list
```

### Focus Window

```powershell
python scripts\winguictl.py window --window-id <window_id> focus
```

### Close Window

```powershell
python scripts\winguictl.py window --window-id <window_id> close
```

### Minimize/Maximize/Restore Window

```powershell
python scripts\winguictl.py window --window-id <window_id> minimize
python scripts\winguictl.py window --window-id <window_id> maximize
python scripts\winguictl.py window --window-id <window_id> restore
```

### Move/Resize Window

```powershell
python scripts\winguictl.py window --window-id <window_id> move --x 100 --y 100
python scripts\winguictl.py window --window-id <window_id> resize --width 800 --height 600
```

---

## Action Tests

### Type Text

```powershell
python scripts\winguictl.py action --window-id <window_id> type --text "Hello World"
```

### Press Key

```powershell
python scripts\winguictl.py action --window-id <window_id> press-key --key Enter
python scripts\winguictl.py action --window-id <window_id> press-key --key Escape
```

### Hotkey

```powershell
python scripts\winguictl.py action --window-id <window_id> hotkey --keys Ctrl S
python scripts\winguictl.py action --window-id <window_id> hotkey --keys Ctrl A
```

### Click at Coordinates

```powershell
python scripts\winguictl.py action --window-id <window_id> click --x 100 --y 100
```

### Drag

```powershell
python scripts\winguictl.py action --window-id <window_id> drag --x1 100 --y1 100 --x2 200 --y2 200
```

### Clear Text

```powershell
python scripts\winguictl.py action --window-id <window_id> clear-text
```

---

## Snapshot Tests

### UIA Snapshot

```powershell
python scripts\winguictl.py snapshot --window-id <window_id> uia
```

### HWND Snapshot

```powershell
python scripts\winguictl.py snapshot --window-id <window_id> hwnd
```

### OCR Snapshot

```powershell
python scripts\winguictl.py snapshot --window-id <window_id> ocr
```

---

## Find Tests

### Find by Text

```powershell
python scripts\winguictl.py find --window-id <window_id> text "Button Text"
python scripts\winguictl.py find --window-id <window_id> text "Button Text" --exact
```

### Find UIA Elements

```powershell
# Find by text
python scripts\winguictl.py find --window-id <window_id> uia --text "One"

# Find by control type
python scripts\winguictl.py find --window-id <window_id> uia --control-type Button
python scripts\winguictl.py find --window-id <window_id> uia --control-type ComboBox
python scripts\winguictl.py find --window-id <window_id> uia --control-type Edit
```

### Find by OCR

```powershell
python scripts\winguictl.py find --window-id <window_id> ocr "Text"
```

### Find by Image

```powershell
python scripts\winguictl.py find --window-id <window_id> image --image-path template.png
```

---

## Screenshot Tests

```powershell
# Full window screenshot
python scripts\winguictl.py screenshot --window-id <window_id> --output screenshot.png

# Region screenshot
python scripts\winguictl.py screenshot --window-id <window_id> --output region.png --x 100 --y 100 --width 200 --height 200
```

---

## Win32Driver Tests

### Get Control hwnd

```powershell
python scripts\winguictl.py snapshot --window-id <window_id> hwnd
```

Notepad output example:
```
- "" [control_type="Edit" class="RichEditD2DPT" hwnd="402474" visible=true enabled=true control_id="0"]
```

### Test Click Operations

```powershell
# Single click a control
python scripts\winguictl.py control --hwnd <hwnd> click

# Double click a control
python scripts\winguictl.py control --hwnd <hwnd> double-click

# Right click a control
python scripts\winguictl.py control --hwnd <hwnd> right-click
```

### Test Keyboard Input

```powershell
# Type text
python scripts\winguictl.py control --hwnd <hwnd> type-keys "Hello World"

# Type special keys
python scripts\winguictl.py control --hwnd <hwnd> type-keys "{ENTER}"
python scripts\winguictl.py control --hwnd <hwnd> type-keys "{CTRL}a{CTRL}{DELETE}"
```

### Test Silent Input (Inactive Window)

```powershell
# Send characters to an inactive window
python scripts\winguictl.py control --hwnd <hwnd> send-chars "Hello"

# Send keystrokes to an inactive window
python scripts\winguictl.py control --hwnd <hwnd> send-keystrokes "{ENTER}New line{ENTER}"
```

### Test Text Operations

```powershell
# Set text
python scripts\winguictl.py control --hwnd <hwnd> set-text "Test text"

# Get text
python scripts\winguictl.py control --hwnd <hwnd> get-text
```

### Test Checkbox

```powershell
# Check
python scripts\winguictl.py control --hwnd <hwnd> check

# Uncheck
python scripts\winguictl.py control --hwnd <hwnd> uncheck

# Get state
python scripts\winguictl.py control --hwnd <hwnd> is-checked
```

### Test Combobox

```powershell
# Select item (by index or text)
python scripts\winguictl.py control --hwnd <hwnd> combo-select 0
python scripts\winguictl.py control --hwnd <hwnd> combo-select "Option Text"

# Get all items
python scripts\winguictl.py control --hwnd <hwnd> combo-items

# Get selected index
python scripts\winguictl.py control --hwnd <hwnd> combo-selected-index

# Get selected text
python scripts\winguictl.py control --hwnd <hwnd> combo-selected-text
```

---

## UIADriver Tests

### Get Element IDs

```powershell
python scripts\winguictl.py snapshot --window-id <window_id> uia
```

Calculator output example:
```
- "One" [control_type="Button" class="Button" automation_id="num1Button" enabled=true rect=(110,710 64x56) runtime_id="42-795520-4-94"]
- "Two" [control_type="Button" class="Button" automation_id="num2Button" enabled=true rect=(176,710 64x56) runtime_id="42-795520-4-95"]
```

Notepad text editor:
```
- "Text Editor" [control_type="Document" class="RichEditD2DPT" enabled=true rect=(582,199 882x692) runtime_id="42-402474"]
```

#### Element ID Format

The `--element-id` parameter accepts:
- **automation_id**: e.g., `num1Button`, `plusButton`, `equalButton`
- **runtime_id**: e.g., `42-795520-4-94`

```powershell
# Using automation_id
python scripts\winguictl.py uia-control --window-id <window_id> --element-id num1Button click

# Using runtime_id
python scripts\winguictl.py uia-control --window-id <window_id> --element-id "42-795520-4-94" click
```

### Test Click Operations

```powershell
# Single click an element
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> click

# Double click an element
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> double-click

# Right click an element
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> right-click

# Invoke (for buttons, menu items)
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> invoke
```

### Test Keyboard Input

```powershell
# Type text
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> type-keys "Hello World"

# Type special keys
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> type-keys "{ENTER}"
```

### Test Text Operations

```powershell
# Set text
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> set-text "Test text"

# Get text
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> get-text
```

### Test Scroll Operations

```powershell
# Scroll down one page
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> scroll down

# Scroll up one page
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> scroll up

# Scroll down 5 lines
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> scroll down --amount line --count 5

# Scroll left/right
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> scroll left
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> scroll right
```

### Test Expand/Collapse

```powershell
# Expand
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> expand

# Collapse
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> collapse

# Check if expanded
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> is-expanded
```

### Test Toggle Operations

```powershell
# Toggle state
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> toggle

# Get toggle state
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> get-toggle-state
```

### Test Combobox

```powershell
# Select item (by index or text)
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> combo-select 0
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> combo-select "Option Text"

# Get all items (expands combobox automatically)
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> combo-items

# Get selected text
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> combo-selected-text

# Get selected index
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> combo-selected-index
```

### Test Slider

```powershell
# Get slider value
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> slider-value

# Set slider value
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> slider-set 50.0

# Get min/max values
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> slider-min
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> slider-max
```

---

## Complete Test Examples

### Notepad Complete Test

```powershell
# 1. Launch Notepad
Start-Process notepad

# 2. Get Notepad window ID
python scripts\winguictl.py window list
# Output: "无标题 - Notepad" [window_id="4918678" ...]

# 3. Focus window
python scripts\winguictl.py window --window-id 4918678 focus

# 4. Type text
python scripts\winguictl.py action --window-id 4918678 type --text "Hello, this is a test from winguictl!"

# 5. Get UIA snapshot
python scripts\winguictl.py snapshot --window-id 4918678 uia

# 6. Get HWND snapshot
python scripts\winguictl.py snapshot --window-id 4918678 hwnd

# 7. Open Save dialog
python scripts\winguictl.py action --window-id 4918678 hotkey --keys Ctrl S

# 8. Get Save dialog window ID
python scripts\winguictl.py window list
# Output: "另存为" [window_id="3745666" ...]

# 9. Find ComboBox elements
python scripts\winguictl.py find --window-id 3745666 uia --control-type ComboBox

# 10. Test encoding ComboBox
python scripts\winguictl.py uia-control --window-id 3745666 --element-id "42-1189248" combo-items
python scripts\winguictl.py uia-control --window-id 3745666 --element-id "42-1189248" combo-selected-text
python scripts\winguictl.py uia-control --window-id 3745666 --element-id "42-1189248" combo-select "GB18030"

# 11. Close Save dialog
python scripts\winguictl.py action --window-id 3745666 press-key --key Escape

# 12. Close Notepad
python scripts\winguictl.py window --window-id 4918678 close
```

### Calculator UIA Test

```powershell
# 1. Launch Calculator
Start-Process calc

# 2. Get Calculator window ID
python scripts\winguictl.py window list
# Output: "计算器" [window_id="12133502" ...]

# 3. Get UIA snapshot
python scripts\winguictl.py snapshot --window-id 12133502 uia

# 4. Find number buttons
python scripts\winguictl.py find --window-id 12133502 uia --text "一"
python scripts\winguictl.py find --window-id 12133502 uia --text "加"
python scripts\winguictl.py find --window-id 12133502 uia --text "等于"

# 5. Test calculation: 1 + 2 = 3
python scripts\winguictl.py uia-control --window-id 12133502 --element-id num1Button click
python scripts\winguictl.py uia-control --window-id 12133502 --element-id plusButton click
python scripts\winguictl.py uia-control --window-id 12133502 --element-id num2Button click
python scripts\winguictl.py uia-control --window-id 12133502 --element-id equalButton click

# 6. Take screenshot
python scripts\winguictl.py screenshot --window-id 12133502 --output calculator_result.png

# 7. Close Calculator
python scripts\winguictl.py window --window-id 12133502 close
```

---

## Known Issues and Notes

### Element ID Resolution

- **automation_id** is preferred for stable element identification
- **runtime_id** is more reliable but changes between sessions
- If `automation_id` lookup fails, try using `runtime_id` from snapshot output

### ComboBox Operations

- `combo-items` automatically expands the ComboBox to retrieve items
- For custom ComboBox controls (like file type selector in Save dialog), items may not be directly accessible
- Standard Win32 ComboBox controls work best with `combo-items` and `combo-selected-index`

### Window Close

- `window close` may fail if the application shows a confirmation dialog
- Use `action hotkey --keys Alt F4` as an alternative
- For force close, use PowerShell: `Stop-Process -Name Notepad -Force`

### Notepad Save Dialog

The Save dialog contains multiple ComboBox types:
- **File name ComboBox**: Custom control (`AppControlHost`), limited functionality
- **File type ComboBox**: Custom control (`AppControlHost`), limited functionality
- **Encoding ComboBox**: Standard Win32 ComboBox, full functionality

---

## Test Checklist

### Window Management

| Feature | Command | Status |
|------|------|------|
| List windows | `window list` | ☑ |
| Focus window | `window --window-id <id> focus` | ☑ |
| Close window | `window --window-id <id> close` | ☑ |
| Minimize window | `window --window-id <id> minimize` | ☐ |
| Maximize window | `window --window-id <id> maximize` | ☐ |
| Restore window | `window --window-id <id> restore` | ☐ |
| Move window | `window --window-id <id> move --x --y` | ☐ |
| Resize window | `window --window-id <id> resize --width --height` | ☐ |

### Action Operations

| Feature | Command | Status |
|------|------|------|
| Type text | `action --window-id <id> type --text` | ☑ |
| Press key | `action --window-id <id> press-key --key` | ☑ |
| Hotkey | `action --window-id <id> hotkey --keys` | ☑ |
| Click | `action --window-id <id> click --x --y` | ☐ |
| Click image | `action --window-id <id> click-image --image-path` | ☑ |
| Drag | `action --window-id <id> drag --x1 --y1 --x2 --y2` | ☐ |
| Clear text | `action --window-id <id> clear-text` | ☐ |

### Snapshot Operations

| Feature | Command | Status |
|------|------|------|
| UIA snapshot | `snapshot --window-id <id> uia` | ☑ |
| HWND snapshot | `snapshot --window-id <id> hwnd` | ☑ |
| OCR snapshot | `snapshot --window-id <id> ocr` | ☐ |

### Find Operations

| Feature | Command | Status |
|------|------|------|
| Find by text | `find --window-id <id> text` | ☐ |
| Find UIA by text | `find --window-id <id> uia --text` | ☑ |
| Find UIA by control type | `find --window-id <id> uia --control-type` | ☑ |
| Find by OCR | `find --window-id <id> ocr` | ☐ |
| Find by image | `find --window-id <id> image` | ☑ |

### Screenshot

| Feature | Command | Status |
|------|------|------|
| Full window | `screenshot --window-id <id> --output` | ☑ |
| Region | `screenshot --window-id <id> --x --y --width --height` | ☑ |

### Win32Driver

| Feature | Command | Status |
|------|------|------|
| Single click | `click` | ☐ |
| Double click | `double-click` | ☐ |
| Right click | `right-click` | ☐ |
| Type keys | `type-keys` | ☐ |
| Send characters | `send-chars` | ☐ |
| Send keystrokes | `send-keystrokes` | ☐ |
| Set text | `set-text` | ☐ |
| Get text | `get-text` | ☐ |
| Set focus | `set-focus` | ☐ |
| Checkbox check | `check` | ☐ |
| Checkbox uncheck | `uncheck` | ☐ |
| Checkbox state | `is-checked` | ☐ |
| Combobox select | `combo-select` | ☐ |
| Combobox items | `combo-items` | ☐ |
| Combobox selected index | `combo-selected-index` | ☐ |
| Combobox selected text | `combo-selected-text` | ☐ |

### UIADriver

| Feature | Command | Status |
|------|------|------|
| Single click | `click` | ☑ |
| Double click | `double-click` | ☐ |
| Right click | `right-click` | ☐ |
| Invoke | `invoke` | ☐ |
| Type keys | `type-keys` | ☐ |
| Set text | `set-text` | ☐ |
| Get text | `get-text` | ☐ |
| Set focus | `set-focus` | ☐ |
| Scroll | `scroll` | ☐ |
| Expand | `expand` | ☑ |
| Collapse | `collapse` | ☐ |
| Is expanded | `is-expanded` | ☐ |
| Toggle state | `toggle` | ☐ |
| Get toggle state | `get-toggle-state` | ☐ |
| Combobox select | `combo-select` | ☑ |
| Combobox items | `combo-items` | ☑ |
| Combobox selected index | `combo-selected-index` | ☑ |
| Combobox selected text | `combo-selected-text` | ☑ |
| Slider value | `slider-value` | ☐ |
| Set slider value | `slider-set` | ☐ |
| Slider minimum | `slider-min` | ☐ |
| Slider maximum | `slider-max` | ☐ |
