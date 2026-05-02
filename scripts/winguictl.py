#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

"""winguictl - Windows desktop automation command-line tool.

Provides a unified CLI entry point for window management, structure snapshotting,
element finding, interaction operations, control manipulation, and screenshot capture.
"""

import argparse
import json
import secrets
from typing import Optional

from find_driver import FindDriver
from models import ActionResult, ElementFormatter
from ocr_driver import OCRDriver
from uia_driver import UIADriver
from win32_driver import Win32Driver
from win32_utils import Win32API
from windows_driver import WindowsDriver


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(prog="winguictl", description="Windows automation CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    _build_window_parser(subparsers)
    _build_snapshot_parser(subparsers)
    _build_find_parser(subparsers)
    _build_action_parser(subparsers)
    _build_control_parser(subparsers)
    _build_uia_control_parser(subparsers)
    _build_screenshot_parser(subparsers)

    return parser


def _build_window_parser(subparsers) -> None:
    """Build the window subcommand parser."""
    p = subparsers.add_parser("window", help="Inspect and control desktop windows.")
    p.add_argument("--window-id", required=False)
    sp = p.add_subparsers(dest="window_command", required=True)
    sp.add_parser("list", help="List visible windows.")
    sp.add_parser("focus", help="Focus a window (bring to foreground).")
    sp.add_parser("minimize", help="Minimize a window.")
    sp.add_parser("maximize", help="Maximize a window.")
    sp.add_parser("restore", help="Restore a window.")
    sp.add_parser("close", help="Close a window.")
    move = sp.add_parser("move", help="Move a window to a new position.")
    move.add_argument("--x", type=int, required=True)
    move.add_argument("--y", type=int, required=True)
    resize = sp.add_parser("resize", help="Resize a window.")
    resize.add_argument("--width", type=int, required=True)
    resize.add_argument("--height", type=int, required=True)


def _build_snapshot_parser(subparsers) -> None:
    """Build the snapshot subcommand parser."""
    p = subparsers.add_parser("snapshot", help="Capture window structure snapshots.")
    p.add_argument("--window-id", required=True)
    sp = p.add_subparsers(dest="snapshot_command", required=True)
    sp.add_parser("hwnd", help="Snapshot HWND tree of a window.")
    sp.add_parser("uia", help="Snapshot UIA tree of a window.")
    sp.add_parser("ocr", help="Snapshot OCR text regions of a window.")


def _build_find_parser(subparsers) -> None:
    """Build the find subcommand parser."""
    p = subparsers.add_parser("find", help="Resolve text or control targets inside a window.")
    p.add_argument("--window-id", required=True)
    sp = p.add_subparsers(dest="find_command", required=True)

    find_text = sp.add_parser("text", help="Find visible text inside a window.")
    find_text.add_argument("text", help="Text to search for")
    find_text.add_argument("--exact", action="store_true")

    find_uia = sp.add_parser("uia", help="Find UIA controls inside a window.")
    find_uia.add_argument("--text")
    find_uia.add_argument("--control-type")
    find_uia.add_argument("--exact", action="store_true")
    find_uia.add_argument("--max-results", type=int, default=20)

    find_ocr = sp.add_parser("ocr", help="Find OCR text inside a window.")
    find_ocr.add_argument("text", help="Text to search for")
    find_ocr.add_argument("--exact", action="store_true")
    find_ocr.add_argument("--confidence-threshold", type=float, default=0.0)

    find_image = sp.add_parser("image", help="Find an image template inside a window.")
    find_image.add_argument("--image-path", required=True)
    find_image.add_argument("--threshold", type=float, default=0.9)
    find_image.add_argument("--max-results", type=int, default=5)


def _build_action_parser(subparsers) -> None:
    """Build the action subcommand parser."""
    p = subparsers.add_parser("action", help="Preview or run actions against a window.")
    p.add_argument("--window-id", required=True)
    sp = p.add_subparsers(dest="action_command", required=True)

    click = sp.add_parser("click", help="Click at coordinates.")
    click.add_argument("--x", type=int, required=True)
    click.add_argument("--y", type=int, required=True)
    click.add_argument("--dry-run", action="store_true")

    click_image = sp.add_parser("click-image", help="Click the first matching image template.")
    click_image.add_argument("--image-path", required=True)
    click_image.add_argument("--threshold", type=float, default=0.9)
    click_image.add_argument("--dry-run", action="store_true")

    drag = sp.add_parser("drag", help="Drag from one point to another.")
    drag.add_argument("--x1", type=int, required=True)
    drag.add_argument("--y1", type=int, required=True)
    drag.add_argument("--x2", type=int, required=True)
    drag.add_argument("--y2", type=int, required=True)
    drag.add_argument("--duration-ms", type=int, default=500)
    drag.add_argument("--dry-run", action="store_true")

    type_cmd = sp.add_parser("type", help="Type text.")
    type_cmd.add_argument("--text", required=True)
    type_cmd.add_argument("--dry-run", action="store_true")

    press_key = sp.add_parser("press-key", help="Press a single key.")
    press_key.add_argument("--key", required=True)
    press_key.add_argument("--dry-run", action="store_true")

    hotkey = sp.add_parser("hotkey", help="Press a key chord in order.")
    hotkey.add_argument("--keys", nargs="+", required=True)
    hotkey.add_argument("--dry-run", action="store_true")

    clear_text = sp.add_parser("clear-text", help="Clear the currently focused text field.")
    clear_text.add_argument("--dry-run", action="store_true")


def _build_control_parser(subparsers) -> None:
    """Build the control subcommand parser (Win32 control operations)."""
    p = subparsers.add_parser("control", help="Directly control a specific control by hwnd.")
    p.add_argument("--hwnd", required=True, help="Control handle (hwnd).")
    sp = p.add_subparsers(dest="control_command", required=True)

    set_text = sp.add_parser("set-text", help="Set text content of an edit control.")
    set_text.add_argument("text", help="Text to set.")
    sp.add_parser("set-focus", help="Set focus to the control.")
    sp.add_parser("get-text", help="Get text content of an edit control.")
    sp.add_parser("click", help="Click a button control.")
    sp.add_parser("double-click", help="Double click the control.")
    sp.add_parser("right-click", help="Right click the control.")
    sp.add_parser("check", help="Check a checkbox control.")
    sp.add_parser("uncheck", help="Uncheck a checkbox control.")
    sp.add_parser("is-checked", help="Get check state of a checkbox/button control.")

    type_keys = sp.add_parser("type-keys", help="Type keys to the control.")
    type_keys.add_argument("keys", help="Keys to type (pywinauto format).")

    send_chars = sp.add_parser("send-chars", help="Send characters to inactive window.")
    send_chars.add_argument("chars", help="Characters to send.")

    send_keystrokes = sp.add_parser("send-keystrokes", help="Send keystrokes to inactive window.")
    send_keystrokes.add_argument("keystrokes", help="Keystrokes to send (pywinauto format).")

    combo_select = sp.add_parser("combo-select", help="Select an item in a combobox by index or text.")
    combo_select.add_argument("item", help="Item index (0-based) or text to select.")
    sp.add_parser("combo-items", help="Get all items in a combobox.")
    sp.add_parser("combo-selected-index", help="Get selected index in a combobox.")
    sp.add_parser("combo-selected-text", help="Get selected text in a combobox.")

    listbox_select = sp.add_parser("listbox-select", help="Select an item in a listbox by index or text.")
    listbox_select.add_argument("item", help="Item index (0-based) or text to select.")
    sp.add_parser("listbox-items", help="Get all items in a listbox.")
    sp.add_parser("listbox-selected-indices", help="Get selected indices in a listbox.")


def _build_uia_control_parser(subparsers) -> None:
    """Build the uia-control subcommand parser (UIA element operations)."""
    p = subparsers.add_parser("uia-control", help="Control UIA elements by automation_id or runtime_id.")
    p.add_argument("--window-id", required=True, help="Parent window ID.")
    p.add_argument("--element-id", required=True, help="UIA element automation_id or runtime_id.")
    sp = p.add_subparsers(dest="uia_control_command", required=True)

    sp.add_parser("click", help="Click the element.")
    sp.add_parser("double-click", help="Double click the element.")
    sp.add_parser("right-click", help="Right click the element.")
    sp.add_parser("invoke", help="Invoke the element (for buttons, menu items).")
    sp.add_parser("toggle", help="Toggle the element (for checkboxes).")
    sp.add_parser("get-toggle-state", help="Get toggle state (0=off, 1=on, 2=indeterminate).")
    sp.add_parser("get-text", help="Get element text.")

    set_text = sp.add_parser("set-text", help="Set text in edit control.")
    set_text.add_argument("text", help="Text to set.")
    sp.add_parser("set-focus", help="Set focus to the element.")

    type_keys = sp.add_parser("type-keys", help="Type keys to the element.")
    type_keys.add_argument("keys", help="Keys to type (pywinauto format).")

    scroll = sp.add_parser("scroll", help="Scroll the element.")
    scroll.add_argument("direction", choices=["up", "down", "left", "right"], help="Scroll direction.")
    scroll.add_argument("--amount", default="page", choices=["line", "page"], help="Scroll amount.")
    scroll.add_argument("--count", type=int, default=1, help="Scroll count.")

    sp.add_parser("get-value", help="Get element value.")

    set_value = sp.add_parser("set-value", help="Set element value.")
    set_value.add_argument("value", help="Value to set.")

    sp.add_parser("select", help="Select the element (for list items, tree items).")
    sp.add_parser("expand", help="Expand the element (for combo boxes, trees).")
    sp.add_parser("collapse", help="Collapse the element.")
    sp.add_parser("is-expanded", help="Check if element is expanded.")

    combo_select = sp.add_parser("combo-select", help="Select item in combo box.")
    combo_select.add_argument("item", help="Item index or text.")
    sp.add_parser("combo-items", help="Get combo box items.")
    sp.add_parser("combo-selected-text", help="Get selected text in combo box.")
    sp.add_parser("combo-selected-index", help="Get selected index in combo box.")
    sp.add_parser("list-items", help="Get list items.")

    list_select = sp.add_parser("list-select", help="Select item in list.")
    list_select.add_argument("item", help="Item index or text.")
    sp.add_parser("list-selected-items", help="Get selected items in list.")

    tab_select = sp.add_parser("tab-select", help="Select tab by index or text.")
    tab_select.add_argument("item", help="Tab index or text.")
    sp.add_parser("tab-selected", help="Get selected tab index.")
    sp.add_parser("tab-count", help="Get tab count.")
    sp.add_parser("slider-value", help="Get slider value.")

    slider_set = sp.add_parser("slider-set", help="Set slider value.")
    slider_set.add_argument("value", type=float, help="Value to set.")
    sp.add_parser("slider-min", help="Get slider minimum value.")
    sp.add_parser("slider-max", help="Get slider maximum value.")


def _build_screenshot_parser(subparsers) -> None:
    """Build the screenshot subcommand parser."""
    p = subparsers.add_parser("screenshot", help="Take a screenshot of a window.")
    p.add_argument("--window-id", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--x", type=int, help="Left offset relative to window (optional)")
    p.add_argument("--y", type=int, help="Top offset relative to window (optional)")
    p.add_argument("--width", type=int, help="Rectangle width (optional)")
    p.add_argument("--height", type=int, help="Rectangle height (optional)")
    p.add_argument("--dry-run", action="store_true")


def emit(payload: dict) -> None:
    """Output result as JSON to standard output."""
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def _generate_nonce() -> str:
    """Generate a random nonce for content boundary markers."""
    return secrets.token_hex(8)


def _wrap_with_boundary(content: str, nonce: str) -> str:
    """Wrap content with boundary markers to prevent context injection."""
    return "--- WINGUICTL_CONTENT nonce=%s ---\n%s\n--- END_WINGUICTL_CONTENT nonce=%s ---" % (nonce, content, nonce)


def _emit_action(ok: bool, verb: str, data: Optional[dict] = None) -> None:
    """Convenience method for outputting operation results, reducing repetitive ActionResult construction code."""
    code = "OK" if ok else "FAILED"
    message = "%s executed" % verb if ok else "%s failed" % verb
    emit(ActionResult(ok=ok, code=code, message=message, data=data or {}).to_dict())


def _build_center_payload(target) -> dict:
    """Build a payload with the element center point as absolute coordinates."""
    center_x = target.bounds.x + (target.bounds.width // 2)
    center_y = target.bounds.y + (target.bounds.height // 2)
    return {
        "window_id": target.window_id,
        "element": target.to_dict(),
        "absolute": {"x": center_x, "y": center_y},
    }


def _handle_window(args) -> int:
    """Handle window subcommands."""
    if args.window_command == "list":
        windows = WindowsDriver.list_windows()
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
        nonce = _generate_nonce()
        print(_wrap_with_boundary("\n".join(lines), nonce))
        return 0

    action_map = {
        "focus": lambda: WindowsDriver.focus_window(args.window_id),
        "minimize": lambda: WindowsDriver.minimize_window(args.window_id),
        "maximize": lambda: WindowsDriver.maximize_window(args.window_id),
        "restore": lambda: WindowsDriver.restore_window(args.window_id),
        "close": lambda: WindowsDriver.close_window(args.window_id),
        "move": lambda: WindowsDriver.move_window(args.window_id, args.x, args.y),
        "resize": lambda: WindowsDriver.resize_window(args.window_id, args.width, args.height),
    }
    handler = action_map.get(args.window_command)
    if handler is None:
        return -1
    success = handler()
    _emit_action(success, args.window_command)
    return 0


def _handle_snapshot(args) -> int:
    """Handle snapshot subcommands."""
    nonce = _generate_nonce()
    match args.snapshot_command:
        case "hwnd":
            content = Win32Driver.snapshot_hwnd_tree(args.window_id)
            print(_wrap_with_boundary(content, nonce))
        case "uia":
            content = UIADriver.snapshot_uia_tree(args.window_id)
            print(_wrap_with_boundary(content, nonce))
        case "ocr":
            content = OCRDriver.snapshot_ocr(args.window_id)
            print(_wrap_with_boundary(content, nonce))
        case _:
            return -1
    return 0


def _handle_find(args) -> int:
    """Handle find subcommands."""
    nonce = _generate_nonce()
    match args.find_command:
        case "text":
            content = FindDriver.find_text(args.window_id, args.text, exact=args.exact)
            print(_wrap_with_boundary(content, nonce))
        case "uia":
            content = FindDriver.find_uia(args.window_id, text=args.text, control_type=args.control_type, exact=args.exact, max_results=args.max_results)
            print(_wrap_with_boundary(content, nonce))
        case "ocr":
            result = OCRDriver.find_ocr_text(args.window_id, args.text, exact=args.exact, confidence_threshold=args.confidence_threshold)
            content = "\n".join(ElementFormatter.format_element(m) for m in result)
            print(_wrap_with_boundary(content, nonce))
        case "image":
            result = FindDriver.find_image(window_id=args.window_id, image_path=args.image_path, threshold=args.threshold, max_results=args.max_results)
            content = "\n".join(ElementFormatter.format_element(m) for m in result) if result else ""
            print(_wrap_with_boundary(content, nonce))
        case _:
            return -1
    return 0


def _handle_action(args) -> int:
    """Handle action subcommands."""
    match args.action_command:
        case "click":
            if args.dry_run:
                emit(ActionResult(ok=True, code="DRY_RUN", message="click preview generated", data={"window_id": args.window_id, "x": args.x, "y": args.y}).to_dict())
            else:
                bounds = Win32API.get_window_bounds(int(args.window_id))
                if bounds is None:
                    raise ValueError("window not found: %s" % args.window_id)
                WindowsDriver.focus_window(args.window_id)
                absolute_x = bounds.x + args.x
                absolute_y = bounds.y + args.y
                Win32API.send_click(absolute_x, absolute_y)
                emit(ActionResult(ok=True, code="OK", message="click executed", data={"window_id": args.window_id, "relative": {"x": args.x, "y": args.y}, "absolute": {"x": absolute_x, "y": absolute_y}}).to_dict())
        case "click-image":
            matches = FindDriver.find_image(window_id=args.window_id, image_path=args.image_path, threshold=args.threshold)
            if not matches:
                raise ValueError("image target not found: %s" % args.image_path)
            target = matches[0]
            payload = _build_center_payload(target)
            if args.dry_run:
                emit(ActionResult(ok=True, code="DRY_RUN", message="click_image preview generated", data=payload).to_dict())
            else:
                WindowsDriver.focus_window(target.window_id)
                Win32API.send_click(payload["absolute"]["x"], payload["absolute"]["y"])
                emit(ActionResult(ok=True, code="OK", message="click_image executed", data=payload).to_dict())
        case "drag":
            if args.dry_run:
                emit(ActionResult(ok=True, code="DRY_RUN", message="drag preview generated", data={"window_id": args.window_id, "from": {"x": args.x1, "y": args.y1}, "to": {"x": args.x2, "y": args.y2}, "duration_ms": args.duration_ms}).to_dict())
            else:
                bounds = Win32API.get_window_bounds(int(args.window_id))
                if bounds is None:
                    raise ValueError("window not found: %s" % args.window_id)
                WindowsDriver.focus_window(args.window_id)
                absolute_x1 = bounds.x + args.x1
                absolute_y1 = bounds.y + args.y1
                absolute_x2 = bounds.x + args.x2
                absolute_y2 = bounds.y + args.y2
                Win32API.send_drag(absolute_x1, absolute_y1, absolute_x2, absolute_y2, duration_ms=args.duration_ms)
                emit(ActionResult(ok=True, code="OK", message="drag executed", data={"window_id": args.window_id, "from": {"relative": {"x": args.x1, "y": args.y1}, "absolute": {"x": absolute_x1, "y": absolute_y1}}, "to": {"relative": {"x": args.x2, "y": args.y2}, "absolute": {"x": absolute_x2, "y": absolute_y2}}, "duration_ms": args.duration_ms}).to_dict())
        case "type":
            if args.dry_run:
                emit(ActionResult(ok=True, code="DRY_RUN", message="type_text preview generated", data={"window_id": args.window_id, "text": args.text, "length": len(args.text)}).to_dict())
            else:
                WindowsDriver.focus_window(args.window_id)
                Win32API.send_type_text(args.text)
                emit(ActionResult(ok=True, code="OK", message="type_text executed", data={"window_id": args.window_id, "text": args.text, "length": len(args.text)}).to_dict())
        case "press-key":
            if args.dry_run:
                emit(ActionResult(ok=True, code="DRY_RUN", message="press_key preview generated", data={"window_id": args.window_id, "key": args.key}).to_dict())
            else:
                WindowsDriver.focus_window(args.window_id)
                Win32API.send_press_key(args.key)
                emit(ActionResult(ok=True, code="OK", message="press_key executed", data={"window_id": args.window_id, "key": args.key}).to_dict())
        case "hotkey":
            if args.dry_run:
                emit(ActionResult(ok=True, code="DRY_RUN", message="hotkey preview generated", data={"window_id": args.window_id, "keys": args.keys}).to_dict())
            else:
                WindowsDriver.focus_window(args.window_id)
                Win32API.send_hotkey(args.keys)
                emit(ActionResult(ok=True, code="OK", message="hotkey executed", data={"window_id": args.window_id, "keys": args.keys}).to_dict())
        case "clear-text":
            if args.dry_run:
                emit(ActionResult(ok=True, code="DRY_RUN", message="clear_text preview generated", data={"window_id": args.window_id}).to_dict())
            else:
                WindowsDriver.focus_window(args.window_id)
                Win32API.send_hotkey(["ctrl", "a"])
                Win32API.send_press_key("delete")
                emit(ActionResult(ok=True, code="OK", message="clear_text executed", data={"window_id": args.window_id}).to_dict())
        case _:
            return -1
    return 0


def _handle_control(args) -> int:
    """处理 control 子命令（Win32 控件操作）。"""
    hwnd = int(args.hwnd)
    match args.control_command:
        case "set-text":
            Win32Driver.set_text(hwnd, args.text)
            _emit_action(True, "set_text")
        case "set-focus":
            Win32Driver.set_focus(hwnd)
            _emit_action(True, "set_focus")
        case "get-text":
            text = Win32Driver.get_text(hwnd)
            _emit_action(True, "get_text", {"text": text})
        case "click":
            Win32Driver.click(hwnd)
            _emit_action(True, "click")
        case "double-click":
            Win32Driver.double_click(hwnd)
            _emit_action(True, "double_click")
        case "right-click":
            Win32Driver.right_click(hwnd)
            _emit_action(True, "right_click")
        case "check":
            Win32Driver.check(hwnd)
            _emit_action(True, "check")
        case "uncheck":
            Win32Driver.uncheck(hwnd)
            _emit_action(True, "uncheck")
        case "is-checked":
            checked = Win32Driver.is_checked(hwnd)
            _emit_action(True, "is_checked", {"checked": checked})
        case "type-keys":
            Win32Driver.type_keys(hwnd, args.keys)
            _emit_action(True, "type_keys")
        case "send-chars":
            Win32Driver.send_chars(hwnd, args.chars)
            _emit_action(True, "send_chars")
        case "send-keystrokes":
            Win32Driver.send_keystrokes(hwnd, args.keystrokes)
            _emit_action(True, "send_keystrokes")
        case "combo-select":
            Win32Driver.combo_select(hwnd, args.item)
            _emit_action(True, "combo_select")
        case "combo-items":
            items = Win32Driver.combo_items(hwnd)
            _emit_action(True, "combo_items", {"items": items})
        case "combo-selected-index":
            index = Win32Driver.combo_selected_index(hwnd)
            _emit_action(True, "combo_selected_index", {"index": index})
        case "combo-selected-text":
            text = Win32Driver.combo_selected_text(hwnd)
            _emit_action(True, "combo_selected_text", {"text": text})
        case "listbox-select":
            Win32Driver.listbox_select(hwnd, args.item)
            _emit_action(True, "listbox_select")
        case "listbox-items":
            items = Win32Driver.listbox_items(hwnd)
            _emit_action(True, "listbox_items", {"items": items})
        case "listbox-selected-indices":
            indices = Win32Driver.listbox_selected_indices(hwnd)
            _emit_action(True, "listbox_selected_indices", {"indices": indices})
        case _:
            return -1
    return 0


def _handle_uia_control(args) -> int:
    """Handle uia-control subcommands (UIA element operations)."""
    wid = args.window_id
    eid = args.element_id
    match args.uia_control_command:
        case "click":
            UIADriver.click(wid, eid)
            _emit_action(True, "click")
        case "double-click":
            UIADriver.double_click(wid, eid)
            _emit_action(True, "double_click")
        case "right-click":
            UIADriver.right_click(wid, eid)
            _emit_action(True, "right_click")
        case "invoke":
            UIADriver.invoke(wid, eid)
            _emit_action(True, "invoke")
        case "toggle":
            UIADriver.toggle(wid, eid)
            _emit_action(True, "toggle")
        case "get-toggle-state":
            state = UIADriver.get_toggle_state(wid, eid)
            _emit_action(True, "get_toggle_state", {"state": state})
        case "get-text":
            text = UIADriver.get_text(wid, eid)
            _emit_action(True, "get_text", {"text": text})
        case "set-text":
            UIADriver.set_text(wid, eid, args.text)
            _emit_action(True, "set_text")
        case "set-focus":
            UIADriver.set_focus(wid, eid)
            _emit_action(True, "set_focus")
        case "type-keys":
            UIADriver.type_keys(wid, eid, args.keys)
            _emit_action(True, "type_keys")
        case "scroll":
            UIADriver.scroll(wid, eid, args.direction, args.amount, args.count)
            _emit_action(True, "scroll")
        case "get-value":
            value = UIADriver.get_value(wid, eid)
            _emit_action(True, "get_value", {"value": value})
        case "set-value":
            UIADriver.set_value(wid, eid, args.value)
            _emit_action(True, "set_value")
        case "select":
            UIADriver.select(wid, eid)
            _emit_action(True, "select")
        case "expand":
            UIADriver.expand(wid, eid)
            _emit_action(True, "expand")
        case "collapse":
            UIADriver.collapse(wid, eid)
            _emit_action(True, "collapse")
        case "is-expanded":
            expanded = UIADriver.is_expanded(wid, eid)
            _emit_action(True, "is_expanded", {"expanded": expanded})
        case "combo-select":
            UIADriver.combo_select(wid, eid, args.item)
            _emit_action(True, "combo_select")
        case "combo-items":
            items = UIADriver.combo_items(wid, eid)
            _emit_action(True, "combo_items", {"items": items})
        case "combo-selected-text":
            text = UIADriver.combo_selected_text(wid, eid)
            _emit_action(True, "combo_selected_text", {"text": text})
        case "combo-selected-index":
            index = UIADriver.combo_selected_index(wid, eid)
            _emit_action(True, "combo_selected_index", {"index": index})
        case "list-items":
            items = UIADriver.list_items(wid, eid)
            _emit_action(True, "list_items", {"items": items})
        case "list-select":
            UIADriver.list_select(wid, eid, args.item)
            _emit_action(True, "list_select")
        case "list-selected-items":
            items = UIADriver.list_selected_items(wid, eid)
            _emit_action(True, "list_selected_items", {"items": items})
        case "tab-select":
            UIADriver.tab_select(wid, eid, args.item)
            _emit_action(True, "tab_select")
        case "tab-selected":
            index = UIADriver.tab_selected(wid, eid)
            _emit_action(True, "tab_selected", {"index": index})
        case "tab-count":
            count = UIADriver.tab_count(wid, eid)
            _emit_action(True, "tab_count", {"count": count})
        case "slider-value":
            value = UIADriver.slider_value(wid, eid)
            _emit_action(True, "slider_value", {"value": value})
        case "slider-set":
            UIADriver.slider_set_value(wid, eid, args.value)
            _emit_action(True, "slider_set_value")
        case "slider-min":
            value = UIADriver.slider_min(wid, eid)
            _emit_action(True, "slider_min", {"value": value})
        case "slider-max":
            value = UIADriver.slider_max(wid, eid)
            _emit_action(True, "slider_max", {"value": value})
        case _:
            return -1
    return 0


def _handle_screenshot(args) -> int:
    """Handle screenshot subcommands."""
    rect = None
    if args.x is not None and args.y is not None and args.width is not None and args.height is not None:
        rect = (args.x, args.y, args.width, args.height)
    if args.dry_run:
        emit(ActionResult(ok=True, code="DRY_RUN", message="screenshot preview generated", data={"window_id": args.window_id, "output": args.output, "rect": rect}).to_dict())
    else:
        output_path = WindowsDriver.screenshot_window(args.window_id, args.output, rect)
        emit(ActionResult(ok=True, code="OK", message="screenshot executed", data={"window_id": args.window_id, "output": output_path}).to_dict())
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """CLI main entry function."""
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        handler_map = {
            "window": _handle_window,
            "snapshot": _handle_snapshot,
            "find": _handle_find,
            "action": _handle_action,
            "control": _handle_control,
            "uia-control": _handle_uia_control,
            "screenshot": _handle_screenshot,
        }
        handler = handler_map.get(args.command)
        if handler is None:
            parser.error("unknown command: %s" % args.command)
            return 1
        result = handler(args)
        return result if result >= 0 else 1
    except Exception as e:
        emit(ActionResult(ok=False, code="ERROR", message=str(e)).to_dict())
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
