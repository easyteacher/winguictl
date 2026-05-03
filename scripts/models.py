#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

"""
Data type definitions.

This module contains data types for window information, element information, and action results.
"""

from dataclasses import asdict, dataclass, field
from typing import Any, Optional


@dataclass
class Bounds:
    """Bounding rectangle."""

    x: int
    y: int
    width: int
    height: int

    @classmethod
    def from_rect(cls, rect) -> "Bounds":
        """Create Bounds from a rect object with left, top, right, bottom attributes."""
        return cls(
            x=int(rect.left),
            y=int(rect.top),
            width=int(rect.right - rect.left),
            height=int(rect.bottom - rect.top),
        )

    def to_dict(self) -> dict[str, int]:
        return {
            "x": int(self.x),
            "y": int(self.y),
            "width": int(self.width),
            "height": int(self.height),
        }


@dataclass
class WindowInfo:
    """Window information."""

    window_id: str
    title: str
    bounds: Bounds
    process_id: Optional[int] = None
    process_name: Optional[str] = None
    is_visible: bool = True
    is_minimized: bool = False
    is_maximized: bool = False
    is_foreground: bool = False
    z_order: int = 0
    parent_hwnd: Optional[int] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "window_id": self.window_id,
            "title": self.title,
            "bounds": self.bounds.to_dict(),
            "process_id": int(self.process_id) if self.process_id is not None else None,
            "process_name": self.process_name,
            "is_visible": self.is_visible,
            "is_minimized": self.is_minimized,
            "is_maximized": self.is_maximized,
            "is_foreground": self.is_foreground,
        }


@dataclass
class ElementInfo:
    """Element information."""

    element_id: str
    window_id: str
    text: str
    bounds: Bounds
    class_name: Optional[str] = None
    control_type: Optional[str] = None
    automation_id: Optional[str] = None
    control_id: Optional[int] = None
    runtime_id: Optional[str] = None
    source: Optional[str] = None
    confidence: Optional[float] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "element_id": self.element_id,
            "window_id": self.window_id,
            "text": self.text,
            "bounds": self.bounds.to_dict(),
            "class_name": self.class_name,
            "control_type": self.control_type,
            "automation_id": self.automation_id,
            "control_id": self.control_id,
            "runtime_id": self.runtime_id,
            "source": self.source,
            "confidence": float(self.confidence) if self.confidence is not None else None,
            "metadata": self.metadata,
        }


@dataclass
class ActionResult:
    """Action result."""

    ok: bool
    code: str
    message: str
    data: dict[str, Any] = field(default_factory=dict)
    timing_ms: Optional[int] = None
    retry_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ElementFormatter:
    """Element formatter."""

    text: str
    rect: Optional[tuple[int, int, int, int]] = None
    control_type: Optional[str] = None
    class_name: Optional[str] = None
    automation_id: Optional[str] = None
    hwnd: Optional[int] = None
    visible: Optional[bool] = None
    enabled: Optional[bool] = None
    confidence: Optional[float] = None
    extra: Optional[dict[str, Any]] = None

    def format(self, indent: int = 0) -> str:
        prefix = "  " * indent
        parts = []

        if self.control_type is not None:
            parts.append(f'control_type="{self.control_type}"')

        if self.class_name is not None:
            parts.append(f'class="{self.class_name}"')

        if self.automation_id is not None:
            parts.append(f'automation_id="{self.automation_id}"')

        if self.hwnd is not None:
            parts.append(f'hwnd="{self.hwnd}"')

        if self.visible is not None:
            parts.append(f"visible={str(self.visible).lower()}")

        if self.enabled is not None:
            parts.append(f"enabled={str(self.enabled).lower()}")

        if self.confidence is not None:
            parts.append(f"confidence={self.confidence:.2f}")

        if self.rect is not None:
            x, y, w, h = self.rect
            parts.append(f"rect=({x},{y} {w}x{h})")

        if self.extra:
            for key, value in self.extra.items():
                if value is not None:
                    parts.append(f'{key}="{value}"')

        details = " ".join(parts)
        return f'{prefix}- "{self.text}" [{details}]'

    @staticmethod
    def format_uia(info: Any, level: int = 0) -> str:
        name = (getattr(info, "name", "") or "").strip()
        if not name:
            name = (getattr(info, "rich_text", "") or "").strip()
        control_type = (getattr(info, "control_type", "") or "").strip() or None
        class_name = (getattr(info, "class_name", "") or "").strip() or None
        automation_id = (getattr(info, "automation_id", "") or "").strip() or None
        control_id = getattr(info, "control_id", None)
        runtime_id = getattr(info, "runtime_id", None)
        rect = getattr(info, "rectangle", None)
        rect_tuple = None
        if rect is not None:
            rect_tuple = (int(rect.left), int(rect.top), int(rect.right - rect.left), int(rect.bottom - rect.top))
        enabled = getattr(info, "enabled", None)

        extra = {}
        if control_id is not None:
            extra["control_id"] = str(control_id)
        if runtime_id is not None:
            extra["runtime_id"] = "-".join(str(x) for x in runtime_id)

        formatter = ElementFormatter(
            text=name,
            rect=rect_tuple,
            control_type=control_type,
            class_name=class_name,
            automation_id=automation_id,
            enabled=enabled,
            extra=extra if extra else None,
        )
        return formatter.format(indent=level)

    @staticmethod
    def format_hwnd(
        hwnd: int,
        text: str,
        class_name: str,
        visible: bool,
        enabled: bool,
        control_id: Optional[int] = None,
        level: int = 0,
        control_type: Optional[str] = None,
    ) -> str:
        extra = {}
        if control_id is not None:
            extra["control_id"] = str(control_id)
        formatter = ElementFormatter(
            text=text,
            hwnd=hwnd,
            class_name=class_name or None,
            visible=visible,
            enabled=enabled,
            control_type=control_type,
            extra=extra if extra else None,
        )
        return formatter.format(indent=level)

    @staticmethod
    def format_ocr(
        text: str,
        left: int,
        top: int,
        width: int,
        height: int,
        confidence: Optional[float] = None,
    ) -> str:
        formatter = ElementFormatter(
            text=text,
            rect=(left, top, width, height),
            confidence=confidence,
        )
        return formatter.format()

    @staticmethod
    def format_element(element_info: "ElementInfo", indent: int = 0) -> str:
        rect_tuple = None
        if element_info.bounds:
            rect_tuple = (
                int(element_info.bounds.x),
                int(element_info.bounds.y),
                int(element_info.bounds.width),
                int(element_info.bounds.height),
            )

        extra = {}
        if element_info.control_id is not None:
            extra["control_id"] = str(element_info.control_id)
        if element_info.runtime_id is not None:
            extra["runtime_id"] = element_info.runtime_id

        formatter = ElementFormatter(
            text=element_info.text,
            rect=rect_tuple,
            control_type=element_info.control_type,
            class_name=element_info.class_name,
            automation_id=element_info.automation_id,
            confidence=element_info.confidence,
            extra=extra if extra else None,
        )
        return formatter.format(indent=indent)
