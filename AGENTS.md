# Architecture

```
scripts/
├── winguictl.py        # CLI entry point, command parsing and dispatch
├── windows_driver.py   # Window management (based on pywinauto HwndWrapper)
├── win32_driver.py     # Win32 control operations (based on pywinauto HwndWrapper)
├── uia_driver.py       # UIA control operations (based on pywinauto UIA backend)
├── ocr_driver.py       # OCR text recognition (based on wx-ocr)
├── find_driver.py      # Element finding (text/UIA/OCR/image)
├── win32_utils.py      # Win32 API low-level wrapper (pywin32 + ctypes fallback)
├── constants.py        # Named constants, VK mapping, control types, optional deps
├── output_utils.py     # Output formatting, boundary markers, JSON emission
└── models.py           # Data models (WindowInfo, Bounds, ActionResult)
```

| Module | Responsibility | Dependencies |
|------|------|------|
| `winguictl.py` | CLI command parsing, dispatching subcommands to appropriate drivers | All drivers (lazy) |
| `windows_driver.py` | Window listing, minimize/maximize/restore/close/move/resize/focus | pywinauto, pywin32 |
| `win32_driver.py` | Native Win32 control operations (click, input, checkbox, combobox, etc.) | pywinauto |
| `uia_driver.py` | UIA control operations (click, scroll, expand/collapse, slider, etc.) | pywinauto, comtypes |
| `ocr_driver.py` | Window screenshot + OCR text recognition | wx-ocr (optional) |
| `find_driver.py` | Find elements by text/UIA/OCR/image | pywinauto, opencv (optional) |
| `win32_utils.py` | Low-level input simulation (mouse click/drag, keyboard input, screenshot) | pywin32, ctypes (PrintWindow only) |
| `constants.py` | Named constants, VK codes, control type mappings, optional dependency detection | opencv, wx-ocr (optional) |
| `output_utils.py` | Output formatting, boundary markers, control info builders | models, win32_utils |
| `models.py` | Data class definitions | dataclasses |

---

# Development Best Practices

## Import Strategy

- Use lazy imports (imports inside functions) for heavy modules (`pywinauto`)
- Import optional dependencies (`cv2`, `wx_ocr`) from `constants.py` for centralized detection
- Use `TYPE_CHECKING` block for type-hint-only imports
- Organize imports: standard library → third-party → local

## Error Handling

- Handle errors at CLI entry point with appropriate error codes
- Error codes: `OK`, `FAILED`, `VALIDATION_ERROR`, `ERROR`, `DRY_RUN`
- Use broad exception catching at driver boundaries with logging

## Logging

- Configure logging in CLI entry point
- Levels: `DEBUG` (verbose), `INFO`, `WARNING` (default), `ERROR`
- Log to stderr, output results to stdout
- Use lazy % formatting for performance

## Type Annotations

- Omit or generalize complex return type annotations
- Use `TYPE_CHECKING` for type-hint-only imports

## Security

- Wrap captured content with boundary markers to prevent context injection
- Never mix stdout results with stderr logs

## Code Style

- Use `@staticmethod` for methods that don't need instance state
- Use `dataclasses` for data models
- Use named constants instead of magic numbers (defined in `constants.py`)

## Constants

All named constants are centralized in `constants.py`:

| Category | Constants | Purpose |
|----------|-----------|---------|
| SendInput | `SENDINPUT_ABSOLUTE_MAX` | Absolute coordinate range (65535) |
| Delays | `DEFAULT_CLICK_DELAY_MS`, `DEFAULT_KEY_DELAY_MS`, `DEFAULT_DRAG_START_DELAY_MS`, `DEFAULT_HOTKEY_DELAY_MS` | Input simulation delays |
| UIA Timeouts | `DEFAULT_UIA_WAIT_TIMEOUT_SEC`, `DEFAULT_COMBOBOX_DROPDOWN_TIMEOUT_MS`, `DEFAULT_COMBOBOX_POLL_INTERVAL_MS` | UIA operation timeouts |
| VK Codes | `VK_CODE_MAP` | Virtual key code mapping |
| Control Types | `WIN32_CONTROL_TYPE_MAP` | Win32 class name to control type |

## Pylint

The project uses pylint for code quality checks. Configuration is in `scripts/.pylintrc`.

### Configuration Highlights

| Setting | Value | Reason |
|---------|-------|--------|
| `max-line-length` | 120 | Readability |
| `max-locals` | 25 | Complex UIA/Win32 operations |
| `max-branches` | 35 | Match/case command handlers |
| `max-statements` | 80 | Large command handlers |
| `max-public-methods` | 35 | Driver classes with many operations |

### Disabled Checks

| Code | Reason |
|------|--------|
| `C0301` | Line too long (handled by max-line-length) |
| `C0415` | Late import (intentional lazy imports) |
| `W0107` | Unnecessary pass (placeholder methods) |
| `W0611` | Unused import (TYPE_CHECKING imports) |
| `W0201` | Attribute defined outside `__init__` (pywinauto wrappers) |
| `W2301` | Unused variable in exception handler |
| `I1101` | Wrong import order (lazy imports) |
| `R0902-R0917` | Too many arguments/locals/branches (CLI handlers) |
| `R1702` | Too many nested blocks (match/case handlers) |

### Extension Packages

The following C-extension packages are allowlisted:
- `win32api`, `win32con`, `win32gui`, `win32ui`, `win32process` (pywin32)
- `wx_ocr` (WeChat OCR)
- `PIL` (Pillow)

## Documentation Style

- Use Markdown headings instead of code block comments for steps

---

# Best Practices Summary

## Input Validation

- Always validate `window_id` before operations using `Win32API.validate_window_id()`
- Validate `hwnd` in `_handle_control` using `Win32API.get_window_bounds()` (returns None for invalid handles)
- Validate coordinates with `validate_relative_coords()` before click/drag operations
- Check optional dependencies at runtime using helper functions from `constants.py`

## Error Handling

- Add debug logging for fallback operations (e.g., PrintWindow → BitBlt)
- Validate bitmap data after capture to detect silent failures
- Use broad exception catching at driver boundaries with logging
- **Consistent handler error handling pattern**: All `_handle_*` functions must have try/except blocks that:
  1. Include `Win32API.validate_window_id()` inside the try block (not before)
  2. Build context info (window_id, window_title, etc.) inside the try block
  3. Emit errors with context via `emit_action(False, verb, {..., "error": str(e)})`
  4. Return 1 on error (0 on success, -1 for unknown subcommands)

## Code Organization

- Extract complex methods into smaller helper functions (see `combo_items` refactoring pattern)
- Place validation utilities in `win32_utils.py` for reuse across drivers
- Keep CLI entry point (`winguictl.py`) focused on command dispatch, not business logic

## Dependency Management

Optional dependencies are centralized in `constants.py`:

| Flag | Helper Function | Package |
|------|-----------------|---------|
| `_OPENCV_AVAILABLE` | `check_opencv_available()` | opencv-python |
| `_WX_OCR_AVAILABLE` | `check_wx_ocr_available()` | wx-ocr |

Usage pattern:
- Import flags (`cv2`, `np`, `wx_ocr`) and helper functions from `constants.py`
- Call helper function at runtime to raise `RuntimeError` with installation instructions if dependency missing
- Avoids duplicate try/except blocks across driver modules

## API Documentation

- Document edge case behavior in docstrings (e.g., coordinate validation allows edge coordinates)
- Add comments for non-obvious formulas (e.g., F-key VK mapping: `0x6F + index → VK_F1..VK_F12`)

