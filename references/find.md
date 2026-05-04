# Find Commands

Find elements in a window.

For output format details, see [Output Format](output-format.md).
For coordinate system details, see [Coordinate Systems](coordinates.md).

## Output Fields

All find commands return element information with the following fields:

- `text` - Element text/content
- `relative_rect` - Element rectangle (window-relative coordinates)
- `control_type` - Control type (UIA/HWND modes)
- `class` - Window class name (UIA/HWND modes)
- `hwnd` - Control handle (HWND mode)
- `automation_id` - Automation ID (UIA mode)
- `runtime_id` - Runtime ID (UIA mode)
- `supported_actions` - Supported uia-control actions (UIA mode)
- `confidence` - Match confidence score (0-1)

## Find Text

### Fuzzy Match

```powershell
python scripts\winguictl.py find --window-id <id> text "Submit"
```

### Exact Match

```powershell
python scripts\winguictl.py find --window-id <id> text "Submit" --exact
```

### Example Output

```
--- WINGUICTL_CONTENT nonce=a1b2c3d4e5f6a7b8 ---
- "Submit" [control_type="Button" class="Button" confidence=0.95 relative_rect=(150,200 80x30)]
--- END_WINGUICTL_CONTENT nonce=a1b2c3d4e5f6a7b8 ---
```

## Find UIA Controls

### Find by Text

```powershell
python scripts\winguictl.py find --window-id <id> uia --text "Submit"
```

### Exact Text Match

```powershell
python scripts\winguictl.py find --window-id <id> uia --text "Submit" --exact
```

### Find by Control Type

```powershell
python scripts\winguictl.py find --window-id <id> uia --control-type Button
```

### Find by Supported Action

```powershell
python scripts\winguictl.py find --window-id <id> uia --action set-text
```

### Combined Conditions

```powershell
python scripts\winguictl.py find --window-id <id> uia --text "OK" --control-type Button

python scripts\winguictl.py find --window-id <id> uia --control-type Edit --action set-text
```

### UIA Control Types

The `--control-type` parameter accepts standard UIA (UI Automation) control types, with case-insensitive fuzzy matching:

| Control Type | Description |
|----------|------|
| `Button` | Button |
| `Calendar` | Calendar |
| `CheckBox` | Checkbox |
| `ComboBox` | Combo box / Dropdown |
| `Edit` | Text input field |
| `Hyperlink` | Hyperlink |
| `Image` | Image |
| `ListItem` | List item |
| `List` | List |
| `Menu` | Menu |
| `MenuBar` | Menu bar |
| `MenuItem` | Menu item |
| `ProgressBar` | Progress bar |
| `RadioButton` | Radio button |
| `ScrollBar` | Scroll bar |
| `Slider` | Slider |
| `Spinner` | Numeric spinner |
| `StatusBar` | Status bar |
| `Tab` | Tab control |
| `TabItem` | Tab item |
| `Text` | Static text |
| `ToolBar` | Toolbar |
| `ToolTip` | Tooltip |
| `Tree` | Tree view |
| `TreeItem` | Tree item |
| `Custom` | Custom control |
| `DataGrid` | Data grid |
| `DataItem` | Data item |
| `Document` | Document |
| `Group` | Group |
| `Header` | Header |
| `HeaderItem` | Header item |
| `Pane` | Pane |
| `Separator` | Separator |
| `Table` | Table |
| `TitleBar` | Title bar |
| `Window` | Window |

### Control Type Aliases

Some UIA control types have aliases. When searching by `--control-type`, matching results from both the original type and its aliases will be returned:

| Search Type | Also Matches | Reason |
|------------|-------------|--------|
| `Edit` | `Document` | Windows 11 Notepad and WinUI3 text editors use `Document` instead of `Edit` |

## Find OCR Text

### Fuzzy Match

```powershell
python scripts\winguictl.py find --window-id <id> ocr "Confirm"
```

### With Confidence Threshold

```powershell
python scripts\winguictl.py find --window-id <id> ocr "Confirm" --confidence-threshold 0.7
```

### Example Output

```
--- WINGUICTL_CONTENT nonce=a1b2c3d4e5f6a7b8 ---
- "Confirm" [confidence=0.90 relative_rect=(46,525 80x20)]
- "Confirmation" [confidence=0.90 relative_rect=(46,550 100x20)]
--- END_WINGUICTL_CONTENT nonce=a1b2c3d4e5f6a7b8 ---
```

### Note

- The `--confidence-threshold` parameter is accepted but currently ignored. The wx_ocr library does not provide confidence scores, so all matches are assigned a fixed confidence of 0.9. If a non-zero threshold is specified, a warning will be logged.
- OCR coordinates are window-relative because the OCR engine processes a cropped window screenshot. These coordinates can be used directly with `action click` commands.

### Warning

OCR-based text finding captures visible text from the window, which may include sensitive information. See the warning in [Snapshot Commands](snapshot.md#ocr) regarding sensitive data.

## Find Image

### Basic Usage

```powershell
python scripts\winguictl.py find --window-id <id> image --image-path assets\button.png
```

### Custom Match Threshold

```powershell
python scripts\winguictl.py find --window-id <id> image --image-path assets\button.png --threshold 0.95
```

### Custom Overlap Threshold

```powershell
python scripts\winguictl.py find --window-id <id> image --image-path assets\button.png --overlap-threshold 0.3
```

### Example Output

```
--- WINGUICTL_CONTENT nonce=a1b2c3d4e5f6a7b8 ---
- "button.png" [confidence=0.95 relative_rect=(100,150 120x40)]
- "button.png" [confidence=0.92 relative_rect=(250,150 120x40)]
--- END_WINGUICTL_CONTENT nonce=a1b2c3d4e5f6a7b8 ---
```

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--image-path` | (required) | Path to the template image file |
| `--threshold` | 0.9 | Match confidence threshold (0-1). Higher values require closer matches. |
| `--overlap-threshold` | 0.5 | IoU threshold for non-maximum suppression (0-1). Higher values allow more overlapping matches. Use lower values (e.g., 0.3) to get fewer overlapping results, or higher values (e.g., 0.7) to allow more overlapping matches. |

### Overlap Threshold Explanation

The `--overlap-threshold` parameter controls how the deduplication (non-maximum suppression) works:

- **Lower values (e.g., 0.3)**: More aggressive deduplication. Matches with >30% overlap will be suppressed. Results in fewer, more distinct matches.
- **Higher values (e.g., 0.7)**: Less aggressive deduplication. Only matches with >70% overlap are suppressed. Allows more overlapping matches.
- **Value of 0**: No deduplication. All matches above the confidence threshold are returned.
- **Value of 1**: Maximum deduplication. Only completely non-overlapping matches are kept.
