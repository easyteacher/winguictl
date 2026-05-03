#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

"""Element finding driver module.

Provides multiple element finding strategies:
- find_text: Find text through UIA or Win32 enumeration
- find_uia: Find controls through UIA tree
- find_image: Find images through OpenCV template matching
"""

import win32gui
from pathlib import Path
from typing import Any, Optional

from pywinauto import Desktop

from models import Bounds, ElementFormatter, ElementInfo
from win32_utils import Win32API


class FindDriver:

    @staticmethod
    def find_text(window_id: str, text: str, exact: bool = False) -> str:
        """Find specified text in the window.

        Prioritizes UIA tree search; falls back to Win32 enumeration if no results found.

        Args:
            window_id: Window handle string
            text: Text to find
            exact: Whether to match exactly

        Returns:
            Formatted matching result string
        """
        query = text.strip()
        if not query:
            raise ValueError("text query must not be empty")
        hwnd = int(window_id)
        matches: list[ElementInfo] = []
        lowered_query = query.casefold()

        try:
            desktop = Desktop(backend="uia")
            wrapper = desktop.window(handle=hwnd)
            for child in wrapper.descendants():
                try:
                    info = child.element_info
                    name = (getattr(info, "name", "") or "").strip()
                    if not name:
                        continue
                    lowered = name.casefold()
                    is_match = lowered == lowered_query if exact else lowered_query in lowered
                    if not is_match:
                        continue
                    rect = getattr(info, "rectangle", None)
                    if rect is None:
                        continue
                    control_id = getattr(info, "control_id", None)
                    runtime_id_raw = getattr(info, "runtime_id", None)
                    runtime_id = "-".join(str(x) for x in runtime_id_raw) if runtime_id_raw else None
                    matches.append(
                        ElementInfo(
                            element_id=str(getattr(info, "handle", None) or id(info)),
                            window_id=str(hwnd),
                            text=name,
                            bounds=Bounds.from_rect(rect),
                            class_name=(getattr(info, "class_name", "") or "").strip() or None,
                            control_type="uia-text",
                            control_id=control_id,
                            runtime_id=runtime_id,
                            source="uia",
                            confidence=1.0 if exact else 0.95,
                        )
                    )
                except Exception:
                    continue
        except Exception:
            pass

        if not matches:
            matches = FindDriver._find_text_win32(hwnd, text, exact)
        return "\n".join(ElementFormatter.format_element(m) for m in matches)

    @staticmethod
    def _find_text_win32(hwnd: int, text: str, exact: bool = False) -> list[ElementInfo]:
        """Find text through Win32 EnumChildWindows enumeration (UIA fallback)."""
        query = text.strip()
        lowered_query = query.casefold()
        matches: list[ElementInfo] = []

        def add_match(candidate_hwnd: int) -> None:
            title = Win32API.get_window_text(candidate_hwnd)
            if not title:
                return
            lowered_title = title.casefold()
            is_match = lowered_title == lowered_query if exact else lowered_query in lowered_title
            if not is_match:
                return
            bounds = Win32API.get_window_bounds(candidate_hwnd)
            if bounds is None:
                return
            matches.append(
                ElementInfo(
                    element_id=str(candidate_hwnd),
                    window_id=str(hwnd),
                    text=title,
                    bounds=bounds,
                    class_name=Win32API.get_class_name(candidate_hwnd),
                    control_type="win32-child",
                    source="win32-text",
                    confidence=1.0 if exact else 0.85,
                )
            )

        add_match(hwnd)

        def child_callback(child_hwnd: int, lparam: int) -> bool:
            if not win32gui.IsWindowVisible(child_hwnd):
                return True
            add_match(child_hwnd)
            return True

        win32gui.EnumChildWindows(hwnd, child_callback, 0)
        return matches

    @staticmethod
    def _get_uia_element_id(info: Any) -> str:
        """Generate a unique identifier string from UIA element info."""
        control_id = getattr(info, "control_id", None)
        if control_id is not None:
            return "uia-%s" % control_id
        runtime_id = getattr(info, "runtime_id", None)
        if runtime_id is not None:
            return "uia-%s" % "-".join(str(x) for x in runtime_id)
        return "uia-%s" % id(info)

    @staticmethod
    def find_uia(
        window_id: str,
        text: Optional[str] = None,
        control_type: Optional[str] = None,
        exact: bool = False,
        max_results: int = 20,
    ) -> str:
        """Find controls through the UIA tree.

        At least one of text or control_type filter must be provided.

        Args:
            window_id: Window handle string
            text: Text filter condition (optional)
            control_type: Control type filter condition (optional)
            exact: Whether to match exactly
            max_results: Maximum number of results to return

        Returns:
            Formatted matching result string
        """
        if text is None and control_type is None:
            raise ValueError("find_uia requires at least one filter")
        target_handle = int(window_id)
        desktop = Desktop(backend="uia")
        wrapper = desktop.window(handle=target_handle)
        descendants = [wrapper] + list(wrapper.descendants())

        def normalize(value: Optional[str]) -> str:
            return (value or "").strip()

        def matches_filter(candidate_text: str, query: Optional[str]) -> bool:
            if query is None:
                return True
            normalized_query = normalize(query)
            normalized_text = normalize(candidate_text)
            if exact:
                return normalized_text.casefold() == normalized_query.casefold()
            return normalized_query.casefold() in normalized_text.casefold()

        results: list[ElementInfo] = []
        for candidate in descendants:
            info = candidate.element_info
            candidate_name = normalize(getattr(info, "name", ""))
            candidate_control_type = normalize(getattr(info, "control_type", ""))
            candidate_automation_id = normalize(getattr(info, "automation_id", ""))
            if text is not None and not matches_filter(candidate_name, text):
                continue
            if control_type is not None and not matches_filter(candidate_control_type, control_type):
                continue
            rect = getattr(info, "rectangle", None)
            if rect is None:
                continue
            element_id = FindDriver._get_uia_element_id(info)
            control_id = getattr(info, "control_id", None)
            runtime_id_raw = getattr(info, "runtime_id", None)
            runtime_id = "-".join(str(x) for x in runtime_id_raw) if runtime_id_raw else None
            results.append(
                ElementInfo(
                    element_id=element_id,
                    window_id=window_id,
                    text=candidate_name or candidate_control_type or candidate_automation_id,
                    bounds=Bounds(
                        x=int(rect.left),
                        y=int(rect.top),
                        width=int(rect.right - rect.left),
                        height=int(rect.bottom - rect.top),
                    ),
                    class_name=normalize(getattr(info, "class_name", "")) or None,
                    control_type=candidate_control_type or None,
                    automation_id=candidate_automation_id or None,
                    control_id=control_id,
                    runtime_id=runtime_id,
                    source="uia",
                    confidence=1.0 if exact else 0.95,
                )
            )
            if len(results) >= max_results:
                break
        return "\n".join(ElementFormatter.format_element(r) for r in results)

    @staticmethod
    def find_image(
        window_id: str,
        image_path: str,
        threshold: float = 0.9,
        max_results: int = 5,
    ) -> list[ElementInfo]:
        """Find image template in window using OpenCV template matching.

        Args:
            window_id: Window handle string
            image_path: Template image file path
            threshold: Match confidence threshold (0-1)
            max_results: Maximum number of results to return

        Returns:
            List of matching ElementInfo
        """
        import cv2
        import numpy as np

        hwnd = int(window_id)
        _, _, width, height, data = Win32API.capture_window_bgra(hwnd)
        img_array = np.frombuffer(data, dtype=np.uint8).reshape((height, width, 4))
        img_bgr = img_array[:, :, :3]
        template = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if template is None:
            raise RuntimeError("failed to load template image: %s" % image_path)
        result = cv2.matchTemplate(img_bgr, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)
        template_h, template_w = template.shape[:2]
        raw_matches: list[tuple[int, int, float]] = []
        for pt in zip(*locations[::-1]):
            score = float(result[pt[1], pt[0]])
            raw_matches.append((int(pt[0]), int(pt[1]), score))
        raw_matches.sort(key=lambda m: m[2], reverse=True)

        kept: list[tuple[int, int, float]] = []
        for x, y, score in raw_matches:
            suppressed = False
            for kx, ky, _ in kept:
                overlap_x = max(0, min(x + template_w, kx + template_w) - max(x, kx))
                overlap_y = max(0, min(y + template_h, ky + template_h) - max(y, ky))
                overlap_area = overlap_x * overlap_y
                area = template_w * template_h
                if area > 0 and overlap_area / area > 0.5:
                    suppressed = True
                    break
            if not suppressed:
                kept.append((x, y, score))
            if len(kept) >= max_results:
                break

        matches: list[ElementInfo] = []
        for x, y, score in kept:
            matches.append(
                ElementInfo(
                    element_id=f"image-{x}-{y}",
                    window_id=str(hwnd),
                    text=Path(image_path).name,
                    bounds=Bounds(x=x, y=y, width=template_w, height=template_h),
                    source="image",
                    confidence=score,
                )
            )
        return matches
