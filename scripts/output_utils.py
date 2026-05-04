#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

"""Output utility functions for winguictl.

Provides functions for formatting and outputting results,
building control information, and generating boundary markers.
"""

import json
import logging
import secrets
from typing import TYPE_CHECKING, Any, Optional

from models import ActionResult, Result, WindowInfo
from win32_utils import Win32API

_logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from uia_driver import UIADriver
    from win32_driver import Win32Driver


def unwrap_result(result: Result, error_prefix: str = "operation failed") -> Any:
    """Unwrap a Result, raising ValueError on error.

    Args:
        result: Result to unwrap
        error_prefix: Prefix for error message

    Returns:
        The success value

    Raises:
        ValueError: If result is an error
    """
    if result.is_ok:
        return result.value
    raise ValueError(f"{error_prefix}: {result.error}")


def emit(payload: dict) -> None:
    """Output result as JSON to standard output."""
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def generate_nonce() -> str:
    """Generate a random nonce for content boundary markers."""
    return secrets.token_hex(8)


def wrap_with_boundary(content: str, nonce: str) -> str:
    """Wrap content with boundary markers to prevent context injection."""
    return f"--- WINGUICTL_CONTENT nonce={nonce} ---\n{content}\n--- END_WINGUICTL_CONTENT nonce={nonce} ---"


def emit_action(ok: bool, verb: str, data: Optional[dict] = None) -> None:
    """Convenience method for outputting operation results, reducing repetitive ActionResult construction code."""
    code = "OK" if ok else "FAILED"
    message = f"{verb} executed" if ok else f"{verb} failed"
    emit(ActionResult(ok=ok, code=code, message=message, data=data or {}).to_dict())


def build_control_info(hwnd: int) -> dict:
    """Build control information for output.

    Args:
        hwnd: Control handle

    Returns:
        Dictionary with control and parent window information
    """
    from win32_driver import Win32Driver

    top_level_hwnd = Win32API.get_top_level_window(hwnd)
    window_title = Win32API.get_window_text(top_level_hwnd)
    control_text = Win32API.get_window_text(hwnd)
    control_class = Win32API.get_class_name(hwnd)
    control_type = Win32Driver.infer_control_type(control_class)

    return {
        "hwnd": str(hwnd),
        "control_text": control_text,
        "control_class": control_class,
        "control_type": control_type,
        "window_id": str(top_level_hwnd),
        "window_title": window_title,
    }


def build_uia_control_info(window_id: int, element_id: str) -> dict:
    """Build UIA element information for output.

    Args:
        window_id: Window handle
        element_id: Element identifier (automation_id or runtime_id)

    Returns:
        Dictionary with element and window information
    """
    window_title = Win32API.get_window_text(window_id)

    return {
        "window_id": str(window_id),
        "window_title": window_title,
        "element_id": element_id,
    }


