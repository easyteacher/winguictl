# winguictl

Windows desktop automation CLI tool built on pywinauto and pywin32.

## Features

- **Window Management** — List, focus, minimize, maximize, restore, close, move, and resize desktop windows
- **Structure Snapshots** — Capture HWND tree, UIA tree, or OCR text regions of any window
- **Element Finding** — Locate UI elements by text, UIA properties, OCR, or image matching
- **Interaction Actions** — Click, drag, type text, press keys, and trigger hotkeys
- **Control Operations** — Directly manipulate Win32 controls (checkbox, combobox, etc.) and UIA elements (scroll, expand/collapse, slider, etc.)
- **Screenshot Capture** — Capture full window or rectangular region screenshots

## Quick Start

```powershell
# List all visible windows
python scripts\winguictl.py window list

# Focus a window
python scripts\winguictl.py window --window-id <id> focus

# Take a UIA snapshot of a window
python scripts\winguictl.py snapshot --window-id <id> uia

# Click a UIA element
python scripts\winguictl.py uia-control --window-id <id> --element-id <elem_id> click

# Type text into a window
python scripts\winguictl.py action --window-id <id> type --text "Hello World"

# Take a screenshot
python scripts\winguictl.py screenshot --window-id <id> --output shot.png
```

## License

MIT
