# Control Commands

Directly control specific controls, including Win32 controls and UIA elements.

## ⚠️ SECURITY WARNING

### Risk Description

Control commands directly manipulate UI elements through their handles (HWND) or identifiers.

### Before using control commands

- Always verify the correct `hwnd`, `automation_id`, or `runtime_id` before performing operations
- Use `snapshot hwnd` or `snapshot uia` to identify the correct control identifiers
- Read the complete [Security Guidelines](SECURITY.md) for detailed safety practices

## Note

### Re-obtain the snapshot after each action operation
Action operations may change the UI state (such as window content, element status, or layout), so the previous snapshot may no longer be accurate. Always use `snapshot hwnd` or `snapshot uia` to get the latest UI state before performing subsequent operations.

## Win32 Control Operations

Operate on controls via their HWND handles. Use `snapshot hwnd` to obtain the control's `hwnd`.

### Click a control

```powershell
python scripts\winguictl.py control --hwnd <hwnd> click
```

### Get/Set Text

```powershell
python scripts\winguictl.py control --hwnd <hwnd> get-text

python scripts\winguictl.py control --hwnd <hwnd> set-text "New Text"
```

### Check/Uncheck

```powershell
python scripts\winguictl.py control --hwnd <hwnd> check

python scripts\winguictl.py control --hwnd <hwnd> uncheck
```

### Check/Uncheck by Click

```powershell
python scripts\winguictl.py control --hwnd <hwnd> check-by-click

python scripts\winguictl.py control --hwnd <hwnd> uncheck-by-click
```

### Combo/List Select

```powershell
python scripts\winguictl.py control --hwnd <hwnd> combo-select 0

python scripts\winguictl.py control --hwnd <hwnd> combo-select "Option 1"

python scripts\winguictl.py control --hwnd <hwnd> combo-items
```

### Win32 Control Subcommand Summary

| Subcommand | Description | Parameters |
|--------|------|------|
| `click` | Click a control | `--hwnd` |
| `double-click` | Double-click a control | `--hwnd` |
| `right-click` | Right-click a control | `--hwnd` |
| `get-text` | Get control text | `--hwnd` |
| `set-text` | Set control text | `--hwnd`, `text` (positional) |
| `set-focus` | Set focus to control | `--hwnd` |
| `type-keys` | Type keys to control | `--hwnd`, `keys` (positional) |
| `send-chars` | Send chars to inactive window | `--hwnd`, `chars` (positional) |
| `send-keystrokes` | Send keystrokes to inactive window | `--hwnd`, `keystrokes` (positional) |
| `check` | Check a checkbox | `--hwnd` |
| `uncheck` | Uncheck a checkbox | `--hwnd` |
| `check-by-click` | Check a checkbox by click (triggers event handlers) | `--hwnd` |
| `uncheck-by-click` | Uncheck a checkbox by click (triggers event handlers) | `--hwnd` |
| `is-checked` | Get checkbox state | `--hwnd` |
| `combo-select` | Select combobox item | `--hwnd`, `item` (positional: index or text), `--index` (treat item as 0-based index) |
| `combo-items` | Get combobox items | `--hwnd` |
| `combo-selected-index` | Get combobox selected index | `--hwnd` |
| `combo-selected-text` | Get combobox selected text | `--hwnd` |
| `listbox-select` | Select listbox item | `--hwnd`, `item` (positional: index or text) |
| `listbox-items` | Get listbox items | `--hwnd` |
| `listbox-selected-indices` | Get listbox selected indices | `--hwnd` |

## UIA Element Operations

Operate on elements via UIA automation_id or runtime_id. Use `snapshot uia` to obtain the element's `automation_id` or `runtime_id`.

```powershell
python scripts\winguictl.py uia-control --window-id <id> --element-id "Button1" click

python scripts\winguictl.py uia-control --window-id <id> --element-id "42-123456" click
```

### Get Text

```powershell
python scripts\winguictl.py uia-control --window-id <id> --element-id "Button1" get-text
```

### Set Value

```powershell
python scripts\winguictl.py uia-control --window-id <id> --element-id "Edit1" set-value "New Text"
```

