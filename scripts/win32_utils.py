#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

"""Win32 API low-level utility module.

Wraps Win32 API calls for window screenshots, mouse clicks,
dragging, text input, key sending and other low-level operations.
Prefers pywin32 (win32gui/win32api/win32ui) wrapped APIs,
falling back to ctypes only for interfaces not wrapped by pywin32
(e.g. PrintWindow). All methods are static.
"""

import ctypes
import time
import zlib
from pathlib import Path
from typing import Optional, Tuple

import win32api
import win32con
import win32gui
import win32ui

from constants import VK_CODE_MAP
from models import Bounds

PW_RENDERFULLCONTENT = 0x00000002


class Win32API:

    @staticmethod
    def get_window_text(hwnd: int) -> str:
        """Get window title text."""
        return win32gui.GetWindowText(hwnd)

    @staticmethod
    def get_class_name(hwnd: int) -> str:
        """Get window class name."""
        return win32gui.GetClassName(hwnd)

    @staticmethod
    def get_window_bounds(hwnd: int) -> Optional[Bounds]:
        """Get window screen coordinates and dimensions."""
        try:
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        except Exception:
            return None
        return Bounds(
            x=int(left),
            y=int(top),
            width=int(right - left),
            height=int(bottom - top),
        )

    @staticmethod
    def get_window_state(hwnd: int) -> Tuple[bool, bool]:
        """Get window minimized/maximized state.

        Returns:
            (is_minimized, is_maximized) tuple
        """
        is_minimized = bool(win32gui.IsIconic(hwnd))
        placement = win32gui.GetWindowPlacement(hwnd)
        show_cmd = placement[1]
        is_maximized = show_cmd == win32con.SW_MAXIMIZE
        return is_minimized, is_maximized

    @staticmethod
    def capture_window_bgra(window_id) -> Tuple[int, int, int, int, bytearray]:
        """Capture window screenshot, returning BGRA pixel data.

        Uses win32gui/win32ui to obtain the window DC and create a bitmap.
        Prefers PrintWindow API (supports background window capture),
        falling back to BitBlt if PrintWindow fails.

        Returns:
            (x, y, width, height, bgra_data) tuple
        """
        hwnd = int(window_id)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        x, y = int(left), int(top)
        width, height = int(right - left), int(bottom - top)
        if width <= 0 or height <= 0:
            raise RuntimeError("invalid window size: %sx%s" % (width, height))

        hdc_window = win32gui.GetWindowDC(hwnd)
        dc = win32ui.CreateDCFromHandle(hdc_window)
        memdc = dc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(dc, width, height)
        memdc.SelectObject(bmp)

        result = ctypes.windll.user32.PrintWindow(hwnd, memdc.GetSafeHdc(), PW_RENDERFULLCONTENT)
        if not result:
            memdc.BitBlt((0, 0), (width, height), dc, (0, 0), win32con.SRCCOPY)

        bits = bmp.GetBitmapBits(True)
        data = bytearray(bits)

        win32gui.DeleteObject(bmp.GetHandle())
        memdc.DeleteDC()
        dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hdc_window)
        return x, y, width, height, data

    @staticmethod
    def write_png(output: Path, width: int, height: int, bgra_data: bytearray) -> None:
        """Write BGRA pixel data to a PNG file (pure Python, no third-party libs)."""
        import struct

        def crc32(data: bytes) -> int:
            return zlib.crc32(data) & 0xFFFFFFFF

        def chunk(chunk_type: bytes, data: bytes) -> bytes:
            chunk_data = chunk_type + data
            return struct.pack(">I", len(data)) + chunk_data + struct.pack(">I", crc32(chunk_data))

        raw = bytearray()
        row_size = width * 4
        for y in range(height):
            raw.append(0)
            raw.extend(bgra_data[y * row_size : (y + 1) * row_size])
        compressed = zlib.compress(bytes(raw))
        ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
        signature = b"\x89PNG\r\n\x1a\n"
        ihdr = chunk(b"IHDR", ihdr_data)
        idat = chunk(b"IDAT", compressed)
        iend = chunk(b"IEND", b"")
        output.write_bytes(signature + ihdr + idat + iend)

    @staticmethod
    def write_bmp(output: Path, width: int, height: int, bgra_data: bytearray) -> None:
        """Write BGRA pixel data to a BMP file."""
        import struct

        row_size = (width * 4 + 3) & ~3
        image_size = row_size * height
        header_size = 54
        file_size = header_size + image_size
        bmp_data = bytearray(file_size)
        struct.pack_into("<2sIHHI", bmp_data, 0, b"BM", file_size, 0, 0, header_size)
        struct.pack_into("<IiiHHIIiiII", bmp_data, 14, 40, width, height, 1, 32, 0, image_size, 0, 0, 0, 0)
        for y in range(height):
            src_offset = y * width * 4
            dst_offset = header_size + (height - 1 - y) * row_size
            bmp_data[dst_offset : dst_offset + width * 4] = bgra_data[src_offset : src_offset + width * 4]
        output.write_bytes(bytes(bmp_data))

    @staticmethod
    def send_click(x: int, y: int) -> None:
        """Perform a left mouse button click at the specified screen coordinates."""
        win32api.SetCursorPos((x, y))
        time.sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    @staticmethod
    def send_drag(x1: int, y1: int, x2: int, y2: int, duration_ms: int = 500) -> None:
        """Drag from (x1,y1) to (x2,y2), moving smoothly over the specified duration."""
        steps = max(1, duration_ms // 16)
        win32api.SetCursorPos((x1, y1))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.05)
        for i in range(1, steps + 1):
            t = i / steps
            cx = int(x1 + (x2 - x1) * t)
            cy = int(y1 + (y2 - y1) * t)
            win32api.SetCursorPos((cx, cy))
            time.sleep(duration_ms / 1000 / steps)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    @staticmethod
    def send_type_text(text: str) -> None:
        """Type text character by character using Unicode keyboard events."""
        for ch in text:
            code_point = ord(ch)
            win32api.keybd_event(0, code_point, win32con.KEYEVENTF_UNICODE, 0)
            win32api.keybd_event(0, code_point, win32con.KEYEVENTF_UNICODE | win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def send_press_key(key: str) -> None:
        """Press and release a single virtual key. See VK_CODE_MAP for key names."""
        virtual_key = VK_CODE_MAP.get(key.lower())
        if virtual_key is None:
            raise ValueError("unsupported key: %s" % key)
        win32api.keybd_event(virtual_key, 0, 0, 0)
        time.sleep(0.05)
        win32api.keybd_event(virtual_key, 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def send_hotkey(keys: list[str]) -> None:
        """Press a key chord. Presses all keys in order, then releases in order."""
        virtual_keys = []
        for key in keys:
            vk = VK_CODE_MAP.get(key.lower())
            if vk is None:
                raise ValueError("unsupported key: %s" % key)
            virtual_keys.append(vk)
        for vk in virtual_keys:
            win32api.keybd_event(vk, 0, 0, 0)
            time.sleep(0.05)
        for vk in virtual_keys:
            win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.05)

    @staticmethod
    def set_focus(hwnd: int) -> None:
        """Bring the specified window to the foreground and set focus."""
        win32gui.SetForegroundWindow(hwnd)
        win32gui.SetFocus(hwnd)
