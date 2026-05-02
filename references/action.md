# Action Commands

Execute interaction operations.

## Note

Action commands rely on coordinates or image matching and should be used as a fallback when `control` / `uia-control` commands are not applicable. Prefer structured identifiers (`hwnd`, `automation_id`, `runtime_id`) via control commands for more reliable and precise element interaction.

## Click Coordinates

```powershell
# Click at window-relative coordinates (x,y)
python scripts\winguictl.py action --window-id <id> click --x 100 --y 200

# Preview click coordinates (without executing actual click)
python scripts\winguictl.py action --window-id <id> click --x 100 --y 200 --dry-run
```

## Click Image

```powershell
# Click the first matching image template
python scripts\winguictl.py action --window-id <id> click-image --image-path assets\button.png

# Preview image click target (showing match position and confidence)
python scripts\winguictl.py action --window-id <id> click-image --image-path assets\button.png --threshold 0.95 --dry-run
```

## Drag

```powershell
# Drag from (x1,y1) to (x2,y2), duration 800ms
python scripts\winguictl.py action --window-id <id> drag --x1 100 --y1 200 --x2 400 --y2 200 --duration-ms 800

# Preview drag path
python scripts\winguictl.py action --window-id <id> drag --x1 100 --y1 200 --x2 400 --y2 200 --dry-run
```

## Type Text

```powershell
# Type text at current focus position
python scripts\winguictl.py action --window-id <id> type --text "hello world"

# Preview text input
python scripts\winguictl.py action --window-id <id> type --text "hello world" --dry-run
```

## Press Key

```powershell
# Press a single key
python scripts\winguictl.py action --window-id <id> press-key --key enter

# Preview key press
python scripts\winguictl.py action --window-id <id> press-key --key enter --dry-run
```

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

## Subcommand Summary

| Subcommand | Description | Parameters |
|--------|------|------|
| `click` | Click coordinates | `--x`, `--y`, `--dry-run` |
| `click-image` | Click image | `--image-path`, `--threshold`, `--dry-run` |
| `drag` | Drag | `--x1`, `--y1`, `--x2`, `--y2`, `--duration-ms`, `--dry-run` |
| `type` | Type text | `--text`, `--dry-run` |
| `press-key` | Press key | `--key`, `--dry-run` |
| `hotkey` | Key chord | `--keys`, `--dry-run` |
| `clear-text` | Clear text | `--dry-run` |
