# Window Commands

Control window state and position.

## List Windows

```powershell
# List all visible windows, output includes window_id, bounds, pid, process, state(minimized/maximized/normal), foreground
# Child windows are shown indented under parent windows
python scripts\winguictl.py window list
```

Output example:
```
- "Window Title" [window_id="123456" bounds=(0,0 1920x1080) pid="1234" process="notepad.exe" state="maximized" foreground="true"]
  - "Child Window" [window_id="123457" bounds=(10,10 200x100) pid="1234" process="notepad.exe"]
```

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