### Expand/Collapse

```powershell
python scripts\winguictl.py uia-control --window-id <id> --element-id "Node1" expand

python scripts\winguictl.py uia-control --window-id <id> --element-id "Node1" collapse
```

### Scroll

```powershell
python scripts\winguictl.py uia-control --window-id <id> --element-id "List1" scroll down --amount page --count 3
```

### Type Keys

```powershell
python scripts\winguictl.py uia-control --window-id <id> --element-id "Edit1" type-keys "{ENTER}"
```

### Slider

```powershell
python scripts\winguictl.py uia-control --window-id <id> --element-id "Slider1" slider-set 50
```

### Select

```powershell
python scripts\winguictl.py uia-control --window-id <id> --element-id "Item1" select
```

### Is Selected

```powershell
python scripts\winguictl.py uia-control --window-id <id> --element-id "Item1" is-selected
```

### Get Toggle State

```powershell
python scripts\winguictl.py uia-control --window-id <id> --element-id "Check1" get-toggle-state
```

### Element ID Format

- **automation_id**: String identifier, e.g. `"Button1"`, `"Edit1"`
- **runtime_id**: Hyphen-separated numeric identifier, e.g. `"42-123456"`, `"42-123456-7"`

### Element ID Recommendation

**Prefer `runtime_id` over `automation_id`** when specifying `--element-id`:

- `runtime_id` is guaranteed to be unique within a desktop session
- `automation_id` may have duplicates, especially in Qt applications where multiple controls can share the same automation_id

Example:

#### Preferred: Use runtime_id

```powershell
python scripts\winguictl.py uia-control --window-id 12345 --element-id "42-3155764" click
```

#### Not Recommended: automation_id May Not Be Unique

```powershell
python scripts\winguictl.py uia-control --window-id 12345 --element-id "SubmitButton" click
```

### UIA Element Subcommand Summary

| Subcommand | Description | Parameters |
|--------|------|------|
| `click` | Click element | `--window-id`, `--element-id` |
| `double-click` | Double-click element | `--window-id`, `--element-id` |
| `right-click` | Right-click element | `--window-id`, `--element-id` |
| `get-text` | Get element text | `--window-id`, `--element-id` |
| `get-value` | Get element value | `--window-id`, `--element-id` |
| `set-value` | Set element value | `--window-id`, `--element-id`, `value` (positional) |
| `set-text` | Set element text | `--window-id`, `--element-id`, `text` (positional) |
| `set-focus` | Set focus to element | `--window-id`, `--element-id` |
| `invoke` | Invoke element (buttons) | `--window-id`, `--element-id` |
| `toggle` | Toggle element state | `--window-id`, `--element-id` |
| `get-toggle-state` | Get toggle state (0=off, 1=on, 2=indeterminate) | `--window-id`, `--element-id` |
| `select` | Select element | `--window-id`, `--element-id` |
| `is-selected` | Check if element is selected | `--window-id`, `--element-id` |
| `expand` | Expand node (TreeItem, ComboBox, MenuItem) | `--window-id`, `--element-id` |
| `collapse` | Collapse node (TreeItem, ComboBox, MenuItem) | `--window-id`, `--element-id` |
| `is-expanded` | Check if element is expanded | `--window-id`, `--element-id` |
| `scroll` | Scroll element | `--window-id`, `--element-id`, `direction`, `--amount`, `--count` |
| `combo-select` | Select combo box item | `--window-id`, `--element-id`, `item` (positional: index or text), `--index` (treat item as 0-based index) |
| `combo-items` | Get combo box items | `--window-id`, `--element-id` |
| `combo-selected-text` | Get selected text in combo box | `--window-id`, `--element-id` |
| `combo-selected-index` | Get selected index in combo box | `--window-id`, `--element-id` |
| `list-items` | Get list items | `--window-id`, `--element-id` |
| `list-select` | Select list item | `--window-id`, `--element-id`, `item` (positional: index or text) |
| `list-selected-items` | Get selected list items | `--window-id`, `--element-id` |
| `tab-select` | Select tab by index or text | `--window-id`, `--element-id`, `item` (positional) |
| `tab-selected` | Get selected tab index | `--window-id`, `--element-id` |
| `tab-count` | Get tab count | `--window-id`, `--element-id` |
| `slider-value` | Get slider value | `--window-id`, `--element-id` |
| `slider-set` | Set slider value | `--window-id`, `--element-id`, `value` (positional) |
| `slider-min` | Get slider minimum | `--window-id`, `--element-id` |
| `slider-max` | Get slider maximum | `--window-id`, `--element-id` |
| `window-close` | Close window (WindowPattern) | `--window-id`, `--element-id` |
| `window-minimize` | Minimize window (WindowPattern) | `--window-id`, `--element-id` |
| `window-maximize` | Maximize window (WindowPattern) | `--window-id`, `--element-id` |
| `window-restore` | Restore window to normal (WindowPattern) | `--window-id`, `--element-id` |
| `window-state` | Get window visual state (WindowPattern) | `--window-id`, `--element-id` |
| `transform-move` | Move element to screen coordinates (TransformPattern) | `--window-id`, `--element-id`, `--absolute-x`, `--absolute-y` |
| `transform-resize` | Resize element (TransformPattern) | `--window-id`, `--element-id`, `width` (positional), `height` (positional) |
| `transform-rotate` | Rotate element (TransformPattern) | `--window-id`, `--element-id`, `degrees` (positional) |
| `type-keys` | Type keys to element | `--window-id`, `--element-id`, `keys` (positional) |

