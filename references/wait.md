# Wait Commands

Wait for conditions to be met before continuing.

For output format details, see [Output Format](output-format.md).

## Common Parameters

All wait commands (except `sleep`) support these parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--timeout` | 30.0 | Timeout in seconds |
| `--interval` | 500 | Poll interval in milliseconds |
| `--disappear` | false | Wait for element to disappear instead of appear |

## Sleep

Wait for a specified duration.

```powershell
python scripts\winguictl.py wait sleep <duration_ms>
```

### Example

```powershell
# Wait for 2 seconds
python scripts\winguictl.py wait sleep 2000

# Wait for 500 milliseconds
python scripts\winguictl.py wait sleep 500
```

### Output

```json
{"ok": true, "action": "sleep", "data": {"duration_ms": 2000}}
```

## Wait for Window

Wait for a window to appear or disappear.

### Wait for Window to Appear

```powershell
# Partial match (default)
python scripts\winguictl.py wait window "记事本"

# Exact match
python scripts\winguictl.py wait window "无标题 - 记事本" --exact

# With class name filter
python scripts\winguictl.py wait window "对话框" --class "#32770"
```

### Wait for Window to Disappear

```powershell
python scripts\winguictl.py wait window "加载中" --disappear --timeout 10
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `title` | Window title to match (supports partial match by default) |
| `--exact` | Match title exactly |
| `--class` | Filter by window class name |
| `--timeout` | Timeout in seconds (default: 30) |
| `--interval` | Poll interval in milliseconds (default: 500) |
| `--disappear` | Wait for window to disappear instead of appear |

### Output

On success (window appeared):
```json
{"ok": true, "action": "window_appear", "data": {"title": "记事本", "window_id": "12345", "window_title": "无标题 - 记事本", "elapsed_ms": 1500}}
```

On success (window disappeared):
```json
{"ok": true, "action": "window_disappear", "data": {"title": "加载中", "elapsed_ms": 3000}}
```

On timeout:
```json
{"ok": false, "action": "window_timeout", "data": {"title": "记事本", "timeout_sec": 30, "disappear": false, "error": "timeout waiting for window to appear"}}
```

## Wait for Text

Wait for text to appear or disappear in a window.

### Wait for Text to Appear

```powershell
# Fuzzy match (default)
python scripts\winguictl.py wait text --window-id <id> "确定"

# Exact match
python scripts\winguictl.py wait text --window-id <id> "确定" --exact
```

### Wait for Text to Disappear

```powershell
python scripts\winguictl.py wait text --window-id <id> "加载中" --disappear --timeout 10
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `--window-id` | Window handle (required) |
| `text` | Text to wait for |
| `--exact` | Match text exactly |
| `--timeout` | Timeout in seconds (default: 30) |
| `--interval` | Poll interval in milliseconds (default: 500) |
| `--disappear` | Wait for text to disappear instead of appear |

### Output

```json
{"ok": true, "action": "text_appear", "data": {"window_id": "12345", "text": "确定", "elapsed_ms": 800}}
```

## Wait for UIA Element

Wait for a UIA element to appear or disappear in a window.

### Wait for Element to Appear

```powershell
# Wait for button with specific text
python scripts\winguictl.py wait uia --window-id <id> --text "确定" --control-type Button

# Wait for element with specific automation-id
python scripts\winguictl.py wait uia --window-id <id> --automation-id "submitButton"

# Combined conditions
python scripts\winguictl.py wait uia --window-id <id> --text "保存" --control-type Button
```

### Wait for Element to Disappear

```powershell
python scripts\winguictl.py wait uia --window-id <id> --text "加载中" --disappear --timeout 15
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `--window-id` | Window handle (required) |
| `--text` | Filter by element text/name |
| `--control-type` | Filter by control type |
| `--class` | Filter by window class name |
| `--automation-id` | Filter by automation ID |
| `--exact` | Match text exactly |
| `--timeout` | Timeout in seconds (default: 30) |
| `--interval` | Poll interval in milliseconds (default: 500) |
| `--disappear` | Wait for element to disappear instead of appear |

### Output

```json
{"ok": true, "action": "uia_appear", "data": {"window_id": "12345", "elapsed_ms": 1200}}
```

## Wait for OCR Text

Wait for OCR-recognized text to appear or disappear in a window.

### Wait for OCR Text to Appear

```powershell
# Fuzzy match (default)
python scripts\winguictl.py wait ocr --window-id <id> "[3条]"

# Exact match
python scripts\winguictl.py wait ocr --window-id <id> "确定" --exact
```

### Wait for OCR Text to Disappear

```powershell
python scripts\winguictl.py wait ocr --window-id <id> "正在加载" --disappear --timeout 20
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `--window-id` | Window handle (required) |
| `text` | Text to wait for |
| `--exact` | Match text exactly |
| `--confidence-threshold` | OCR confidence threshold (default: 0.0) |
| `--timeout` | Timeout in seconds (default: 30) |
| `--interval` | Poll interval in milliseconds (default: 500) |
| `--disappear` | Wait for text to disappear instead of appear |

### Output

```json
{"ok": true, "action": "ocr_appear", "data": {"window_id": "12345", "text": "[3条]", "elapsed_ms": 2500}}
```

### Warning

OCR-based text finding captures visible text from the window, which may include sensitive information. See the warning in [Snapshot Commands](snapshot.md#ocr) regarding sensitive data.

## Wait for Image

Wait for an image template to appear or disappear in a window.

### Wait for Image to Appear

```powershell
python scripts\winguictl.py wait image --window-id <id> --image-path assets\button.png

# With custom threshold
python scripts\winguictl.py wait image --window-id <id> --image-path assets\button.png --threshold 0.95
```

### Wait for Image to Disappear

```powershell
python scripts\winguictl.py wait image --window-id <id> --image-path assets\loading.png --disappear --timeout 10
```

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--window-id` | (required) | Window handle |
| `--image-path` | (required) | Path to the template image file |
| `--threshold` | 0.9 | Match confidence threshold (0-1) |
| `--timeout` | 30.0 | Timeout in seconds |
| `--interval` | 500 | Poll interval in milliseconds |
| `--disappear` | false | Wait for image to disappear instead of appear |

### Output

```json
{"ok": true, "action": "image_appear", "data": {"window_id": "12345", "image_path": "assets\\button.png", "elapsed_ms": 1800}}
```

## Use Cases

### Wait for Dialog to Appear

```powershell
# After clicking a button, wait for dialog
python scripts\winguictl.py uia-control --window-id <id> --element-id "openButton" click
python scripts\winguictl.py wait window "打开" --class "#32770" --timeout 5
```

### Wait for Loading to Complete

```powershell
# Wait for loading indicator to disappear
python scripts\winguictl.py wait ocr --window-id <id> "加载中" --disappear --timeout 30
```

### Wait for Message Notification

```powershell
# Wait for new message badge to appear
python scripts\winguictl.py wait ocr --window-id <wx_id> "[新消息]" --timeout 60
```

### Wait for Button to Become Available

```powershell
# Wait for submit button to appear
python scripts\winguictl.py wait uia --window-id <id> --text "提交" --control-type Button --timeout 10
```

## Error Handling

All wait commands return exit code `1` on timeout or error:

| Exit Code | Description |
|-----------|-------------|
| 0 | Success (condition met) |
| 1 | Timeout or error |
