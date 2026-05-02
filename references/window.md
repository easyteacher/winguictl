# Window Commands

Control window state and position.

## List Windows

```powershell
# List all visible windows, output includes window_id, bounds, pid, process, state(minimized/maximized/normal), foreground
# Child windows are shown indented under parent windows
python scripts\winguictl.py window list
```

Output is wrapped with content boundary markers:

```
--- WINGUICTL_CONTENT nonce=a1b2c3d4e5f6g7h8 ---
- "Window Title" [window_id="123456" bounds=(0,0 1920x1080) pid="1234" process="notepad.exe" state="maximized" foreground="true"]
  - "Child Window" [window_id="123457" bounds=(10,10 200x100) pid="1234" process="notepad.exe"]
--- END_WINGUICTL_CONTENT nonce=a1b2c3d4e5f6g7h8 ---
```

The `nonce` is a randomly generated hex string that must match between the start and end markers.

The window list displays parent-child hierarchical relationships, with child windows indented under their parent windows.

## Focus Window

```powershell
# Bring window to foreground and activate it
python scripts\winguictl.py window --window-id <window_id> focus
```

## Minimize Window

```powershell
python scripts\winguictl.py window --window-id <window_id> minimize
```

## Maximize Window

```powershell
python scripts\winguictl.py window --window-id <window_id> maximize
```

## Restore Window

```powershell
# Restore from minimized/maximized state to normal
python scripts\winguictl.py window --window-id <window_id> restore
```

## Close Window

```powershell
# Send WM_CLOSE message
python scripts\winguictl.py window --window-id <window_id> close
```

## Move Window

```powershell
# Move window to specified coordinates (keeping original size)
python scripts\winguictl.py window --window-id <window_id> move --x 100 --y 200
```

## Resize Window

```powershell
# Resize window while keeping original position
python scripts\winguictl.py window --window-id <window_id> resize --width 800 --height 600
```

## Subcommand Summary

| Subcommand | Description | Parameters |
|--------|------|------|
| `list` | List all visible windows | None |
| `focus` | Focus a window | `--window-id` |
| `minimize` | Minimize a window | `--window-id` |
| `maximize` | Maximize a window | `--window-id` |
| `restore` | Restore a window | `--window-id` |
| `close` | Close a window | `--window-id` |
| `move` | Move a window | `--window-id`, `--x`, `--y` |
| `resize` | Resize a window | `--window-id`, `--width`, `--height` |
