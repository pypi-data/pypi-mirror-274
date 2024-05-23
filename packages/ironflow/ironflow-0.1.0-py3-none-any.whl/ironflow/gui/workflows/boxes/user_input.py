# coding: utf-8
# Copyright (c) Max-Planck-Institut für Eisenforschung GmbH - Computational Materials Design (CM) Department
# Distributed under the terms of "New BSD License", see the LICENSE file.
"""
For getting non-flow feedback from the user, e.g. filenames and confirmations.
"""

from __future__ import annotations

from typing import Any, Optional

import ipywidgets as widgets

from ironflow.gui.draws_widgets import DrawsWidgets


class UserInput(DrawsWidgets):
    main_widget_class = widgets.HBox

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_field = widgets.Text(value="INIT VALUE", description="DESCRIPTION")
        self.decision_info = widgets.Label(value="INIT VALUE")
        button_layout = widgets.Layout(width="50px")
        self.ok_button = widgets.Button(
            tooltip="Confirm", icon="check", layout=button_layout
        )
        self._last_ok_callback = None
        self.cancel_button = widgets.Button(
            tooltip="Cancel", icon="ban", layout=button_layout
        )
        # Todo: Use xmark once this is available
        self.cancel_button.on_click(self._click_clear)

    def clear(self):
        self._clear_callback()
        self.widget.children = []
        super().clear()

    @property
    def text(self):
        return self.input_field.value

    def wrap_callback(self, callback: callable) -> callable:
        def wrapped_callback(change: dict) -> None:
            callback(change)
            self.clear()

        return wrapped_callback

    def _clear_callback(self):
        if self._last_ok_callback is not None:
            self.input_field.on_submit(self._last_ok_callback, remove=True)
            self.ok_button.on_click(self._last_ok_callback, remove=True)

    def _set_callback(self, callback: callable):
        wrapped_callback = self.wrap_callback(callback)
        self.input_field.on_submit(wrapped_callback)
        # ^ Ignore the deprecation warning, 'observe' doesn't function the way we actually want
        # https://github.com/jupyter-widgets/ipywidgets/issues/2446
        self.ok_button.on_click(wrapped_callback)
        self._last_ok_callback = wrapped_callback

    def _open(
        self,
        widget: widgets.Widget,
        callback: callable,
        ok_tooltip: str,
        cancel_tooltip: str,
    ):
        self.widget.children = [widget, self.ok_button, self.cancel_button]
        self.ok_button.tooltip = ok_tooltip
        self.cancel_button.tooltip = cancel_tooltip
        self._set_callback(callback)

    def open_text(
        self,
        description: str,
        callback: callable,
        initial_value: Any,
        description_tooltip: Optional[str] = None,
        ok_tooltip: str = "Confirm",
        cancel_tooltip: str = "Cancel",
    ):
        self.input_field.description = description
        description_tooltip = (
            description_tooltip if description_tooltip is not None else description
        )
        self.input_field.description_tooltip = description_tooltip
        self.input_field.value = initial_value
        self._open(self.input_field, callback, ok_tooltip, cancel_tooltip)

    def open_bool(
        self,
        description: str,
        callback: callable,
        ok_tooltip: str = "Confirm",
        cancel_tooltip: str = "Cancel",
    ):
        self.decision_info.value = description
        self._open(self.decision_info, callback, ok_tooltip, cancel_tooltip)

    def _click_clear(self, change: None):
        self.clear()
