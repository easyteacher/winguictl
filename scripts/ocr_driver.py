#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

"""OCR text recognition driver module.

Performs text recognition on window screenshots using WeChat OCR engine,
supporting both full-window OCR snapshots and text finding modes.
Depends on wx_ocr library and Pillow library.
"""

import os
import tempfile
from typing import Optional

import wx_ocr
from PIL import Image

from models import Bounds, ElementFormatter, ElementInfo
from win32_utils import Win32API


class OCRDriver:

    @staticmethod
    def _capture_and_ocr(window_id: str) -> list[dict]:
        """Capture window screenshot and perform OCR recognition.

        Saves window screenshot to a temporary PNG file, calls wx_ocr for text recognition,
        and automatically deletes the temporary file after recognition.

        Args:
            window_id: Window handle string

        Returns:
            OCR result list, each item contains "text" and "location" fields

        Raises:
            RuntimeError: OCR recognition failed
        """
        hwnd = int(window_id)
        _, _, width, height, data = Win32API.capture_window_bgra(hwnd)
        rgb_data = bytearray()
        for i in range(0, len(data), 4):
            rgb_data.extend([data[i + 2], data[i + 1], data[i]])
        image = Image.frombytes("RGB", (width, height), bytes(rgb_data))
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name
        image.save(tmp_path)
        try:
            result = wx_ocr.ocr(tmp_path)
            return result if isinstance(result, list) else []
        except Exception as e:
            raise RuntimeError("WeChat OCR failed: %s" % e) from e
        finally:
            os.unlink(tmp_path)

    @staticmethod
    def snapshot_ocr(window_id: str) -> str:
        """Generate an OCR text snapshot for the window.

        Performs OCR recognition on the window screenshot, formatting each
        recognized text segment with its position and size information.
        """
        results = OCRDriver._capture_and_ocr(window_id)
        lines: list[str] = []
        for r in results:
            text = r.get("text", "")
            loc = r.get("location", {})
            left = int(loc.get("left") or 0)
            top = int(loc.get("top") or 0)
            right = int(loc.get("right") or 0)
            bottom = int(loc.get("bottom") or 0)
            lines.append(ElementFormatter.format_ocr(text, left, top, right - left, bottom - top))
        return "\n".join(lines)

    @staticmethod
    def find_ocr_text(
        window_id: str,
        text: str,
        exact: bool = False,
        confidence_threshold: float = 0.0,
    ) -> list[ElementInfo]:
        """Find specified text in the window via OCR.

        Args:
            window_id: Window handle string
            text: Text to find
            exact: Whether to match exactly (default is fuzzy match)
            confidence_threshold: Confidence threshold (reserved parameter)

        Returns:
            List of matching ElementInfo
        """
        results = OCRDriver._capture_and_ocr(window_id)
        matches: list[ElementInfo] = []
        query = text.strip().casefold()
        for r in results:
            candidate = (r.get("text", "") or "").strip()
            if not candidate:
                continue
            if exact:
                if candidate.casefold() != query:
                    continue
            else:
                if query not in candidate.casefold():
                    continue
            loc = r.get("location", {})
            left = int(loc.get("left") or 0)
            top = int(loc.get("top") or 0)
            right = int(loc.get("right") or 0)
            bottom = int(loc.get("bottom") or 0)
            matches.append(
                ElementInfo(
                    element_id="ocr-%s" % id(r),
                    window_id=str(int(window_id)),
                    text=candidate,
                    bounds=Bounds(x=left, y=top, width=right - left, height=bottom - top),
                    source="ocr",
                    confidence=0.9,
                )
            )
        return matches
