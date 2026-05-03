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

import logging
import time
from typing import TYPE_CHECKING, Any, Optional, Union

from pywinauto import Desktop
from pywinauto.uia_element_info import UIAElementInfo
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.timings import TimeoutError as PywinautoTimeoutError

from constants import (
    DEFAULT_COMBOBOX_DROPDOWN_TIMEOUT_MS,
    DEFAULT_COMBOBOX_POLL_INTERVAL_MS,
    DEFAULT_UIA_WAIT_TIMEOUT_SEC,
)
from models import ElementFormatter

if TYPE_CHECKING:
    from pywinauto.controls.uiawrapper import UiaWrapper

_logger = logging.getLogger(__name__)

_uia_desktop: Optional[Desktop] = None


def _get_uia_desktop() -> Desktop:
    """Get or create a cached UIA Desktop instance."""
    global _uia_desktop
    if _uia_desktop is None:
        _uia_desktop = Desktop(backend="uia")
    return _uia_desktop


class UIAOperationError(RuntimeError):
    """Base exception for UIA operation failures."""
    pass


class UIAElementNotFoundError(UIAOperationError):
    """Raised when a UIA element cannot be found."""
    pass


class UIATimeoutError(UIAOperationError):
    """Raised when a UIA operation times out."""
    pass


class UIAAttributeError(UIAOperationError):
    """Raised when a required UIA attribute is not available."""
    pass


