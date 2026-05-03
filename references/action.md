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

## Type Text

```powershell
# Type text at current focus position
python scripts\winguictl.py action --window-id <id> type --text "hello world"

# Preview text input
python scripts\winguictl.py action --window-id <id> type --text "hello world" --dry-run
```

### Execution Behavior

Before typing text, the command will:
1. Focus the target window (bring it to foreground)
2. Move the mouse cursor to the center of the window
3. Type the text using keyboard simulation

This ensures the window is active and the mouse is within the window bounds for proper text input.

## Press Key

```powershell
# Press a single key
python scripts\winguictl.py action --window-id <id> press-key --key enter

# Preview key press
python scripts\winguictl.py action --window-id <id> press-key --key enter --dry-run
```

### Execution Behavior

Before pressing the key, the command will:
1. Focus the target window (bring it to foreground)
2. Move the mouse cursor to the center of the window
3. Press and release the specified key

This ensures the window is active and the mouse is within the window bounds for proper key input.

### Supported Key Names

| Key Category | Names |
|---------|------|
| Letter keys | `a` `b` `c` `d` `e` `f` `g` `h` `i` `j` `k` `l` `m` `n` `o` `p` `q` `r` `s` `t` `u` `v` `w` `x` `y` `z` |
| Number keys | `0` `1` `2` `3` `4` `5` `6` `7` `8` `9` |
| Function keys | `f1` `f2` `f3` `f4` `f5` `f6` `f7` `f8` `f9` `f10` `f11` `f12` |
| Control keys | `backspace` `tab` `enter` `return` `shift` `ctrl` `control` `alt` `pause` `capslock` `esc` `escape` `space` |
| Navigation keys | `pageup` `pagedown` `end` `home` `left` `up` `right` `down` |
| Edit keys | `insert` `delete` `del` |
| System keys | `meta` `win` `cmd` |

## Hotkey

```powershell
# Press a key chord (press in order, release in reverse order)
python scripts\winguictl.py action --window-id <id> hotkey --keys ctrl a

# Multiple key chords
python scripts\winguictl.py action --window-id <id> hotkey --keys ctrl shift s

# Preview hotkey
python scripts\winguictl.py action --window-id <id> hotkey --keys ctrl a --dry-run
```

### Execution Behavior

Before executing the hotkey, the command will:
1. Focus the target window (bring it to foreground)
2. Move the mouse cursor to the center of the window
3. Press all keys in order, then release in reverse order

This ensures the window is active and the mouse is within the window bounds for proper hotkey execution.

### Common Hotkey Examples

| Operation | Command |
|------|------|
| Select all | `hotkey --keys ctrl a` |
| Copy | `hotkey --keys ctrl c` |
| Paste | `hotkey --keys ctrl v` |
| Cut | `hotkey --keys ctrl x` |
| Undo | `hotkey --keys ctrl z` |
| Save | `hotkey --keys ctrl s` |
| Find | `hotkey --keys ctrl f` |
| Close window | `hotkey --keys alt f4` |

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
