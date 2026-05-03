# Output Format

Understanding winguictl command output formats.

## Content Boundary Markers

All snapshot and find command outputs are wrapped with content boundary markers:

```
--- WINGUICTL_CONTENT nonce=a1b2c3d4e5f6a7b8 ---
[output content here]
--- END_WINGUICTL_CONTENT nonce=a1b2c3d4e5f6a7b8 ---
```

The `nonce` is a randomly generated hex string that must match between start and end markers. Always verify the nonce matches before trusting the captured content.

## Element Output Format

Elements are formatted as:

```
- "Element Text" [attribute1="value1" attribute2="value2" rect=(x,y width x height)]
```

### Common Attributes

| Attribute | Description |
|-----------|-------------|
| `text` | Element text/content (shown in quotes) |
| `rect` | Bounding rectangle (window-relative coordinates) |
| `control_type` | UIA or Win32 control type |
| `class` | Window class name |
| `hwnd` | Win32 control handle |
| `automation_id` | UIA automation ID |
| `runtime_id` | UIA runtime ID |
| `visible` | Whether element is visible |
| `enabled` | Whether element is enabled |
| `confidence` | Match confidence (0-1) for OCR/image matching |

## JSON Output Format

Some commands (like `action` and `window` operations) output JSON:

```json
{
  "ok": true,
  "code": "OK",
  "message": "click executed",
  "data": {
    "window_id": "12345",
    "window_title": "Window Title"
  }
}
```

### Result Codes

| Code | Description |
|------|-------------|
| `OK` | Operation succeeded |
| `FAILED` | Operation failed |
| `VALIDATION_ERROR` | Invalid input parameters |
| `ERROR` | Unexpected error |
| `DRY_RUN` | Preview mode (no action taken) |