### Scroll Parameters

| Parameter | Value |
|------|------|
| `--direction` | `up`, `down`, `left`, `right` |
| `--amount` | `line`, `page` |
| `--count` | Number of scrolls (default: 1) |

### UIA Actions

The `supported_actions` field in `snapshot uia` and `find uia` output shows which `uia-control` subcommands the element supports. Actions are derived from the element's UIA patterns:

| Action | Required Pattern | Description |
|--------|-----------------|-------------|
| `invoke` | InvokePattern | Invoke the element (buttons, menu items) |
| `get-value` | ValuePattern | Get element value |
| `set-value` | ValuePattern | Set element value |
| `set-text` | ValuePattern | Set element text |
| `get-text` | ValuePattern, TextPattern | Get element text |
| `toggle` | TogglePattern | Toggle element state |
| `get-toggle-state` | TogglePattern | Get toggle state (0=off, 1=on, 2=indeterminate) |
| `expand` | ExpandCollapsePattern | Expand node (ComboBox, TreeItem, MenuItem) |
| `collapse` | ExpandCollapsePattern | Collapse node |
| `is-expanded` | ExpandCollapsePattern | Check if element is expanded |
| `scroll` | ScrollPattern | Scroll element |
| `select` | SelectionItemPattern | Select element |
| `is-selected` | SelectionItemPattern | Check if element is selected |
| `combo-select` | SelectionItemPattern | Select combo box item |
| `list-select` | SelectionItemPattern | Select list item |
| `tab-select` | SelectionItemPattern | Select tab |
| `list-selected-items` | SelectionPattern | Get selected items in list |
| `slider-value` | RangeValuePattern | Get slider value |
| `slider-set` | RangeValuePattern | Set slider value |
| `slider-min` | RangeValuePattern | Get slider minimum |
| `slider-max` | RangeValuePattern | Get slider maximum |
| `window-close` | WindowPattern | Close the window |
| `window-minimize` | WindowPattern | Minimize the window |
| `window-maximize` | WindowPattern | Maximize the window |
| `window-restore` | WindowPattern | Restore window to normal size |
| `window-state` | WindowPattern | Get window visual state (normal/maximized/minimized) |
| `transform-move` | TransformPattern | Move element to screen coordinates (args: --absolute-x, --absolute-y) |
| `transform-resize` | TransformPattern | Resize element (args: width, height in pixels) |
| `transform-rotate` | TransformPattern | Rotate element (args: degrees) |

The following operations are always available regardless of patterns: `click`, `double-click`, `right-click`, `set-focus`, `type-keys`.
