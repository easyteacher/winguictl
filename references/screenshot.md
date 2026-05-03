# Screenshot Commands

Capture window screenshots.

## Warning

Screenshots capture all visible content in the target window, which may include sensitive information. Close or hide sensitive applications (password managers, messaging apps, etc.) before taking screenshots.

## Take Screenshot

```powershell
# Capture the entire window and save as PNG
python scripts\winguictl.py screenshot --window-id <id> --output artifacts\shot.png

# Save as BMP
python scripts\winguictl.py screenshot --window-id <id> --output artifacts\shot.bmp

# Capture a specific rectangular region within the window
python scripts\winguictl.py screenshot --window-id <id> --output artifacts\region.png --x 100 --y 50 --width 300 --height 200

# Preview screenshot output path (without executing actual screenshot)
python scripts\winguictl.py screenshot --window-id <id> --output artifacts\shot.png --dry-run
```

## Output Examples

Successful screenshot:
```json
{"ok": true, "code": "OK", "message": "screenshot executed", "data": {"window_id": "123456", "output": "artifacts\\shot.png"}}
```

Rectangular region screenshot:
```json
{"ok": true, "code": "OK", "message": "screenshot executed", "data": {"window_id": "123456", "output": "artifacts\\region.png", "rect": {"x": 100, "y": 50, "width": 300, "height": 200}}}
```

Preview mode (--dry-run):
```json
{"ok": true, "code": "DRY_RUN", "message": "screenshot preview generated", "data": {"window_id": "123456", "output": "artifacts\\shot.png"}}
```

## Parameter Description

| Parameter | Description |
|------|------|
| `--window-id` | Window ID (required) |
| `--output` | Output file path, supports `.png` or `.bmp` format (required) |
| `--x` | Left boundary of the rectangular region, relative to window top-left (optional) |
| `--y` | Top boundary of the rectangular region, relative to window top-left (optional) |
| `--width` | Width of the rectangular region (optional) |
| `--height` | Height of the rectangular region (optional) |
| `--dry-run` | Preview mode, does not execute actual screenshot |

## Rectangular Region Screenshot

When all four parameters `--x`, `--y`, `--width`, `--height` are specified, only the specified rectangular region within the window is captured. All four parameters must be provided together, otherwise the entire window is captured.

The coordinate origin is the window's top-left corner (excluding title bar border).

## Dependencies

- Requires `Pillow`: `pip install Pillow`