class UIADriver:
    """Driver class for UIA element operations."""

    @staticmethod
    def _get_uia_wrapper(window_id: int, element_id: str) -> "UiaWrapper":
        """Find and return the UIA element wrapper based on element_id.

        Search strategy:
        1. First try exact match by runtime_id via descendant traversal (most reliable)
        2. Then try pywinauto's conditional search by automation_id
        3. Raise UIAElementNotFoundError if not found

        Args:
            window_id: Parent window handle
            element_id: Element identifier (automation_id or runtime_id)

        Returns:
            Matched pywinauto UIA wrapper (UiaWrapper)

        Raises:
            UIAElementNotFoundError: No matching element found
        """
        desktop = _get_uia_desktop()
        wrapper = desktop.window(handle=window_id)

        def get_runtime_id(info) -> Optional[str]:
            try:
                raw = info if isinstance(info, UIAElementInfo) else getattr(info, "_element", info)
                rid = getattr(raw, "runtime_id", None)
                if rid is not None:
                    return "-".join(str(x) for x in rid)
            except (AttributeError, TypeError) as e:
                _logger.debug("failed to get runtime_id: %s", e)
            except Exception as e:  # pylint: disable=broad-exception-caught
                _logger.debug("unexpected error getting runtime_id: %s", e)
            return None

        def get_automation_id(info) -> Optional[str]:
            try:
                raw = info if isinstance(info, UIAElementInfo) else getattr(info, "_element", info)
                aid = getattr(raw, "automation_id", None)
                if aid:
                    return aid.strip()
            except (AttributeError, TypeError) as e:
                _logger.debug("failed to get automation_id: %s", e)
            except Exception as e:  # pylint: disable=broad-exception-caught
                _logger.debug("unexpected error getting automation_id: %s", e)
            return None

        query = element_id.strip()

        descendants = [wrapper] + wrapper.descendants()
        for candidate in descendants:
            info = candidate.element_info
            rid = get_runtime_id(info)
            if rid == query:
                return candidate
            aid = get_automation_id(info)
            if aid and aid == query:
                return candidate

        try:
            candidate = wrapper.child_window(automation_id=element_id, found_index=0)
            candidate.wait("visible", timeout=DEFAULT_UIA_WAIT_TIMEOUT_SEC)
            return candidate
        except (ElementNotFoundError, PywinautoTimeoutError) as e:
            _logger.debug("child_window search for automation_id=%s failed: %s", element_id, e)
        except Exception as e:  # pylint: disable=broad-exception-caught
            _logger.debug("unexpected error in child_window search: %s", e)

        raise UIAElementNotFoundError(f"UIA element not found: {element_id}")

    @staticmethod
    def click(window_id: int, element_id: str) -> None:
        """Click the UIA element."""
        UIADriver._get_uia_wrapper(window_id, element_id).click()

    @staticmethod
    def invoke(window_id: int, element_id: str) -> None:
        """Invoke the UIA element's Invoke pattern (for buttons, menu items, etc.)."""
        UIADriver._get_uia_wrapper(window_id, element_id).invoke()

    @staticmethod
    def toggle(window_id: int, element_id: str) -> None:
        """Toggle the UIA element's Toggle pattern (for checkboxes)."""
        UIADriver._get_uia_wrapper(window_id, element_id).toggle()

    @staticmethod
    def get_toggle_state(window_id: int, element_id: str) -> int:
        """Get the toggle state of the UIA element.

        Returns:
            0=off, 1=on, 2=indeterminate.

        Note:
            This returns int for UIA TogglePattern, while Win32's is_checked returns
            Optional[bool] (True/False/None). Both patterns match their underlying API conventions:
            - UIA ToggleState enum: ToggleState_Off=0, ToggleState_On=1, ToggleState_Indeterminate=2
            - Win32 checkbox: True=checked, False=unchecked, None=indeterminate
        """
        return UIADriver._get_uia_wrapper(window_id, element_id).get_toggle_state()

    @staticmethod
    def get_text(window_id: int, element_id: str) -> str:
        """Get the text content of the UIA element."""
        return UIADriver._get_uia_wrapper(window_id, element_id).window_text()

    @staticmethod
    def set_text(window_id: int, element_id: str, text: str) -> None:
        """Set the text content of a UIA edit control.

        Args:
            window_id: Parent window handle
            element_id: Element identifier
            text: Text content to set

        Raises:
            UIAOperationError: If text cannot be set via either method
        """
        wrapper = UIADriver._get_uia_wrapper(window_id, element_id)
        try:
            wrapper.set_text(text, 0, len(text))
        except (AttributeError, TypeError) as e:
            _logger.debug("set_text failed, falling back to SetValue: %s", e)
            try:
                wrapper.iface_value.SetValue(text)
            except (AttributeError, TypeError) as inner_e:
                raise UIAOperationError(f"Failed to set text via SetValue: {inner_e}") from inner_e
        except Exception as e:  # pylint: disable=broad-exception-caught
            _logger.debug("set_text failed, falling back to SetValue: %s", e)
            try:
                wrapper.iface_value.SetValue(text)
            except Exception as inner_e:  # pylint: disable=broad-exception-caught
                raise UIAOperationError(f"Failed to set text: {inner_e}") from inner_e

    @staticmethod
    def set_focus(window_id: int, element_id: str) -> None:
        """Set focus to the UIA element."""
        UIADriver._get_uia_wrapper(window_id, element_id).set_focus()

    @staticmethod
    def double_click(window_id: int, element_id: str, button: str = "left") -> None:
        """Double-click the UIA element."""
        UIADriver._get_uia_wrapper(window_id, element_id).double_click_input(button=button)

    @staticmethod
    def right_click(window_id: int, element_id: str) -> None:
        """Right-click the UIA element."""
        UIADriver._get_uia_wrapper(window_id, element_id).right_click_input()

    @staticmethod
    def type_keys(window_id: int, element_id: str, keys: str) -> None:
        """Send key sequence to the UIA element (pywinauto format)."""
        UIADriver._get_uia_wrapper(window_id, element_id).type_keys(keys)

    @staticmethod
    def scroll(window_id: int, element_id: str, direction: str, amount: str = "page", count: int = 1) -> None:
        """Scroll the UIA element.

        Args:
            direction: Scroll direction ("up"/"down"/"left"/"right")
            amount: Scroll amount ("line"/"page")
            count: Number of scrolls
        """
        UIADriver._get_uia_wrapper(window_id, element_id).scroll(direction, amount, count)

    @staticmethod
    def get_value(window_id: int, element_id: str) -> str:
        """Get the current value of the UIA element (via Value pattern)."""
        return UIADriver._get_uia_wrapper(window_id, element_id).iface_value.CurrentValue

    @staticmethod
    def set_value(window_id: int, element_id: str, value: str) -> None:
        """Set the value of the UIA element (via Value pattern)."""
        UIADriver._get_uia_wrapper(window_id, element_id).iface_value.SetValue(value)

    @staticmethod
    def select(window_id: int, element_id: str) -> None:
        """Select the UIA element (for list items, tree items, etc.)."""
        UIADriver._get_uia_wrapper(window_id, element_id).select()

    @staticmethod
    def expand(window_id: int, element_id: str) -> None:
        """Expand the UIA element (for combo boxes, tree nodes, etc.)."""
        UIADriver._get_uia_wrapper(window_id, element_id).expand()

    @staticmethod
    def collapse(window_id: int, element_id: str) -> None:
        """Collapse the UIA element."""
        UIADriver._get_uia_wrapper(window_id, element_id).collapse()

    @staticmethod
    def is_expanded(window_id: int, element_id: str) -> bool:
        """Check whether the UIA element is in expanded state.

        Args:
            window_id: Parent window handle
            element_id: Element identifier

        Returns:
            True if expanded, False otherwise (including on error)
        """
        try:
            return UIADriver._get_uia_wrapper(window_id, element_id).is_expanded()
        except (AttributeError, TypeError):
            return False
        except Exception:  # pylint: disable=broad-exception-caught
            return False

    @staticmethod
    def combo_select(window_id: int, element_id: str, item: int | str) -> None:
        """Select an item in a UIA combobox."""
        UIADriver._get_uia_wrapper(window_id, element_id).select(item)

    @staticmethod
    def _get_combo_items_from_children(wrapper) -> list[str]:
        """Extract items from combobox children (ListItem controls).

        Args:
            wrapper: pywinauto wrapper for the combobox

        Returns:
            List of item text strings
        """
        items: list[str] = []
        try:
            list_items = wrapper.children(control_type="ListItem")
            for item in list_items:
                text = item.window_text()
                if text:
                    items.append(text)
                else:
                    name = getattr(item.element_info, "name", "")
                    if name:
                        items.append(name)
        except (AttributeError, TypeError):
            pass
        except Exception:  # pylint: disable=broad-exception-caught
            pass
        return items

    @staticmethod
    def _get_combo_items_from_nearby_listitems(
        window_id: int,
        _combo_rect,
        combo_left: int,
        combo_right: int,
        combo_top: int,
        combo_bottom: int
    ) -> list[str]:
        """Find ListItem controls near the combobox position (for expanded dropdown lists).

        Args:
            window_id: Parent window handle
            _combo_rect: ComboBox rectangle (unused)
            combo_left: Left edge of combobox
            combo_right: Right edge of combobox
            combo_top: Top edge of combobox
            combo_bottom: Bottom edge of combobox

        Returns:
            List of item text strings found near the combobox
        """
        items: list[str] = []
        try:
            desktop = _get_uia_desktop()
            window = desktop.window(handle=window_id)

            all_list_items = window.children(control_type="ListItem")
            if not all_list_items:
                all_list_items = []
                for child in window.iter_descendants():
                    try:
                        if child.element_info.control_type == "ListItem":
                            all_list_items.append(child)
                    except (AttributeError, TypeError):
                        continue
                    except Exception:  # pylint: disable=broad-exception-caught
                        continue

            for item in all_list_items:
                try:
                    item_rect = item.rectangle()
                    x_near = abs(item_rect.left - combo_left) < 50 or abs(item_rect.left - combo_right) < 50
                    vertical_near = abs(item_rect.bottom - combo_top) < 10 or abs(item_rect.top - combo_bottom) < 10
                    if x_near and vertical_near:
                        text = item.window_text()
                        if text:
                            items.append(text)
                        else:
                            name = getattr(item.element_info, "name", "")
                            if name:
                                items.append(name)
                except (AttributeError, TypeError):
                    continue
                except Exception:  # pylint: disable=broad-exception-caught
                    continue
        except (AttributeError, TypeError):
            pass
        except Exception:  # pylint: disable=broad-exception-caught
            pass
        return items

    @staticmethod
    def _wait_for_dropdown_items(
        wrapper,
        timeout_ms: int = DEFAULT_COMBOBOX_DROPDOWN_TIMEOUT_MS,
        poll_interval_ms: int = DEFAULT_COMBOBOX_POLL_INTERVAL_MS
    ) -> list[str]:
        """Wait for dropdown items to populate with polling.

        Args:
            wrapper: pywinauto wrapper for the combobox
            timeout_ms: Maximum time to wait in milliseconds
            poll_interval_ms: Time between polls in milliseconds

        Returns:
            List of item text strings (may be empty if timeout)
        """
        start_time = time.monotonic()
        timeout_sec = timeout_ms / 1000.0
        poll_interval_sec = poll_interval_ms / 1000.0

        while (time.monotonic() - start_time) < timeout_sec:
            items = UIADriver._get_combo_items_from_children(wrapper)
            if items:
                return items
            time.sleep(poll_interval_sec)

        return []

    @staticmethod
    def combo_items(
        window_id: int,
        element_id: str,
        dropdown_timeout_ms: int = DEFAULT_COMBOBOX_DROPDOWN_TIMEOUT_MS
    ) -> list[str]:
        """Get all item texts in a UIA combobox.

        Strategy:
        1. Try to expand and get ListItem children with polling
        2. If no children, search for ListItem in window near ComboBox position
        3. Fall back to pywinauto's texts() method

        Args:
            window_id: Parent window handle
            element_id: Element identifier
            dropdown_timeout_ms: Maximum time to wait for dropdown to populate (default 500ms)

        Returns:
            List of item text strings
        """
        wrapper = UIADriver._get_uia_wrapper(window_id, element_id)

        combo_rect = None
        combo_left = combo_right = combo_top = combo_bottom = 0
        try:
            combo_rect = wrapper.rectangle()
            combo_left = combo_rect.left
            combo_right = combo_rect.right
            combo_top = combo_rect.top
            combo_bottom = combo_rect.bottom
        except (AttributeError, TypeError):
            pass
        except Exception:  # pylint: disable=broad-exception-caught
            pass

        was_expanded = False
        try:
            was_expanded = wrapper.is_expanded()
        except (AttributeError, TypeError):
            pass
        except Exception:  # pylint: disable=broad-exception-caught
            pass

        if not was_expanded:
            try:
                wrapper.expand()
            except (AttributeError, TypeError):
                pass
            except Exception:  # pylint: disable=broad-exception-caught
                pass

        try:
            items = UIADriver._wait_for_dropdown_items(
                wrapper,
                timeout_ms=dropdown_timeout_ms
            )

            if not items:
                items = UIADriver._get_combo_items_from_nearby_listitems(
                    window_id, combo_rect,
                    combo_left, combo_right, combo_top, combo_bottom
                )

            if items:
                return items

            try:
                texts = wrapper.texts()
                if texts:
                    return texts
            except (AttributeError, TypeError):
                pass
            except Exception:  # pylint: disable=broad-exception-caught
                pass

            return items
        finally:
            if not was_expanded:
                try:
                    wrapper.collapse()
                except (AttributeError, TypeError):
                    pass
                except Exception:  # pylint: disable=broad-exception-caught
                    pass

    @staticmethod
    def combo_selected_text(window_id: int, element_id: str) -> Optional[str]:
        """Get the selected item text in a UIA combobox.

        Args:
            window_id: Parent window handle
            element_id: Element identifier

        Returns:
            Selected item text or None if no selection
        """
        wrapper = UIADriver._get_uia_wrapper(window_id, element_id)
        try:
            return wrapper.selected_text()
        except (AttributeError, TypeError):
            pass
        except Exception:  # pylint: disable=broad-exception-caught
            pass

        try:
            selection = wrapper.get_selection()
            if selection:
                return selection[0].name
        except (AttributeError, TypeError):
            pass
        except Exception:  # pylint: disable=broad-exception-caught
            pass

        return None

    @staticmethod
    def combo_selected_index(window_id: int, element_id: str) -> int:  # pylint: disable=too-many-return-statements
        """Get the selected item index in a UIA combobox.

        Strategy:
        1. Get selected text
        2. Get all items
        3. Find index of selected text in items

        Args:
            window_id: Parent window handle
            element_id: Element identifier

        Returns:
            Selected item index (0-based), or -1 if not found
        """
        wrapper = UIADriver._get_uia_wrapper(window_id, element_id)

        try:
            return wrapper.selected_index()
        except (AttributeError, TypeError):
            pass
        except Exception:  # pylint: disable=broad-exception-caught
            pass

        selected_text = UIADriver.combo_selected_text(window_id, element_id)
        if selected_text is None:
            return -1

        items = UIADriver.combo_items(window_id, element_id)
        try:
            return items.index(selected_text)
        except ValueError:
            pass

        for i, item in enumerate(items):
            if item.lower() == selected_text.lower():
                return i

        return -1

    @staticmethod
    def list_items(window_id: int, element_id: str) -> list[str]:
        """Get all item texts in a UIA list."""
        items = UIADriver._get_uia_wrapper(window_id, element_id).children(content_only=True)
        return [item.window_text() for item in items]

    @staticmethod
    def list_select(window_id: int, element_id: str, item: int | str) -> None:
        """Select an item in a UIA list."""
        UIADriver._get_uia_wrapper(window_id, element_id).get_item(item).select()

    @staticmethod
    def list_selected_items(window_id: int, element_id: str) -> list[str]:
        """Get all selected item texts in a UIA list."""
        selection = UIADriver._get_uia_wrapper(window_id, element_id).get_selection()
        if selection:
            return [elem.name for elem in selection]
        return []

    @staticmethod
    def tab_select(window_id: int, element_id: str, item: int | str) -> None:
        """Select a UIA tab."""
        UIADriver._get_uia_wrapper(window_id, element_id).select(item)

    @staticmethod
    def tab_selected(window_id: int, element_id: str) -> int:
        """Get the selected tab index in a UIA tab control."""
        return UIADriver._get_uia_wrapper(window_id, element_id).get_selected_tab()

    @staticmethod
    def tab_count(window_id: int, element_id: str) -> int:
        """Get the number of tabs in a UIA tab control."""
        return UIADriver._get_uia_wrapper(window_id, element_id).tab_count()

    @staticmethod
    def slider_value(window_id: int, element_id: str) -> float:
        """Get the current value of a UIA slider."""
        return UIADriver._get_uia_wrapper(window_id, element_id).value()

    @staticmethod
    def slider_set_value(window_id: int, element_id: str, value: float) -> None:
        """Set the value of a UIA slider."""
        UIADriver._get_uia_wrapper(window_id, element_id).set_value(value)

    @staticmethod
    def slider_min(window_id: int, element_id: str) -> float:
        """Get the minimum value of a UIA slider."""
        return UIADriver._get_uia_wrapper(window_id, element_id).min_value()

    @staticmethod
    def slider_max(window_id: int, element_id: str) -> float:
        """Get the maximum value of a UIA slider."""
        return UIADriver._get_uia_wrapper(window_id, element_id).max_value()

    @staticmethod
    def snapshot_uia_tree(window_id: int) -> str:
        """Generate a UIA element tree snapshot for the window.

        Recursively traverses all UIA child elements of the target window,
        formatting each element's name, control type, class name, automation ID, etc.
        """
        desktop = _get_uia_desktop()
        wrapper = desktop.window(handle=window_id)
        lines: list[str] = []

        def walk(element: Any, level: int) -> None:
            info = element.element_info
            lines.append(ElementFormatter.format_uia(info, level))
            try:
                for child in element.children():
                    walk(child, level + 1)
            except Exception:  # pylint: disable=broad-exception-caught
                pass

        walk(wrapper, 0)
        return "\n".join(lines)

    @staticmethod
    def get_element_at_point(absolute_x: int, absolute_y: int) -> Optional[dict]:
        """Get UIA element information at the specified screen coordinates.

        Args:
            absolute_x: Absolute X coordinate on screen
            absolute_y: Absolute Y coordinate on screen

        Returns:
            Dictionary with element information or None if no element found
        """
        try:
            element_info = UIAElementInfo.from_point(absolute_x, absolute_y)
            if element_info is None:
                return None

            name = (getattr(element_info, "name", "") or "").strip()
            control_type = (getattr(element_info, "control_type", "") or "").strip() or None
            class_name = (getattr(element_info, "class_name", "") or "").strip() or None
            automation_id = (getattr(element_info, "automation_id", "") or "").strip() or None
            runtime_id = getattr(element_info, "runtime_id", None)

            result = {
                "name": name,
                "control_type": control_type,
                "class_name": class_name,
                "automation_id": automation_id,
            }

            if runtime_id is not None:
                result["runtime_id"] = "-".join(str(x) for x in runtime_id)

            return result
        except Exception as e:  # pylint: disable=broad-exception-caught
            _logger.warning("Failed to get UIA element at point (%d, %d): %s", absolute_x, absolute_y, e)
            return None
