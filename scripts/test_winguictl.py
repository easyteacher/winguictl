#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

"""Unit tests for winguictl."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from constants import VK_CODE_MAP, WIN32_CONTROL_TYPE_MAP
from models import Bounds, ElementInfo, WindowInfo, ActionResult, ElementFormatter
from win32_driver import Win32Driver


class TestConstants:
    """Tests for constants module."""

    def test_vk_code_map_contains_common_keys(self):
        assert "enter" in VK_CODE_MAP
        assert "tab" in VK_CODE_MAP
        assert "esc" in VK_CODE_MAP
        assert "space" in VK_CODE_MAP
        assert "ctrl" in VK_CODE_MAP
        assert "shift" in VK_CODE_MAP
        assert "alt" in VK_CODE_MAP

    def test_vk_code_map_function_keys(self):
        for i in range(1, 13):
            assert f"f{i}" in VK_CODE_MAP

    def test_vk_code_map_letters(self):
        for c in "abcdefghijklmnopqrstuvwxyz":
            assert c in VK_CODE_MAP

    def test_vk_code_map_digits(self):
        for d in "0123456789":
            assert d in VK_CODE_MAP

    def test_win32_control_type_map_common_classes(self):
        assert "Button" in WIN32_CONTROL_TYPE_MAP
        assert "Edit" in WIN32_CONTROL_TYPE_MAP
        assert "ComboBox" in WIN32_CONTROL_TYPE_MAP
        assert "ListBox" in WIN32_CONTROL_TYPE_MAP


class TestModels:
    """Tests for models module."""

    def test_bounds_from_rect(self):
        class MockRect:
            left = 100
            top = 200
            right = 400
            bottom = 500

        bounds = Bounds.from_rect(MockRect())
        assert bounds.x == 100
        assert bounds.y == 200
        assert bounds.width == 300
        assert bounds.height == 300

    def test_bounds_to_dict(self):
        bounds = Bounds(x=10, y=20, width=100, height=200)
        d = bounds.to_dict()
        assert d == {"x": 10, "y": 20, "width": 100, "height": 200}

    def test_window_info_to_dict(self):
        bounds = Bounds(x=0, y=0, width=800, height=600)
        info = WindowInfo(
            window_id="12345",
            title="Test Window",
            bounds=bounds,
            process_id=1234,
            process_name="test.exe",
        )
        d = info.to_dict()
        assert d["window_id"] == "12345"
        assert d["title"] == "Test Window"
        assert d["process_id"] == 1234
        assert d["process_name"] == "test.exe"

    def test_element_info_to_dict(self):
        bounds = Bounds(x=100, y=100, width=50, height=30)
        info = ElementInfo(
            element_id="btn1",
            window_id="12345",
            text="Click Me",
            bounds=bounds,
            control_type="Button",
        )
        d = info.to_dict()
        assert d["element_id"] == "btn1"
        assert d["text"] == "Click Me"
        assert d["control_type"] == "Button"

    def test_action_result_to_dict(self):
        result = ActionResult(ok=True, code="OK", message="Success", data={"key": "value"})
        d = result.to_dict()
        assert d["ok"] is True
        assert d["code"] == "OK"
        assert d["message"] == "Success"
        assert d["data"] == {"key": "value"}


class TestElementFormatter:
    """Tests for ElementFormatter class."""

    def test_format_basic(self):
        formatter = ElementFormatter(text="Hello")
        result = formatter.format()
        assert '- "Hello"' in result

    def test_format_with_rect(self):
        formatter = ElementFormatter(text="Button", rect=(10, 20, 100, 50))
        result = formatter.format()
        assert '- "Button"' in result
        assert "rect=(10,20 100x50)" in result

    def test_format_with_control_type(self):
        formatter = ElementFormatter(text="Submit", control_type="Button")
        result = formatter.format()
        assert 'control_type="Button"' in result

    def test_format_with_hwnd(self):
        formatter = ElementFormatter(text="Window", hwnd=12345)
        result = formatter.format()
        assert 'hwnd="12345"' in result

    def test_format_with_confidence(self):
        formatter = ElementFormatter(text="Match", confidence=0.95)
        result = formatter.format()
        assert "confidence=0.95" in result

    def test_format_ocr(self):
        result = ElementFormatter.format_ocr("Text", 10, 20, 100, 30, confidence=0.9)
        assert '- "Text"' in result
        assert "rect=(10,20 100x30)" in result
        assert "confidence=0.90" in result


class TestWin32Driver:
    """Tests for Win32Driver class."""

    def test_infer_control_type_exact_match(self):
        assert Win32Driver.infer_control_type("Button") == "Button"
        assert Win32Driver.infer_control_type("Edit") == "Edit"
        assert Win32Driver.infer_control_type("ComboBox") == "ComboBox"

    def test_infer_control_type_case_insensitive(self):
        assert Win32Driver.infer_control_type("button") == "Button"
        assert Win32Driver.infer_control_type("BUTTON") == "Button"
        assert Win32Driver.infer_control_type("edit") == "Edit"

    def test_infer_control_type_prefix_match_with_delimiter(self):
        assert Win32Driver.infer_control_type("Button.Extra") == "Button"
        assert Win32Driver.infer_control_type("Edit_Something") == "Edit"
        assert Win32Driver.infer_control_type("ComboBoxItem") is None

    def test_infer_control_type_no_match(self):
        assert Win32Driver.infer_control_type("CustomClass") is None
        assert Win32Driver.infer_control_type("") is None
        assert Win32Driver.infer_control_type(None) is None

    def test_infer_control_type_short_prefix_requires_delimiter(self):
        assert Win32Driver.infer_control_type("TButton.Extra") == "Button"
        assert Win32Driver.infer_control_type("TButtonExtra") is None


class TestOutputUtils:
    """Tests for output_utils module."""

    def test_generate_nonce(self):
        from output_utils import generate_nonce

        nonce1 = generate_nonce()
        nonce2 = generate_nonce()
        assert len(nonce1) == 16
        assert len(nonce2) == 16
        assert nonce1 != nonce2

    def test_wrap_with_boundary(self):
        from output_utils import wrap_with_boundary

        content = "test content"
        nonce = "abcd1234"
        result = wrap_with_boundary(content, nonce)
        assert "--- WINGUICTL_CONTENT nonce=abcd1234 ---" in result
        assert "--- END_WINGUICTL_CONTENT nonce=abcd1234 ---" in result
        assert "test content" in result

    def test_emit_action(self):
        from output_utils import emit_action
        import io
        import sys

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            emit_action(True, "test", {"key": "value"})
            output = sys.stdout.getvalue()
            assert '"ok": true' in output
            assert '"code": "OK"' in output
            assert '"message": "test executed"' in output
        finally:
            sys.stdout = old_stdout


class TestCLI:
    """Tests for CLI argument parsing."""

    def test_build_parser(self):
        from winguictl import build_parser

        parser = build_parser()
        assert parser.prog == "winguictl"

    def test_window_list_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["window", "list"])
        assert args.command == "window"
        assert args.window_command == "list"

    def test_window_focus_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["window", "--window-id", "12345", "focus"])
        assert args.command == "window"
        assert args.window_command == "focus"
        assert args.window_id == 12345

    def test_snapshot_uia_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["snapshot", "--window-id", "12345", "uia"])
        assert args.command == "snapshot"
        assert args.snapshot_command == "uia"
        assert args.window_id == 12345

    def test_find_text_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["find", "--window-id", "12345", "text", "Submit"])
        assert args.command == "find"
        assert args.find_command == "text"
        assert args.text == "Submit"

    def test_action_click_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["action", "--window-id", "12345", "click", "--x", "100", "--y", "200"])
        assert args.command == "action"
        assert args.action_command == "click"
        assert args.x == 100
        assert args.y == 200

    def test_action_type_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["action", "--window-id", "12345", "type", "--text", "Hello"])
        assert args.command == "action"
        assert args.action_command == "type"
        assert args.text == "Hello"

    def test_control_click_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["control", "--hwnd", "12345", "click"])
        assert args.command == "control"
        assert args.control_command == "click"
        assert args.hwnd == 12345

    def test_uia_control_click_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["uia-control", "--window-id", "12345", "--element-id", "btn1", "click"])
        assert args.command == "uia-control"
        assert args.uia_control_command == "click"
        assert args.window_id == 12345
        assert args.element_id == "btn1"

    def test_screenshot_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["screenshot", "--window-id", "12345", "--output", "test.png"])
        assert args.command == "screenshot"
        assert args.window_id == 12345
        assert args.output == "test.png"

    def test_verbose_flag(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["--verbose", "window", "list"])
        assert args.verbose is True

    def test_dry_run_flag(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["action", "--window-id", "12345", "click", "--x", "100", "--y", "200", "--dry-run"])
        assert args.dry_run is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
