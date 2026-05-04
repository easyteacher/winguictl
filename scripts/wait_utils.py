#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

"""Wait utility functions for condition checking.

Provides helper functions for checking various conditions:
- Window existence
- Text presence
- UIA element presence
- OCR text presence
- Image presence
"""

import logging
from typing import Optional

from find_driver import FindDriver
from ocr_driver import OCRDriver
from win32_utils import Win32API
from windows_driver import WindowsDriver

_logger = logging.getLogger(__name__)


class WaitUtils:
    """Utility class for checking wait conditions."""

    @staticmethod
    def check_window_exists(title: str, exact: bool, class_name: Optional[str] = None) -> Optional[int]:
        """Check if window exists and return its handle, or None if not found.

        Args:
            title: Window title to match (supports partial match by default)
            exact: Whether to match title exactly
            class_name: Optional window class name filter

        Returns:
            Window handle if found, None otherwise
        """
        windows = WindowsDriver.list_windows()
        title_lower = title.casefold()
        for win in windows:
            win_title = (win.title or "").strip()
            win_title_lower = win_title.casefold()
            if exact:
                if win_title_lower != title_lower:
                    continue
            else:
                if title_lower not in win_title_lower:
                    continue
            if class_name:
                actual_class = Win32API.get_class_name(int(win.window_id))
                if actual_class and class_name.casefold() not in actual_class.casefold():
                    continue
            return int(win.window_id)
        return None

    @staticmethod
    def check_text_exists(window_id: int, text: str, exact: bool) -> bool:
        """Check if text exists in window.

        Args:
            window_id: Window handle
            text: Text to search for
            exact: Whether to match exactly

        Returns:
            True if text found, False otherwise
        """
        try:
            result = FindDriver.find_text(window_id, text, exact)
            return bool(result.strip())
        except Exception:  # pylint: disable=broad-exception-caught
            _logger.exception("Failed to check text existence in window %d", window_id)
            return False

    @staticmethod
    def check_uia_exists(
        window_id: int,
        text: Optional[str] = None,
        control_type: Optional[str] = None,
        class_name: Optional[str] = None,
        automation_id: Optional[str] = None,
        exact: bool = False,
    ) -> bool:
        """Check if UIA element exists in window.

        Args:
            window_id: Window handle
            text: Optional element text/name filter
            control_type: Optional control type filter
            class_name: Optional window class name filter
            automation_id: Optional automation ID filter
            exact: Whether to match text exactly

        Returns:
            True if element found, False otherwise
        """
        try:
            result = FindDriver.find_uia(
                window_id=window_id,
                text=text,
                control_type=control_type,
                class_name=class_name,
                automation_id=automation_id,
                exact=exact,
                skip_actions=True,
                skip_state=True,
            )
            return bool(result.strip())
        except Exception:  # pylint: disable=broad-exception-caught
            _logger.exception("Failed to check UIA element existence in window %d", window_id)
            return False

    @staticmethod
    def check_ocr_exists(window_id: int, text: str, exact: bool, confidence: float = 0.0) -> bool:
        """Check if OCR text exists in window.

        Args:
            window_id: Window handle
            text: Text to search for
            exact: Whether to match exactly
            confidence: OCR confidence threshold (default: 0.0)

        Returns:
            True if text found, False otherwise
        """
        try:
            matches = OCRDriver.find_ocr_text(window_id, text, exact, confidence)
            return len(matches) > 0
        except Exception:  # pylint: disable=broad-exception-caught
            _logger.exception("Failed to check OCR text existence in window %d", window_id)
            return False

    @staticmethod
    def check_image_exists(window_id: int, image_path: str, threshold: float = 0.9) -> bool:
        """Check if image exists in window.

        Args:
            window_id: Window handle
            image_path: Path to template image file
            threshold: Match confidence threshold (default: 0.9)

        Returns:
            True if image found, False otherwise
        """
        try:
            matches = FindDriver.find_image(window_id, image_path, threshold)
            return len(matches) > 0
        except Exception:  # pylint: disable=broad-exception-caught
            _logger.exception("Failed to check image existence in window %d", window_id)
            return False
