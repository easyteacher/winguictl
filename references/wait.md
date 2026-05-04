# Wait Commands

Wait for conditions to be met before continuing.

For output format details, see [Output Format](output-format.md).

## Common Parameters

All wait commands support these parameters at the main command level:

| Parameter | Description |
|-----------|-------------|
| `--window-id` | Window handle (required for text, uia, ocr, image subcommands) |

The `--window-id` can be specified anywhere in the command line:

```powershell
# All these are equivalent
python scripts\winguictl.py --window-id 123 wait uia --automation-id "button"
python scripts\winguictl.py wait --window-id 123 uia --automation-id "button"
python scripts\winguictl.py wait uia --window-id 123 --automation-id "button"
```

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
```
--- WINGUICTL_CONTENT nonce=abc123 ---
- "无标题 - 记事本" [window_id="12345" class_name="Notepad" process="notepad.exe" pid="5678"]
--- END_WINGUICTL_CONTENT nonce=abc123 ---
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
python scripts\winguictl.py --window-id <id> wait text "确定"

# Exact match
python scripts\winguictl.py --window-id <id> wait text "确定" --exact
```

### Wait for Text to Disappear

```powershell
python scripts\winguictl.py --window-id <id> wait text "加载中" --disappear --timeout 10
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `--window-id` | Window handle (required, can be specified at any position) |
| `text` | Text to wait for |
| `--exact` | Match text exactly |
| `--timeout` | Timeout in seconds (default: 30) |
| `--interval` | Poll interval in milliseconds (default: 500) |
| `--disappear` | Wait for text to disappear instead of appear |

### Output

On success, returns matched elements with full control information:
```
--- WINGUICTL_CONTENT nonce=abc123 ---
- "确定" [control_type="Button" class="Button" confidence=0.95 relative_rect=(100,200 80x30) runtime_id="42-12345-4-1234"]
--- END_WINGUICTL_CONTENT nonce=abc123 ---
```

## Wait for UIA Element

Wait for a UIA element to appear or disappear in a window.

### Wait for Element to Appear

```powershell
# Wait for button with specific text
python scripts\winguictl.py --window-id <id> wait uia --text "确定" --control-type Button

# Wait for element with specific automation-id
python scripts\winguictl.py --window-id <id> wait uia --automation-id "submitButton"

# Combined conditions
python scripts\winguictl.py --window-id <id> wait uia --text "保存" --control-type Button
```

### Wait for Element to Disappear

```powershell
python scripts\winguictl.py --window-id <id> wait uia --text "加载中" --disappear --timeout 15
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `--window-id` | Window handle (required, can be specified at any position) |
| `--text` | Filter by element text/name |
| `--control-type` | Filter by control type |
| `--class` | Filter by window class name |
| `--automation-id` | Filter by automation ID |
| `--exact` | Match text exactly |
| `--timeout` | Timeout in seconds (default: 30) |
| `--interval` | Poll interval in milliseconds (default: 500) |
| `--disappear` | Wait for element to disappear instead of appear |

### Output

On success, returns matched elements with full control information:
```
--- WINGUICTL_CONTENT nonce=abc123 ---
- "确定" [control_type="Button" class="Button" automation_id="okButton" confidence=0.95 relative_rect=(100,200 80x30) runtime_id="42-12345-4-1234"]
--- END_WINGUICTL_CONTENT nonce=abc123 ---
```

## Wait for OCR Text

Wait for OCR-recognized text to appear or disappear in a window.

### Wait for OCR Text to Appear

```powershell
# Fuzzy match (default)
python scripts\winguictl.py --window-id <id> wait ocr "[3条]"

# Exact match
python scripts\winguictl.py --window-id <id> wait ocr "确定" --exact
```

### Wait for OCR Text to Disappear

```powershell
python scripts\winguictl.py --window-id <id> wait ocr "正在加载" --disappear --timeout 20
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `--window-id` | Window handle (required, can be specified at any position) |
| `text` | Text to wait for |
| `--exact` | Match text exactly |
| `--confidence-threshold` | OCR confidence threshold (default: 0.0) |
| `--timeout` | Timeout in seconds (default: 30) |
| `--interval` | Poll interval in milliseconds (default: 500) |
| `--disappear` | Wait for text to disappear instead of appear |

### Output

On success, returns matched text regions:
```
--- WINGUICTL_CONTENT nonce=abc123 ---
- "[3条]" [confidence=0.90 relative_rect=(100,50 40x20)]
--- END_WINGUICTL_CONTENT nonce=abc123 ---
```

### Warning

OCR-based text finding captures visible text from the window, which may include sensitive information. See the warning in [Snapshot Commands](snapshot.md#ocr) regarding sensitive data.

## Wait for Image

Wait for an image template to appear or disappear in a window.

### Wait for Image to Appear

```powershell
python scripts\winguictl.py --window-id <id> wait image --image-path assets\button.png

# With custom threshold
python scripts\winguictl.py --window-id <id> wait image --image-path assets\button.png --threshold 0.95
```

### Wait for Image to Disappear

```powershell
python scripts\winguictl.py --window-id <id> wait image --image-path assets\loading.png --disappear --timeout 10
```

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--window-id` | (required) | Window handle (can be specified at any position) |
| `--image-path` | (required) | Path to the template image file |
| `--threshold` | 0.9 | Match confidence threshold (0-1) |
| `--timeout` | 30.0 | Timeout in seconds |
| `--interval` | 500 | Poll interval in milliseconds |
| `--disappear` | false | Wait for image to disappear instead of appear |

### Output

On success, returns matched image regions:
```
--- WINGUICTL_CONTENT nonce=abc123 ---
- "button.png" [confidence=0.95 relative_rect=(100,200 80x30)]
--- END_WINGUICTL_CONTENT nonce=abc123 ---
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
python scripts\winguictl.py --window-id <id> wait ocr "加载中" --disappear --timeout 30
```

### Wait for Message Notification

```powershell
# Wait for new message badge to appear
python scripts\winguictl.py --window-id <wx_id> wait ocr "[新消息]" --timeout 60
```

### Wait for Button to Become Available

```powershell
# Wait for submit button to appear
python scripts\winguictl.py --window-id <id> wait uia --text "提交" --control-type Button --timeout 10
```

## Error Handling

All wait commands return exit code `1` on timeout or error:

| Exit Code | Description |
|-----------|-------------|
| 0 | Success (condition met) |
| 1 | Timeout or error |

When `--window-id` is required but not provided:
```json
{"ok": false, "action": "text", "data": {"error": "--window-id is required for text subcommand"}}
```
