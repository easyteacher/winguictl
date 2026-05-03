# Coordinate Systems

Understanding the coordinate system used by winguictl commands.

## Coordinate Type Labels

Output uses explicit labels to distinguish coordinate types:

- `relative_rect` - Window-relative coordinates (origin at window's top-left corner)
- `absolute_rect` - Screen-absolute coordinates (origin at screen's top-left corner)

## Window-Relative Coordinates (`relative_rect`)

Most winguictl commands return **window-relative coordinates**, labeled as `relative_rect`.

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

### Commands Using `relative_rect`

| Command | Coordinate System |
|---------|------------------|
| `snapshot hwnd` | Window-relative (`relative_rect`) |
| `snapshot uia` | Window-relative (`relative_rect`) |
| `snapshot ocr` | Window-relative (`relative_rect`) |
| `find text` | Window-relative (`relative_rect`) |
| `find uia` | Window-relative (`relative_rect`) |
| `find ocr` | Window-relative (`relative_rect`) |
| `find image` | Window-relative (`relative_rect`) |

### Commands Using Screen-Absolute Coordinates (`absolute_rect`)

| Command | Coordinate System |
|---------|------------------|
| `window list` | Screen-absolute (`absolute_rect` field) |

### Using Coordinates with Action Commands

Window-relative coordinates can be used directly with `action click` commands:

```powershell
# Find a button
python scripts\winguictl.py find --window-id 12345 ocr "Submit"
# Output: - "Submit" [relative_rect=(100,200 80x30)]

# Click the button center
python scripts\winguictl.py action --window-id 12345 click --relative-x 140 --relative-y 215
```

No manual coordinate conversion is needed.
