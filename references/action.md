# Action Commands

Execute interaction operations.

## ⚠️ SECURITY WARNING

### Risk Description

Action commands directly simulate mouse clicks, keyboard input, and other user interactions.

### Before using action commands

- Always use `--dry-run` to preview operations before execution
- Always verify the correct `window_id` before performing actions
- Read the complete [Security Guidelines](SECURITY.md) for detailed safety practices

## Note

### Prefer structured identifiers
- Action commands rely on coordinates or image matching and should be used as a fallback when `control` / `uia-control` commands are not applicable. Prefer structured identifiers (`hwnd`, `automation_id`, `runtime_id`) via control commands for more reliable and precise element interaction.

### Re-obtain the snapshot after each action operation
Action operations may change the UI state (such as window content, element status, or layout), so the previous snapshot may no longer be accurate. Always use `snapshot hwnd` or `snapshot uia` to get the latest UI state before performing subsequent operations.

## Output Information

Both `--dry-run` and actual execution output include the following information to help verify the operation:

### Window Information
- `window_id`: Window handle
- `window_title`: Window title text

### Coordinate Information
- `relative`: Coordinates relative to the window (x, y) - included when using `--relative-x/y`
- `absolute`: Absolute screen coordinates (x, y) - included when using `--absolute-x/y`

### Element at Point (UIA Information)
- `element_at_point`: UIA element information at the target coordinates, including:
  - `name`: Element name/text
  - `control_type`: Control type (e.g., "Button", "Edit")
  - `class_name`: Window class name
  - `automation_id`: Automation ID (if available)
  - `runtime_id`: Runtime ID (if available)

### Note

If UIA information is not available, this field will be `null`

### Control Information (Win32 Information)
- `control_info`: Win32 control information at the target coordinates, including:
  - `hwnd`: Control handle
  - `control_text`: Control text
  - `control_class`: Control class name
  - `control_type`: Inferred control type
  - `window_id`: Top-level window handle
  - `window_title`: Top-level window title

### Note

This field may be `null` in rare cases when no Win32 control is found at the coordinates

This information helps you verify:
1. The correct window is being targeted
2. The coordinates point to the expected UI element
3. Both UIA and Win32 perspectives of the target element
4. The element type matches your expectations

### Example Output

When clicking within a window:
```json
{
  "window_id": "25959812",
  "window_title": "计算器",
  "relative": {"x": 155, "y": 530},
  "element_at_point": {
    "name": "一",
    "control_type": "Button",
    "class_name": "Button",
    "automation_id": "num1Button",
    "runtime_id": "42-3349712-4-95"
  },
  "control_info": {
    "hwnd": "3349712",
    "control_text": "计算器",
    "control_class": "Windows.UI.Core.CoreWindow",
    "control_type": null,
    "window_id": "25959812",
    "window_title": "计算器"
  }
}
```

When clicking with absolute coordinates:
```json
{
  "absolute": {"x": 500, "y": 300},
  "window_id": "25959812",
  "window_title": "计算器",
  "relative": {"x": 155, "y": 530},
  "element_at_point": {...},
  "control_info": {...}
}
```

## Click Coordinates

```powershell
# Click at window-relative coordinates (requires --window-id)
python scripts\winguictl.py action --window-id <id> click --relative-x 100 --relative-y 200

# Click at absolute screen coordinates (no --window-id required)
python scripts\winguictl.py action click --absolute-x 500 --absolute-y 300

# Preview click coordinates (without executing actual click)
python scripts\winguictl.py action --window-id <id> click --relative-x 100 --relative-y 200 --dry-run
```

### Coordinate Parameters

| Parameter | Description |
|-----------|-------------|
| `--relative-x`, `--relative-y` | Window-relative coordinates (requires `--window-id`) |
| `--absolute-x`, `--absolute-y` | Absolute screen coordinates (mutually exclusive with relative) |

### Coordinate Validation

For relative coordinates, values must be within the window bounds:
- Valid range: `0 <= x < window_width` and `0 <= y < window_height`
- If coordinates are outside the bounds, an error will be raised with a message like:
  ```
  coordinates (9999, 9999) are outside window bounds (0-499, 0-599)
  ```

**Example**: For a window with bounds `(200, 100, 500x600)`:
- Valid relative coordinates: `(0, 0)` to `(499, 599)`
- Invalid relative coordinates: `(-1, 100)`, `(500, 300)`, `(100, 600)`

## Click Image

