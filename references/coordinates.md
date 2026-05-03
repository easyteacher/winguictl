# Coordinate Systems

Understanding the coordinate system used by winguictl commands.

## Window-Relative Coordinates

Most winguictl commands return **window-relative coordinates**, not screen-absolute coordinates.

### What Are Window-Relative Coordinates?

Window-relative coordinates are measured from the top-left corner of the window (0, 0), not from the screen origin.

```
Screen coordinates:        Window-relative coordinates:
(0,0)─────────────►       (0,0)─────────────►
  │                         │
  │   ┌─────────┐           ┌─────────┐
  │   │ Window  │    vs     │ Window  │
  │   │ (591,150)│           │ (0,0)   │
  │   └─────────┘           └─────────┘
  ▼                         ▼
```

### Commands Using Window-Relative Coordinates

| Command | Coordinate System |
|---------|------------------|
| `snapshot hwnd` | Window-relative |
| `snapshot uia` | Window-relative |
| `snapshot ocr` | Window-relative |
| `find text` | Window-relative |
| `find uia` | Window-relative |
| `find ocr` | Window-relative |
| `find image` | Window-relative |

### Commands Using Screen-Absolute Coordinates

| Command | Coordinate System |
|---------|------------------|
| `window list` | Screen-absolute (`bounds` field) |

### Using Coordinates with Action Commands

Window-relative coordinates can be used directly with `action click` commands:

```powershell
# Find a button
python scripts\winguictl.py find --window-id 12345 ocr "Submit"
# Output: - "Submit" [rect=(100,200 80x30)]

# Click the button center
python scripts\winguictl.py action --window-id 12345 click --x 140 --y 215
```

No manual coordinate conversion is needed.
