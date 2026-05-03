#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

"""Output utility functions for winguictl.

Provides functions for formatting and outputting results,
building control information, and generating boundary markers.
"""

import json
import secrets
from typing import Any, Optional

from models import ActionResult, WindowInfo
from uia_driver import UIADriver
from win32_driver import Win32Driver
from win32_utils import Win32API


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
    message = "%s executed" % verb if ok else "%s failed" % verb
    emit(ActionResult(ok=ok, code=code, message=message, data=data or {}).to_dict())


def build_control_info(hwnd: int) -> dict:
    """Build control information for output.

    Args:
        hwnd: Control handle

    Returns:
        Dictionary with control and parent window information
    """
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


def build_uia_control_info(window_id: str, element_id: str) -> dict:
    """Build UIA element information for output.

    Args:
        window_id: Window handle string
        element_id: Element identifier (automation_id or runtime_id)

    Returns:
        Dictionary with element and window information
    """
    window_title = Win32API.get_window_text(int(window_id))

    return {
        "window_id": window_id,
        "window_title": window_title,
        "element_id": element_id,
    }


def build_center_payload(target) -> dict:
    """Build a payload with the element center point as coordinates."""
    center_x = target.bounds.x + (target.bounds.width // 2)
    center_y = target.bounds.y + (target.bounds.height // 2)

    window_bounds = Win32API.get_window_bounds(int(target.window_id))
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
        parts.append(f"bounds=({w.bounds.x},{w.bounds.y} {w.bounds.width}x{w.bounds.height})")
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


def resolve_window_context(window_id: str) -> tuple[str, "Bounds"]:
    """Resolve window title and bounds, raising ValueError if window not found."""
    window_title = Win32API.get_window_text(int(window_id))
    bounds = Win32API.get_window_bounds(int(window_id))
    if bounds is None:
        raise ValueError(f"window not found: {window_id}")
    return window_title, bounds


def validate_relative_coords(x: int, y: int, bounds: "Bounds") -> None:
    """Validate that relative coordinates are within window bounds."""
    if x < 0 or x >= bounds.width or y < 0 or y >= bounds.height:
        raise ValueError(f"coordinates ({x}, {y}) are outside window bounds (0-{bounds.width - 1}, 0-{bounds.height - 1})")


def build_point_context(absolute_x: int, absolute_y: int) -> dict[str, Any]:
    """Build element and control info at the given screen coordinates."""
    element_at_point = UIADriver.get_element_at_point(absolute_x, absolute_y)
    hwnd_at_point = Win32API.get_hwnd_from_point(absolute_x, absolute_y)
    control_info = build_control_info(hwnd_at_point) if hwnd_at_point else None
    return {"element_at_point": element_at_point, "control_info": control_info}


def emit_action_result(verb: str, dry_run: bool, data: dict[str, Any]) -> None:
    """Emit an ActionResult for action commands with proper code/message."""
    code = "DRY_RUN" if dry_run else "OK"
    message = "%s preview generated" % verb if dry_run else "%s executed" % verb
    emit(ActionResult(ok=True, code=code, message=message, data=data).to_dict())
