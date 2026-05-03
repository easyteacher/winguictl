# Find Commands

Find elements in a window.

## Content Boundary Markers

All find command outputs are wrapped with content boundary markers to help identify and isolate captured content:

```
--- WINGUICTL_CONTENT nonce=a1b2c3d4e5f6g7h8 ---
[find output here]
--- END_WINGUICTL_CONTENT nonce=a1b2c3d4e5f6g7h8 ---
```

The `nonce` is a randomly generated hex string that must match between the start and end markers. Always verify the nonce matches before trusting the captured content.

## Find Text

```powershell
# Find visible controls containing the specified text (fuzzy match)
python scripts\winguictl.py find --window-id <id> text "Submit"

# Find visible controls exactly matching the specified text
python scripts\winguictl.py find --window-id <id> text "Submit" --exact
```

## Find UIA Controls

```powershell
# Find controls containing the specified text via UIA
python scripts\winguictl.py find --window-id <id> uia --text "Submit"

# Find controls exactly matching the specified text via UIA
python scripts\winguictl.py find --window-id <id> uia --text "Submit" --exact

# Find elements of a specified control type via UIA
python scripts\winguictl.py find --window-id <id> uia --control-type Button

# Combined conditions: find buttons whose text contains "OK"
python scripts\winguictl.py find --window-id <id> uia --text "OK" --control-type Button
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

## Find OCR Text

```powershell
# Find text in a window via OCR (fuzzy match)
python scripts\winguictl.py find --window-id <id> ocr "Confirm"

# Find text via OCR, with confidence threshold
python scripts\winguictl.py find --window-id <id> ocr "Confirm" --confidence-threshold 0.7
```

### Note

The `--confidence-threshold` parameter is currently reserved for future use. The wx_ocr library does not provide confidence scores, so all matches are assigned a fixed confidence of 0.9.

### Warning

OCR-based text finding captures visible text from the window, which may include sensitive information. See the warning in [Snapshot Commands](snapshot.md#ocr) regarding sensitive data.

## Find Image

```powershell
# Find a matching image template in a window
python scripts\winguictl.py find --window-id <id> image --image-path assets\button.png

# Find image template with custom match similarity threshold (default 0.9)
python scripts\winguictl.py find --window-id <id> image --image-path assets\button.png --threshold 0.95
```
