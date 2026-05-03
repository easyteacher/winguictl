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
├── constants.py        # Virtual key mapping table, control type mapping table
├── output_utils.py     # Output formatting, boundary markers, JSON emission
└── models.py           # Data models (WindowInfo, Bounds, ActionResult)
```

| Module | Responsibility | Dependencies |
|------|------|------|
| `winguictl.py` | CLI command parsing, dispatching subcommands to appropriate drivers | All drivers (lazy) |
| `windows_driver.py` | Window listing, minimize/maximize/restore/close/move/resize/focus | pywinauto, pywin32 |
| `win32_driver.py` | Native Win32 control operations (click, input, checkbox, combobox, etc.) | pywinauto |
| `uia_driver.py` | UIA control operations (click, scroll, expand/collapse, slider, etc.) | pywinauto, comtypes |
| `ocr_driver.py` | Window screenshot + OCR text recognition | wx-ocr |
| `find_driver.py` | Find elements by text/UIA/OCR/image | pywinauto, wx-ocr, opencv |
| `win32_utils.py` | Low-level input simulation (mouse click/drag, keyboard input, screenshot) | pywin32, ctypes (PrintWindow only) |
| `constants.py` | Virtual key code mapping table, Win32 control type mapping table | — |
| `output_utils.py` | Output formatting, boundary markers, control info builders | models, win32_utils |
| `models.py` | Data class definitions | dataclasses |

---

# Development Best Practices

## Import Strategy

- Use lazy imports (imports inside functions) for heavy modules (`pywinauto`, `cv2`, `wx_ocr`)
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

## Documentation Style

- Use Markdown headings instead of code block comments for steps

