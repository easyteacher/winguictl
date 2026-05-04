# Clipboard Commands

Clipboard operations for copying files/text and getting text from the Windows clipboard.

## Commands

### copy-files

Copy files to the Windows clipboard. This allows pasting files in applications like Windows Explorer.

```powershell
python scripts\winguictl.py clipboard copy-files <file1> [file2] ...
```

#### Arguments

| Argument | Description |
|----------|-------------|
| `files` | One or more file paths to copy to clipboard |

#### Examples

```powershell
# Copy a single file
python scripts\winguictl.py clipboard copy-files "C:\Users\Documents\report.pdf"

# Copy multiple files
python scripts\winguictl.py clipboard copy-files "C:\file1.txt" "C:\file2.txt" "D:\images\photo.png"
```

#### Output

```json
{
  "ok": true,
  "code": "OK",
  "message": "copy_files executed",
  "data": {
    "files": ["C:\\file1.txt", "C:\\file2.txt"],
    "count": 2
  }
}
```

### copy-text

Copy text to the Windows clipboard.

```powershell
python scripts\winguictl.py clipboard copy-text <text>
```

#### Arguments

| Argument | Description |
|----------|-------------|
| `text` | Text string to copy to clipboard |

#### Examples

```powershell
# Copy simple text
python scripts\winguictl.py clipboard copy-text "Hello, World!"

# Copy text with spaces (use quotes)
python scripts\winguictl.py clipboard copy-text "This is a longer text string"
```

#### Output

```json
{
  "ok": true,
  "code": "OK",
  "message": "copy_text executed",
  "data": {
    "text": "Hello, World!",
    "length": 13
  }
}
```

### get-text

Get text from the Windows clipboard.

```powershell
python scripts\winguictl.py clipboard get-text
```

#### Output

```
--- WINGUICTL_CONTENT nonce=<nonce> ---
<clipboard text content>
--- END_WINGUICTL_CONTENT nonce=<nonce> ---
```

#### Examples

```powershell
# Get text from clipboard
python scripts\winguictl.py clipboard get-text
```

#### Error Output

If no text is available in the clipboard:

```json
{
  "ok": false,
  "code": "ERROR",
  "message": "get_text failed",
  "data": {
    "error": "no text in clipboard"
  }
}
```

## Use Cases

### Preparing Files for Upload

Copy files to clipboard before using paste operations in applications:

### 步骤1：Copy files to clipboard

```powershell
python scripts\winguictl.py clipboard copy-files "C:\Documents\report.pdf"
```

### 步骤2：Focus the target application window

```powershell
python scripts\winguictl.py window --window-id 12345 focus
```

### 步骤3：Click the paste area or use Ctrl+V

```powershell
python scripts\winguictl.py action --window-id 12345 hotkey --keys "{CTRL}v"
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `failed to copy files to clipboard` | Clipboard access denied or invalid paths | Ensure paths exist and application has clipboard access |
| `failed to copy text to clipboard` | Clipboard access denied | Close other applications that might be using clipboard |
| `no text in clipboard` | Clipboard is empty or contains non-text data | Copy text to clipboard first |
