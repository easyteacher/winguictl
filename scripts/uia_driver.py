#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

"""UIA element operation driver module.

Operates on UI Automation elements through pywinauto's UIA backend,
including clicking, invoking, toggling, text reading/writing, scrolling, selecting, expanding/collapsing,
and combobox/list/tab/slider operations.
Also provides snapshot functionality for UIA element trees.
"""

from typing import Optional

from pywinauto import Desktop
from pywinauto.uia_element_info import UIAElementInfo

from models import ElementFormatter


class UIADriver:

    @staticmethod
    def _get_uia_wrapper(window_id: str, element_id: str):
        """Find and return the UIA element wrapper based on element_id.

        Search strategy:
        1. First try exact match by automation_id
        2. Then try exact match by runtime_id
        3. Raise ValueError if not found

        Args:
            window_id: Parent window handle string
            element_id: Element identifier (automation_id or runtime_id)

        Returns:
            Matched pywinauto UIA wrapper

        Raises:
            ValueError: No matching element found
        """
        target_handle = int(window_id)
        desktop = Desktop(backend="uia")
        wrapper = desktop.window(handle=target_handle)
        descendants = [wrapper] + list(wrapper.descendants())

        def normalize(value: Optional[str]) -> str:
            return (value or "").strip()

        def get_runtime_id(info) -> Optional[str]:
            try:
                raw = info if isinstance(info, UIAElementInfo) else getattr(info, "_element", info)
                rid = getattr(raw, "runtime_id", None)
                if rid is not None:
                    return "-".join(str(x) for x in rid)
            except Exception:
                pass
            return None

        query = normalize(element_id)
        for candidate in descendants:
            info = candidate.element_info
            if normalize(getattr(info, "automation_id", "")) == query:
                return candidate
        for candidate in descendants:
            info = candidate.element_info
            if get_runtime_id(info) == query:
                return candidate
        raise ValueError("UIA element not found: %s" % element_id)

    @staticmethod
    def click(window_id: str, element_id: str) -> None:
        """Click the UIA element."""
        UIADriver._get_uia_wrapper(window_id, element_id).click()

    @staticmethod
    def invoke(window_id: str, element_id: str) -> None:
        """Invoke the UIA element's Invoke pattern (for buttons, menu items, etc.)."""
        UIADriver._get_uia_wrapper(window_id, element_id).invoke()

    @staticmethod
    def toggle(window_id: str, element_id: str) -> None:
        """Toggle the UIA element's Toggle pattern (for checkboxes)."""
        UIADriver._get_uia_wrapper(window_id, element_id).toggle()

    @staticmethod
    def get_toggle_state(window_id: str, element_id: str) -> int:
        """Get the toggle state of the UIA element (0=off, 1=on, 2=indeterminate)."""
        return UIADriver._get_uia_wrapper(window_id, element_id).get_toggle_state()

    @staticmethod
    def get_text(window_id: str, element_id: str) -> str:
        """Get the text content of the UIA element."""
        return UIADriver._get_uia_wrapper(window_id, element_id).window_text()

    @staticmethod
    def set_text(window_id: str, element_id: str, text: str) -> None:
        """Set the text content of a UIA edit control."""
        wrapper = UIADriver._get_uia_wrapper(window_id, element_id)
        try:
            wrapper.set_text(text, 0, len(text))
        except Exception:
            wrapper.iface_value.SetValue(text)

    @staticmethod
    def set_focus(window_id: str, element_id: str) -> None:
        """Set focus to the UIA element."""
        UIADriver._get_uia_wrapper(window_id, element_id).set_focus()

    @staticmethod
    def double_click(window_id: str, element_id: str, button: str = "left") -> None:
        """Double-click the UIA element."""
        UIADriver._get_uia_wrapper(window_id, element_id).double_click_input(button=button)

    @staticmethod
    def right_click(window_id: str, element_id: str) -> None:
        """Right-click the UIA element."""
        UIADriver._get_uia_wrapper(window_id, element_id).right_click_input()

    @staticmethod
    def type_keys(window_id: str, element_id: str, keys: str) -> None:
        """Send key sequence to the UIA element (pywinauto format)."""
        UIADriver._get_uia_wrapper(window_id, element_id).type_keys(keys)

    @staticmethod
    def scroll(window_id: str, element_id: str, direction: str, amount: str = "page", count: int = 1) -> None:
        """Scroll the UIA element.

        Args:
            direction: Scroll direction ("up"/"down"/"left"/"right")
            amount: Scroll amount ("line"/"page")
            count: Number of scrolls
        """
        UIADriver._get_uia_wrapper(window_id, element_id).scroll(direction, amount, count)

    @staticmethod
    def get_value(window_id: str, element_id: str) -> str:
        """Get the current value of the UIA element (via Value pattern)."""
        return UIADriver._get_uia_wrapper(window_id, element_id).iface_value.CurrentValue

    @staticmethod
    def set_value(window_id: str, element_id: str, value: str) -> None:
        """Set the value of the UIA element (via Value pattern)."""
        UIADriver._get_uia_wrapper(window_id, element_id).iface_value.SetValue(value)

    @staticmethod
    def select(window_id: str, element_id: str) -> None:
        """Select the UIA element (for list items, tree items, etc.)."""
        UIADriver._get_uia_wrapper(window_id, element_id).select()

    @staticmethod
    def expand(window_id: str, element_id: str) -> None:
        """Expand the UIA element (for combo boxes, tree nodes, etc.)."""
        UIADriver._get_uia_wrapper(window_id, element_id).expand()

    @staticmethod
    def collapse(window_id: str, element_id: str) -> None:
        """Collapse the UIA element."""
        UIADriver._get_uia_wrapper(window_id, element_id).collapse()

    @staticmethod
    def is_expanded(window_id: str, element_id: str) -> bool:
        """Check whether the UIA element is in expanded state."""
        try:
            return UIADriver._get_uia_wrapper(window_id, element_id).is_expanded()
        except Exception:
            return False

    @staticmethod
    def combo_select(window_id: str, element_id: str, item) -> None:
        """Select an item in a UIA combobox."""
        UIADriver._get_uia_wrapper(window_id, element_id).select(item)

    @staticmethod
    def combo_items(window_id: str, element_id: str) -> list[str]:
        """Get all item texts in a UIA combobox."""
        return UIADriver._get_uia_wrapper(window_id, element_id).texts()

    @staticmethod
    def combo_selected_text(window_id: str, element_id: str) -> Optional[str]:
        """Get the selected item text in a UIA combobox."""
        return UIADriver._get_uia_wrapper(window_id, element_id).selected_text()

    @staticmethod
    def combo_selected_index(window_id: str, element_id: str) -> int:
        """Get the selected item index in a UIA combobox."""
        return UIADriver._get_uia_wrapper(window_id, element_id).selected_index()

    @staticmethod
    def list_items(window_id: str, element_id: str) -> list[str]:
        """Get all item texts in a UIA list."""
        items = UIADriver._get_uia_wrapper(window_id, element_id).children(content_only=True)
        return [item.window_text() for item in items]

    @staticmethod
    def list_select(window_id: str, element_id: str, item) -> None:
        """Select an item in a UIA list."""
        UIADriver._get_uia_wrapper(window_id, element_id).get_item(item).select()

    @staticmethod
    def list_selected_items(window_id: str, element_id: str) -> list[str]:
        """Get all selected item texts in a UIA list."""
        selection = UIADriver._get_uia_wrapper(window_id, element_id).get_selection()
        if selection:
            return [elem.name for elem in selection]
        return []

    @staticmethod
    def tab_select(window_id: str, element_id: str, item) -> None:
        """Select a UIA tab."""
        UIADriver._get_uia_wrapper(window_id, element_id).select(item)

    @staticmethod
    def tab_selected(window_id: str, element_id: str) -> int:
        """Get the selected tab index in a UIA tab control."""
        return UIADriver._get_uia_wrapper(window_id, element_id).get_selected_tab()

    @staticmethod
    def tab_count(window_id: str, element_id: str) -> int:
        """Get the number of tabs in a UIA tab control."""
        return UIADriver._get_uia_wrapper(window_id, element_id).tab_count()

    @staticmethod
    def slider_value(window_id: str, element_id: str) -> float:
        """Get the current value of a UIA slider."""
        return UIADriver._get_uia_wrapper(window_id, element_id).value()

    @staticmethod
    def slider_set_value(window_id: str, element_id: str, value: float) -> None:
        """Set the value of a UIA slider."""
        UIADriver._get_uia_wrapper(window_id, element_id).set_value(value)

    @staticmethod
    def slider_min(window_id: str, element_id: str) -> float:
        """Get the minimum value of a UIA slider."""
        return UIADriver._get_uia_wrapper(window_id, element_id).min_value()

    @staticmethod
    def slider_max(window_id: str, element_id: str) -> float:
        """Get the maximum value of a UIA slider."""
        return UIADriver._get_uia_wrapper(window_id, element_id).max_value()

    @staticmethod
    def snapshot_uia_tree(window_id: str) -> str:
        """Generate a UIA element tree snapshot for the window.

        Recursively traverses all UIA child elements of the target window,
        formatting each element's name, control type, class name, automation ID, etc.
        """
        target_handle = int(window_id)
        desktop = Desktop(backend="uia")
        wrapper = desktop.window(handle=target_handle)
        lines: list[str] = []

        def walk(element, level: int) -> None:
            info = element.element_info
            lines.append(ElementFormatter.format_uia(info, level))
            try:
                for child in element.children():
                    walk(child, level + 1)
            except Exception:
                pass

        walk(wrapper, 0)
        return "\n".join(lines)
