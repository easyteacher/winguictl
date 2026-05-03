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
from typing import Optional

from models import ActionResult
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
    return "--- WINGUICTL_CONTENT nonce=%s ---\n%s\n--- END_WINGUICTL_CONTENT nonce=%s ---" % (nonce, content, nonce)


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
