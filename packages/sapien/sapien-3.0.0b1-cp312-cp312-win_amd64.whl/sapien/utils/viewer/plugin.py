from __future__ import annotations
from sapien import Scene

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import viewer


def copy_to_clipboard(content):
    try:
        import pyperclip

        pyperclip.copy(content)
    except ModuleNotFoundError:
        print(
            "copy to clipboard is only available when pyperclip is installed with [pip install pyperclip]"
        )


class Plugin:
    def init(self, v: viewer.Viewer):
        self.viewer = v

    def notify_scene_change(self):
        pass

    def notify_selected_entity_change(self):
        pass

    def notify_window_focus_change(self, focused):
        pass

    def get_ui_windows(self):
        return []

    def before_render(self):
        pass

    def after_render(self):
        pass

    def close(self):
        pass

    def clear_scene(self):
        pass