```powershell
# Click the first matching image template
python scripts\winguictl.py action --window-id <id> click-image --image-path assets\button.png

# Preview image click target (showing match position and confidence)
python scripts\winguictl.py action --window-id <id> click-image --image-path assets\button.png --threshold 0.95 --dry-run
```

## Drag

```powershell
# Drag from (x1,y1) to (x2,y2) using window-relative coordinates, duration 800ms
python scripts\winguictl.py action --window-id <id> drag --relative-x1 100 --relative-y1 200 --relative-x2 400 --relative-y2 200 --duration-ms 800

# Drag using absolute screen coordinates
python scripts\winguictl.py action drag --absolute-x1 100 --absolute-y1 200 --absolute-x2 400 --absolute-y2 200 --duration-ms 800

# Preview drag path
python scripts\winguictl.py action --window-id <id> drag --relative-x1 100 --relative-y1 200 --relative-x2 400 --relative-y2 200 --dry-run
```

### Coordinate Parameters

| Parameter | Description |
|-----------|-------------|
| `--relative-x1`, `--relative-y1` | Start point window-relative coordinates (requires `--window-id`) |
| `--relative-x2`, `--relative-y2` | End point window-relative coordinates (requires `--window-id`) |
| `--absolute-x1`, `--absolute-y1` | Start point absolute screen coordinates |
| `--absolute-x2`, `--absolute-y2` | End point absolute screen coordinates |

### Coordinate Validation

For relative coordinates, both start and end coordinates must be within the window bounds:
- Valid range: `0 <= x < window_width` and `0 <= y < window_height`
- If either coordinate is outside the bounds, an error will be raised:
  ```
  start coordinates (-1, 100) are outside window bounds (0-499, 0-599)
  end coordinates (9999, 9999) are outside window bounds (0-499, 0-599)
  ```

## Keyboard Operations

### Type Text

```powershell
# Type text at current focus position
python scripts\winguictl.py action --window-id <id> type --text "hello world"

# Type text with embedded special keys (e.g., multi-line text)
python scripts\winguictl.py action --window-id <id> type --text "first line{ENTER}second line{TAB}indented"

# Preview text input
python scripts\winguictl.py action --window-id <id> type --text "hello world" --dry-run
```

#### Execution Behavior

Before typing text, the command will:
1. Focus the target window (bring it to foreground)
2. Move the mouse cursor to the center of the window
3. Type the text using keyboard simulation

This ensures the window is active and the mouse is within the window bounds for proper text input.

### Press Key

```powershell
# Press a single key (must use pywinauto-style braces)
python scripts\winguictl.py action --window-id <id> press-key --key "{ENTER}"

# Preview key press
python scripts\winguictl.py action --window-id <id> press-key --key "{ENTER}" --dry-run
```

#### Execution Behavior

Before pressing the key, the command will:
1. Focus the target window (bring it to foreground)
2. Move the mouse cursor to the center of the window
3. Press and release the specified key

This ensures the window is active and the mouse is within the window bounds for proper key input.

### Hotkey

```powershell
# Press a key chord using list format (press in order, release in reverse order)
python scripts\winguictl.py action --window-id <id> hotkey --keys "{CTRL}" "{A}"

# Press a key chord using concatenated string format
python scripts\winguictl.py action --window-id <id> hotkey --keys "{CTRL}{SHIFT}{A}"

# Preview hotkey
python scripts\winguictl.py action --window-id <id> hotkey --keys "{CTRL}" "{A}" --dry-run
```

#### Execution Behavior

Before executing the hotkey, the command will:
1. Focus the target window (bring it to foreground)
2. Move the mouse cursor to the center of the window
3. Press all keys in order, then release in reverse order

This ensures the window is active and the mouse is within the window bounds for proper hotkey execution.

#### Common Hotkey Examples

| Operation | Command |
|------|------|
| Select all | `hotkey --keys "{CTRL}" "{A}"` or `hotkey --keys "{CTRL}{A}"` |
| Copy | `hotkey --keys "{CTRL}" "{C}"` or `hotkey --keys "{CTRL}{C}"` |
| Paste | `hotkey --keys "{CTRL}" "{V}"` or `hotkey --keys "{CTRL}{V}"` |
| Cut | `hotkey --keys "{CTRL}" "{X}"` or `hotkey --keys "{CTRL}{X}"` |
| Undo | `hotkey --keys "{CTRL}" "{Z}"` or `hotkey --keys "{CTRL}{Z}"` |
| Save | `hotkey --keys "{CTRL}" "{S}"` or `hotkey --keys "{CTRL}{S}"` |
| Find | `hotkey --keys "{CTRL}" "{F}"` or `hotkey --keys "{CTRL}{F}"` |
| Close window | `hotkey --keys "{ALT}" "{F4}"` or `hotkey --keys "{ALT}{F4}"` |

