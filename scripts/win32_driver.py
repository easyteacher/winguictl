#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

"""Win32 control operation driver module.

Operates on native Win32 controls through pywinauto's Win32 backend,
including text reading/writing, clicking, key input, button/combobox/listbox operations, etc.
Also provides snapshot functionality for HWND control trees.
"""

from typing import Optional

from pywinauto import Desktop
from pywinauto.controls.hwndwrapper import HwndWrapper
from pywinauto.controls.win32_controls import (
    ButtonWrapper,
    ComboBoxWrapper,
    EditWrapper,
    ListBoxWrapper,
)

from constants import WIN32_CONTROL_TYPE_MAP
from models import ElementFormatter
from win32_utils import Win32API


class Win32Driver:

    @staticmethod
    def _wrap_hwnd(hwnd: int) -> HwndWrapper:
        """Wrap a handle integer as an HwndWrapper instance."""
        return HwndWrapper(hwnd)

    @staticmethod
    def infer_control_type(class_name: Optional[str]) -> Optional[str]:
        """Infer control type from window class name.

        Matching strategy (by priority):
        1. Exact match (case-insensitive)
        2. Prefix match (case-insensitive)
        3. Contains match (case-insensitive)
        """
        if not class_name:
            return None
        class_lower = class_name.lower()
        for pattern, control_type in WIN32_CONTROL_TYPE_MAP.items():
            if pattern.lower() == class_lower:
                return control_type
            if class_lower.startswith(pattern.lower()):
                return control_type
        for pattern, control_type in WIN32_CONTROL_TYPE_MAP.items():
            if pattern.lower() in class_lower:
                return control_type
        return None

    @staticmethod
    def set_text(hwnd: int, text: str) -> None:
        """Set the text content of an edit control."""
        EditWrapper(hwnd).set_edit_text(text)

    @staticmethod
    def get_text(hwnd: int) -> str:
        """Get the text content of an edit control."""
        return EditWrapper(hwnd).text_block()

    @staticmethod
    def set_focus(hwnd: int) -> None:
        """Set focus to the specified control."""
        Win32API.set_focus(hwnd)

    @staticmethod
    def click(hwnd: int, button: str = "left") -> None:
        """Click the control."""
        Win32Driver._wrap_hwnd(hwnd).click(button=button)

    @staticmethod
    def double_click(hwnd: int, button: str = "left") -> None:
        """Double-click the control."""
        Win32Driver._wrap_hwnd(hwnd).double_click(button=button)

    @staticmethod
    def right_click(hwnd: int) -> None:
        """Right-click the control."""
        Win32Driver._wrap_hwnd(hwnd).right_click()

    @staticmethod
    def type_keys(hwnd: int, keys: str) -> None:
        """Send key sequence to the control (pywinauto format)."""
        Win32Driver._wrap_hwnd(hwnd).type_keys(keys)

    @staticmethod
    def send_chars(hwnd: int, chars: str) -> None:
        """Send characters to an inactive window."""
        Win32Driver._wrap_hwnd(hwnd).send_chars(chars)

    @staticmethod
    def send_keystrokes(hwnd: int, keystrokes: str) -> None:
        """Send keystrokes to an inactive window (pywinauto format)."""
        Win32Driver._wrap_hwnd(hwnd).send_keystrokes(keystrokes)

    @staticmethod
    def check(hwnd: int) -> None:
        """Check a checkbox."""
        ButtonWrapper(hwnd).check()

    @staticmethod
    def uncheck(hwnd: int) -> None:
        """Uncheck a checkbox."""
        ButtonWrapper(hwnd).uncheck()

    @staticmethod
    def is_checked(hwnd: int) -> Optional[bool]:
        """Get the checked state of a checkbox."""
        return ButtonWrapper(hwnd).is_checked()

    @staticmethod
    def combo_select(hwnd: int, item) -> None:
        """Select an item in a combobox (by index or text)."""
        ComboBoxWrapper(hwnd).select(item)

    @staticmethod
    def combo_items(hwnd: int) -> list[str]:
        """Get all item texts in a combobox."""
        return ComboBoxWrapper(hwnd).item_texts()

    @staticmethod
    def combo_selected_index(hwnd: int) -> int:
        """Get the selected item index in a combobox."""
        return ComboBoxWrapper(hwnd).selected_index()

    @staticmethod
    def combo_selected_text(hwnd: int) -> str:
        """Get the selected item text in a combobox."""
        return ComboBoxWrapper(hwnd).selected_text()

    @staticmethod
    def listbox_select(hwnd: int, item) -> None:
        """Select an item in a listbox (by index or text)."""
        ListBoxWrapper(hwnd).select(item)

    @staticmethod
    def listbox_items(hwnd: int) -> list[str]:
        """Get all item texts in a listbox."""
        return ListBoxWrapper(hwnd).item_texts()

    @staticmethod
    def listbox_selected_indices(hwnd: int) -> tuple:
        """Get the indices of all selected items in a listbox."""
        return ListBoxWrapper(hwnd).selected_indices()

    @staticmethod
    def snapshot_hwnd_tree(window_id: str) -> str:
        """Generate an HWND control tree snapshot for the window.

        Traverses the target window and all its descendant controls,
        formatting each control's handle, text, class name, visibility,
        enabled state, and other information.
        """
        target_handle = int(window_id)
        desktop = Desktop(backend="win32")
        wrapper = desktop.window(handle=target_handle)
        lines: list[str] = []
        visited: set[int] = set()

        for element in [wrapper] + list(wrapper.descendants()):
            info = element.element_info
            hwnd = getattr(info, "handle", None) or 0
            if hwnd in visited:
                continue
            visited.add(hwnd)
            text = (getattr(info, "name", "") or "").strip()
            if not text:
                text = (getattr(info, "rich_text", "") or "").strip()
            cls = (getattr(info, "class_name", "") or "").strip()
            visible = getattr(info, "visible", True)
            enabled = getattr(info, "enabled", True)
            control_id = getattr(info, "control_id", None)
            control_type = Win32Driver.infer_control_type(cls)
            level = 0
            parent = element.parent()
            while parent is not None and parent != wrapper:
                level += 1
                parent = parent.parent()
            lines.append(ElementFormatter.format_hwnd(hwnd, text, cls, visible, enabled, control_id, level, control_type))

        return "\n".join(lines)
