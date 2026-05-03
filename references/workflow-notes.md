# Workflow Notes

Best practices for using winguictl commands effectively.

## Prefer Structured Identifiers

Action commands (`click`, `type`, etc.) rely on coordinates or image matching. For more reliable automation:

1. **Prefer `control` / `uia-control` commands** over `action` commands
2. Use structured identifiers (`hwnd`, `automation_id`, `runtime_id`) when available
3. Reserve `action` commands as a fallback when structured approaches don't work

```powershell
# Preferred: Use control commands with structured identifiers
python scripts\winguictl.py uia-control --window-id 12345 --element-id "SubmitButton" click

# Fallback: Use action commands with coordinates
python scripts\winguictl.py action --window-id 12345 click --relative-x 100 --relative-y 200
```

## Re-obtain Snapshots After Actions

Action operations may change the UI state:

- Window content may change
- Element positions may shift
- New elements may appear
- Existing elements may disappear

**Always re-run `snapshot` commands after actions to get the latest UI state.**

```powershell
# 1. Get initial snapshot
python scripts\winguictl.py snapshot --window-id 12345 uia

# 2. Perform action
python scripts\winguictl.py uia-control --window-id 12345 --element-id "NextButton" click

# 3. Get updated snapshot before next action
python scripts\winguictl.py snapshot --window-id 12345 uia
```

## Typical Workflow

1. **List windows** to find the target
   ```powershell
   python scripts\winguictl.py window list
   ```

2. **Focus the window** to bring it to foreground
   ```powershell
   python scripts\winguictl.py window --window-id 12345 focus
   ```

3. **Get snapshot** to understand window structure
   ```powershell
   python scripts\winguictl.py snapshot --window-id 12345 uia
   ```

4. **Find elements** if needed
   ```powershell
   python scripts\winguictl.py find --window-id 12345 uia --text "Submit"
   ```

5. **Interact with elements** (preview with --dry-run first)
   ```powershell
   python scripts\winguictl.py uia-control --window-id 12345 --element-id "SubmitButton" click
   ```

6. **Verify results** with another snapshot
   ```powershell
   python scripts\winguictl.py snapshot --window-id 12345 uia
   ```

## Finding the Right Approach

| Scenario | Recommended Command |
|----------|-------------------|
| Win32 controls with known hwnd | `control --hwnd <hwnd> click` |
| UIA controls with automation_id | `uia-control --element-id <id> click` |
| UIA controls without automation_id | `uia-control --element-id <runtime_id> click` |
| Text-based UI elements | `find ocr` + `action click` |
| Icon/image buttons | `find image` + `action click` |
| Unknown element at known position | `action click --relative-x/y` |