### Key Format Reference

All keyboard commands use pywinauto-style braced key names: `"{ENTER}"`, `"{TAB}"`, `"{ESC}"`, etc.

- `type`: Keys can be embedded within text: `"first line{ENTER}second line"`
- `press-key`: Single key only: `"{ENTER}"`
- `hotkey`: Multiple keys as list or concatenated string

#### Example

`"first line{ENTER}second line{ENTER}third line"` will type three lines of text.

#### Note

Text outside braces is typed as Unicode characters. Braces must be balanced — use `{{` and `}}` to type literal braces if needed.

#### Supported Key Names

| Key Category | Names |
|---------|------|
| Letter keys | `{a}` `{b}` `{c}` ... `{z}` |
| Number keys | `{0}` `{1}` `{2}` ... `{9}` |
| Function keys | `{f1}` `{f2}` ... `{f12}` |
| Control keys | `{backspace}` `{tab}` `{enter}` `{return}` `{shift}` `{ctrl}` `{control}` `{alt}` `{pause}` `{capslock}` `{esc}` `{escape}` `{space}` |
| Navigation keys | `{pageup}` `{pagedown}` `{end}` `{home}` `{left}` `{up}` `{right}` `{down}` |
| Edit keys | `{insert}` `{delete}` `{del}` |
| System keys | `{meta}` `{win}` `{cmd}` |

## Clear Text

```powershell
# Ctrl+A then Delete
python scripts\winguictl.py action --window-id <id> clear-text

# Preview clear operation
python scripts\winguictl.py action --window-id <id> clear-text --dry-run
```

### Execution Behavior

Before clearing text, the command will:
1. Focus the target window (bring it to foreground)
2. Move the mouse cursor to the center of the window
3. Execute Ctrl+A to select all, then Delete to clear

This ensures the window is active and the mouse is within the window bounds for proper text clearing.

## Scroll

Send mouse wheel scroll events at the current mouse position.

```powershell
# Scroll down 3 notches
python scripts\winguictl.py action --window-id <id> scroll --direction down --amount 3

# Scroll up 1 notch (default)
python scripts\winguictl.py action --window-id <id> scroll --direction up

# Scroll right 2 notches
python scripts\winguictl.py action --window-id <id> scroll --direction right --amount 2

# Preview scroll operation
python scripts\winguictl.py action --window-id <id> scroll --direction down --amount 3 --dry-run
```

### Execution Behavior

Before scrolling, the command will:
1. Focus the target window (bring it to foreground)
2. Move the mouse cursor to the center of the window
3. Send mouse wheel events in the specified direction

This ensures the window is active and the mouse is within the window bounds for proper scroll delivery.

### Scroll Parameters

| Parameter | Description |
|-----------|-------------|
| `--direction` | Scroll direction: `up`, `down`, `left`, `right` (required) |
| `--amount` | Number of notches to scroll (default: 1) |
| `--dry-run` | Preview mode, does not execute actual scroll |

### Scroll vs Keyboard Page Keys

Prefer `scroll` over `press-key` with `{PGDN}`/`{PGUP}` for scrolling:
- `scroll` sends mouse wheel events, which work in any scrollable area
- `{PGDN}`/`{PGUP}` only work when a text control has keyboard focus
- `scroll` supports horizontal scrolling (`left`/`right`)
- `scroll` allows fine-grained control via `--amount`

## Subcommand Summary

| Subcommand | Description | Parameters |
|--------|------|------|
| `click` | Click coordinates | `--relative-x`, `--relative-y` (with `--window-id`) OR `--absolute-x`, `--absolute-y`, `--dry-run` |
| `click-image` | Click image | `--image-path`, `--threshold`, `--dry-run` |
| `drag` | Drag | `--relative-x/y1/2` (with `--window-id`) OR `--absolute-x/y1/2`, `--duration-ms`, `--dry-run` |
| `type` | Type text | `--text`, `--dry-run` |
| `press-key` | Press key | `--key`, `--dry-run` |
| `hotkey` | Key chord | `--keys`, `--dry-run` |
| `clear-text` | Clear text | `--dry-run` |
| `scroll` | Mouse wheel scroll | `--direction`, `--amount`, `--dry-run` |
