# Control Commands

Directly control specific controls, including Win32 controls and UIA elements.

## Win32 Control Operations

Operate on controls via their HWND handles. Use `snapshot hwnd` to obtain the control's `hwnd`.

```powershell
# Click a control
python scripts\winguictl.py control --hwnd <hwnd> click

# Get control text
python scripts\winguictl.py control --hwnd <hwnd> get-text

# Set control text
python scripts\winguictl.py control --hwnd <hwnd> set-text --text "New Text"

# Check/uncheck a checkbox or radio button
python scripts\winguictl.py control --hwnd <hwnd> check
python scripts\winguictl.py control --hwnd <hwnd> uncheck

# Select an item in a combobox or listbox
python scripts\winguictl.py control --hwnd <hwnd> select --index 0
python scripts\winguictl.py control --hwnd <hwnd> select --text "Option 1"

# Get the number of items in a combobox or listbox
python scripts\winguictl.py control --hwnd <hwnd> count
```

### Win32 Control Subcommand Summary

| Subcommand | Description | Parameters |
|--------|------|------|
| `click` | Click a control | `--hwnd` |
| `get-text` | Get control text | `--hwnd` |
| `set-text` | Set control text | `--hwnd`, `--text` |
| `check` | Check a checkbox/radio | `--hwnd` |
| `uncheck` | Uncheck a checkbox/radio | `--hwnd` |
| `select` | Select an item | `--hwnd`, `--index` or `--text` |
| `count` | Get item count | `--hwnd` |

## UIA Element Operations

Operate on elements via UIA automation_id or runtime_id. Use `snapshot uia` to obtain the element's `automation_id` or `runtime_id`.

```powershell
# Click a UIA element (using automation_id)
python scripts\winguictl.py uia-control --window-id <id> --element-id "Button1" click

# Click a UIA element (using runtime_id)
python scripts\winguictl.py uia-control --window-id <id> --element-id "42-123456" click

# Get element text
python scripts\winguictl.py uia-control --window-id <id> --element-id "Button1" get-text

# Set element value (for editable controls)
python scripts\winguictl.py uia-control --window-id <id> --element-id "Edit1" set-value --value "New Text"

# Expand/collapse a node (for TreeItem, ComboBox, etc.)
python scripts\winguictl.py uia-control --window-id <id> --element-id "Node1" expand
python scripts\winguictl.py uia-control --window-id <id> --element-id "Node1" collapse

# Scroll a scrollable element
python scripts\winguictl.py uia-control --window-id <id> --element-id "List1" scroll --direction down --amount small

# Set slider value
python scripts\winguictl.py uia-control --window-id <id> --element-id "Slider1" set-slider-value --value 50

# Select a UIA element
python scripts\winguictl.py uia-control --window-id <id> --element-id "Item1" select

# Get toggle state (for CheckBox, etc.)
python scripts\winguictl.py uia-control --window-id <id> --element-id "Check1" toggle

# Get element property value
python scripts\winguictl.py uia-control --window-id <id> --element-id "Button1" get-property --property Name
```

### Element ID Format

- **automation_id**: String identifier, e.g. `"Button1"`, `"Edit1"`
- **runtime_id**: Hyphen-separated numeric identifier, e.g. `"42-123456"`, `"42-123456-7"`

### UIA Element Subcommand Summary

| Subcommand | Description | Parameters |
|--------|------|------|
| `click` | Click element | `--window-id`, `--element-id` |
| `get-text` | Get element text | `--window-id`, `--element-id` |
| `set-value` | Set element value | `--window-id`, `--element-id`, `--value` |
| `expand` | Expand node | `--window-id`, `--element-id` |
| `collapse` | Collapse node | `--window-id`, `--element-id` |
| `scroll` | Scroll element | `--window-id`, `--element-id`, `--direction`, `--amount` |
| `set-slider-value` | Set slider value | `--window-id`, `--element-id`, `--value` |
| `select` | Select element | `--window-id`, `--element-id` |
| `toggle` | Toggle element state | `--window-id`, `--element-id` |
| `get-property` | Get element property | `--window-id`, `--element-id`, `--property` |

### Scroll Parameters

| Parameter | Value |
|------|------|
| `--direction` | `up`, `down`, `left`, `right` |
| `--amount` | `small` (one line), `large` (one page) |

### Common Property Names

| Property | Description |
|------|------|
| `Name` | Element name |
| `ClassName` | Class name |
| `ControlType` | Control type |
| `IsEnabled` | Whether enabled |
| `IsOffscreen` | Whether off-screen |
| `BoundingRectangle` | Bounding rectangle |
| `ProcessId` | Process ID |
| `IsKeyboardFocusable` | Whether keyboard focusable |
| `HasKeyboardFocus` | Whether has keyboard focus |