def build_center_payload(target) -> dict:
    """Build a payload with the element center point as coordinates."""
    center_x = target.bounds.x + (target.bounds.width // 2)
    center_y = target.bounds.y + (target.bounds.height // 2)

    if getattr(target, "source", None) == "image":
        relative_x = center_x
        relative_y = center_y
    else:
        bounds_result = Win32API.get_window_bounds(int(target.window_id))
        window_bounds = bounds_result.value if bounds_result.is_ok else None
        if window_bounds:
            relative_x = center_x - window_bounds.x
            relative_y = center_y - window_bounds.y
        else:
            relative_x = center_x
            relative_y = center_y

    return {
        "window_id": target.window_id,
        "element": target.to_dict(),
        "relative": {"x": relative_x, "y": relative_y},
    }


def format_window_tree(windows: list[WindowInfo]) -> str:
    """Format a list of WindowInfo objects into a hierarchical tree string."""
    window_map = {int(w.window_id): w for w in windows}
    children_map: dict[int, list[int]] = {}
    root_ids: list[int] = []
    for w in windows:
        hwnd = int(w.window_id)
        parent = w.parent_hwnd
        if parent is None or parent == 0 or parent not in window_map:
            root_ids.append(hwnd)
        else:
            if parent not in children_map:
                children_map[parent] = []
            children_map[parent].append(hwnd)

    lines: list[str] = []

    def format_window(hwnd: int, indent: int = 0) -> None:
        w = window_map[hwnd]
        state = ""
        if w.is_minimized:
            state = ' state="minimized"'
        elif w.is_maximized:
            state = ' state="maximized"'
        if w.is_foreground:
            state += ' foreground="true"'
        prefix = "  " * indent
        parts = [f'{prefix}- "{w.title}" [window_id="{w.window_id}"']
        parts.append(f"absolute_rect=({w.bounds.x},{w.bounds.y} {w.bounds.width}x{w.bounds.height})")
        if w.process_id:
            parts.append(f'pid="{w.process_id}"')
        if w.process_name:
            parts.append(f'process="{w.process_name}"')
        if w.parent_hwnd:
            parts.append(f'parent_id="{w.parent_hwnd}"')
        if state:
            parts.append(state.strip())
        lines.append(" ".join(parts) + "]")
        for child_hwnd in children_map.get(hwnd, []):
            format_window(child_hwnd, indent + 1)

    for root_id in root_ids:
        format_window(root_id)
    return "\n".join(lines)


def resolve_window_context(window_id: int) -> tuple[str, "Bounds"]:
    """Resolve window title and bounds, raising ValueError if window not found."""
    window_title = Win32API.get_window_text(window_id)
    bounds_result = Win32API.get_window_bounds(window_id)
    if bounds_result.is_err:
        raise ValueError(f"window not found: {window_id}")
    return window_title, bounds_result.value


def validate_relative_coords(x: int, y: int, bounds: "Bounds") -> None:
    """Validate that relative coordinates are within window bounds.

    Note: This allows coordinates at the edge (bounds.width - 1, bounds.height - 1).
    Window edges may not always be clickable depending on the application,
    but this validation ensures coordinates are at least within the window area.

    Args:
        x: X coordinate relative to window
        y: Y coordinate relative to window
        bounds: Window bounds

    Raises:
        ValueError: If coordinates are outside window bounds
    """
    if x < 0 or x >= bounds.width or y < 0 or y >= bounds.height:
        raise ValueError(f"coordinates ({x}, {y}) are outside window bounds (0-{bounds.width - 1}, 0-{bounds.height - 1})")


def build_point_context(absolute_x: int, absolute_y: int) -> dict[str, Any]:
    """Build element and control info at the given screen coordinates."""
    from uia_driver import UIADriver

    element_at_point = UIADriver.get_element_at_point(absolute_x, absolute_y)
    hwnd_result = Win32API.get_hwnd_from_point(absolute_x, absolute_y)
    hwnd_at_point = hwnd_result.value if hwnd_result.is_ok else None
    control_info = build_control_info(hwnd_at_point) if hwnd_at_point else None
    return {"element_at_point": element_at_point, "control_info": control_info}


def emit_action_result(verb: str, dry_run: bool, data: dict[str, Any]) -> None:
    """Emit an ActionResult for action commands with proper code/message."""
    code = "DRY_RUN" if dry_run else "OK"
    message = f"{verb} preview generated" if dry_run else f"{verb} executed"
    emit(ActionResult(ok=True, code=code, message=message, data=data).to_dict())


def validate_coordinate_pair(x: Optional[int], y: Optional[int], x_name: str, y_name: str) -> None:
    """Validate that coordinate pair is either both provided or both None.

    Args:
        x: X coordinate value
        y: Y coordinate value
        x_name: Name of X parameter for error message
        y_name: Name of Y parameter for error message

    Raises:
        ValueError: If only one coordinate is provided
    """
    if x is not None and y is None:
        raise ValueError(f"{x_name} requires {y_name}")
    if y is not None and x is None:
        raise ValueError(f"{y_name} requires {x_name}")


def validate_positive_int(value: int, name: str) -> None:
    """Validate that a value is a positive integer.

    Args:
        value: Value to validate
        name: Parameter name for error message

    Raises:
        ValueError: If value is not positive
    """
    if value <= 0:
        raise ValueError(f"{name} must be positive, got: {value}")


def validate_threshold(value: float, name: str) -> None:
    """Validate that a value is within [0.0, 1.0] range.

    Args:
        value: Value to validate
        name: Parameter name for error message

    Raises:
        ValueError: If value is outside valid range
    """
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0.0 and 1.0, got: {value}")


def build_error_context(window_id: Optional[int]) -> dict:
    """Build error context with window bounds and available element hints.

    When an operation fails, this provides the agent with enough information
    to diagnose and recover from the error without requiring a separate
    snapshot/find call.

    Args:
        window_id: Window handle (may be None if not yet validated)

    Returns:
        Dictionary with window_bounds and available_elements hints
    """
    context: dict = {}
    if window_id is None:
        return context

    bounds_result = Win32API.get_window_bounds(window_id)
    if bounds_result.is_ok:
        context["window_bounds"] = bounds_result.value.to_dict()

    try:
        from uia_driver import _get_uia_desktop
        desktop = _get_uia_desktop()
        wrapper = desktop.window(handle=window_id)
        hints: list[str] = []
        count = 0
        for child in wrapper.iter_descendants():
            if count >= 10:
                hints.append("...")
                break
            info = child.element_info
            name = (getattr(info, "name", "") or "").strip()
            ct = (getattr(info, "control_type", "") or "").strip()
            aid = (getattr(info, "auto_id", None) or getattr(info, "automation_id", "") or "").strip()
            parts = []
            if name:
                parts.append(f'"{name}"')
            if ct:
                parts.append(f"control_type={ct}")
            if aid:
                parts.append(f"automation_id={aid}")
            if parts:
                hints.append(" ".join(parts))
                count += 1
        if hints:
            context["available_elements_hint"] = hints
    except Exception:  # pylint: disable=broad-exception-caught
        _logger.exception("Failed to collect error context elements")

    return context
