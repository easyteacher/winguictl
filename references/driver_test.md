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

### Test Click Operations

```powershell
# Single click an element
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> click

# Double click an element
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> double-click

# Right click an element
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> right-click
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
# Select item
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> combo-select 0
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> combo-select "Option Text"

# Get all items
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

### Notepad Win32 Test

```powershell
# 1. Get Notepad window ID
python scripts\winguictl.py window list

# 2. Get edit box hwnd
python scripts\winguictl.py snapshot --window-id 533514 hwnd

# 3. Test input
python scripts\winguictl.py control --hwnd 402474 type-keys "Hello from type_keys!"
python scripts\winguictl.py control --hwnd 402474 send-chars " SEND_CHARS "
python scripts\winguictl.py control --hwnd 402474 send-keystrokes "{ENTER}send_keystrokes test{ENTER}"

# 4. Test click
python scripts\winguictl.py control --hwnd 402474 click
python scripts\winguictl.py control --hwnd 402474 double-click
python scripts\winguictl.py control --hwnd 402474 right-click
```

### Notepad UIA Test

```powershell
# 1. Get UIA elements
python scripts\winguictl.py snapshot --window-id 533514 uia

# 2. Test text operations
python scripts\winguictl.py uia-control --window-id 533514 --element-id "42-402474" set-text "UIA set-text test"
python scripts\winguictl.py uia-control --window-id 533514 --element-id "42-402474" type-keys "{ENTER}Type-keys test{ENTER}"
python scripts\winguictl.py uia-control --window-id 533514 --element-id "42-402474" get-text

# 3. Test scroll
python scripts\winguictl.py uia-control --window-id 533514 --element-id "42-402474" scroll down
python scripts\winguictl.py uia-control --window-id 533514 --element-id "42-402474" scroll up --amount line --count 5
```

### Calculator UIA Test

```powershell
# 1. Get Calculator window ID
python scripts\winguictl.py window list

# 2. Get button elements
python scripts\winguictl.py snapshot --window-id 4727732 uia

# 3. Test button clicks
python scripts\winguictl.py uia-control --window-id 4727732 --element-id num1Button click
python scripts\winguictl.py uia-control --window-id 4727732 --element-id num2Button double-click
python scripts\winguictl.py uia-control --window-id 4727732 --element-id num3Button right-click
python scripts\winguictl.py uia-control --window-id 4727732 --element-id plusButton click
python scripts\winguictl.py uia-control --window-id 4727732 --element-id num5Button click
python scripts\winguictl.py uia-control --window-id 4727732 --element-id equalButton click
```

---

## Test Checklist

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
| Single click | `click` | ☐ |
| Double click | `double-click` | ☐ |
| Right click | `right-click` | ☐ |
| Type keys | `type-keys` | ☐ |
| Set text | `set-text` | ☐ |
| Get text | `get-text` | ☐ |
| Set focus | `set-focus` | ☐ |
| Scroll | `scroll` | ☐ |
| Expand | `expand` | ☐ |
| Collapse | `collapse` | ☐ |
| Is expanded | `is-expanded` | ☐ |
| Toggle state | `toggle` | ☐ |
| Get toggle state | `get-toggle-state` | ☐ |
| Combobox select | `combo-select` | ☐ |
| Combobox items | `combo-items` | ☐ |
| Combobox selected index | `combo-selected-index` | ☐ |
| Combobox selected text | `combo-selected-text` | ☐ |
| Slider value | `slider-value` | ☐ |
| Set slider value | `slider-set` | ☐ |
| Slider minimum | `slider-min` | ☐ |
| Slider maximum | `slider-max` | ☐ |
