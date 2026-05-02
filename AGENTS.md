# Architecture

The skill scripts consist of the following modules, each with specific responsibilities:

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
└── models.py           # Data models (WindowInfo, Bounds, ActionResult)
```

| Module | Responsibility | Dependencies |
|------|------|------|
| `winguictl.py` | CLI command parsing, dispatching subcommands to appropriate drivers | All drivers |
| `windows_driver.py` | Window listing, minimize/maximize/restore/close/move/resize/focus | pywinauto, pywin32 |
| `win32_driver.py` | Native Win32 control operations (click, input, checkbox, combobox, etc.) | pywinauto |
| `uia_driver.py` | UIA control operations (click, scroll, expand/collapse, slider, etc.) | pywinauto, comtypes |
| `ocr_driver.py` | Window screenshot + OCR text recognition | wx-ocr |
| `find_driver.py` | Find elements by text/UIA/OCR/image | pywinauto, wx-ocr, opencv |
| `win32_utils.py` | Low-level input simulation (mouse click/drag, keyboard input, screenshot) | pywin32, ctypes (PrintWindow only) |
| `constants.py` | Virtual key code mapping table, Win32 control type mapping table | — |
| `models.py` | Data class definitions | dataclasses |
