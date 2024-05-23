# coding: utf-8
# Copyright (c) Max-Planck-Institut für Eisenforschung GmbH - Computational Materials Design (CM) Department
# Distributed under the terms of "New BSD License", see the LICENSE file.
"""
Canvas representations of the nodes.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import numpy as np
from ipycanvas import hold_canvas

from ironflow.gui.workflows.canvas_widgets.base import CanvasWidget
from ironflow.gui.workflows.canvas_widgets.buttons import (
    RepresentButtonWidget,
    ExpandButtonWidget,
    CollapseButtonWidget,
    ExecButtonWidget,
)
from ironflow.gui.workflows.canvas_widgets.layouts import (
    NodeLayout,
    DataPortLayout,
    ExecPortLayout,
    ButtonLayout,
)
from ironflow.gui.workflows.canvas_widgets.ports import PortWidget

if TYPE_CHECKING:
    from ironflow.gui.workflows.canvas_widgets.flow import FlowCanvas
    from ironflow.gui.workflows.canvas_widgets.base import Number
    from ironflow.model.port import NodeInputBP, NodeOutputBP
    from ironflow.model.node import Node


class NodeWidget(CanvasWidget):
    """
    The main ipycanvas representation of a node. Has graphical elements for IO ports. Collapsable to save space.

    Also has a `SHOW` button that sends a representation over to the `ironflow.GUI.node_presenter` window.
    Presentation gets locked until the button is pressed again, the node is deleted, or another node gets presented.
    While presented, representation updates automatically on changes to input.
    """

    def __init__(
        self,
        x: Number,
        y: Number,
        parent: FlowCanvas | CanvasWidget,
        layout: NodeLayout,
        node: Node,
        selected: bool = False,
        title: Optional[str] = None,
        port_radius: Number = 10,
    ):
        super().__init__(
            x=x,
            y=y,
            parent=parent,
            layout=layout,
            selected=selected,
            title=title if title is not None else node.title,
        )

        self.node = node
        self.inputs = node.inputs
        self.outputs = node.outputs

        # Register callback to change color on updates
        self.node.widget = self
        self._updating = False
        self.node.before_update.connect(self._draw_before_updating)
        self.node.after_update.connect(self._draw_after_updating)

        self.port_radius = port_radius
        self.port_layouts = {"data": DataPortLayout(), "exec": ExecPortLayout()}

        n_ports_max = (
            max(len(self.node.inputs), len(self.node.outputs)) + 1
        )  # Includes the expand/collapse button
        exec_port_i = np.where([p.type_ == "exec" for p in self.node.inputs])[0]
        n_ports_min = exec_port_i[-1] + 1 if len(exec_port_i) > 0 else 1
        subwidget_size_and_buffer = 1.33 * 2 * self.port_radius
        self._title_box_height = self.layout.title_box_height
        self._max_body_height = subwidget_size_and_buffer * n_ports_max
        self._min_body_height = subwidget_size_and_buffer * n_ports_min
        self._expanded_height = self._title_box_height + self._max_body_height
        self._collapsed_height = self._title_box_height + self._min_body_height
        self._height = self._expanded_height

        y_step = self._max_body_height / n_ports_max
        self._subwidget_y_locs = (
            np.arange(n_ports_max) + 0.5
        ) * y_step + self._title_box_height

        self.add_inputs()
        self.add_outputs()
        self.expand_button = ExpandButtonWidget(
            x=0.5 * self.width - self.port_radius,
            y=self._subwidget_y_locs[0] - self.port_radius,
            parent=self,
            layout=ButtonLayout(),
            pressed=True,
            visible=False,
            size=2 * self.port_radius,
        )
        self.add_widget(self.expand_button)
        self.collapse_button = CollapseButtonWidget(
            x=0.5 * self.width - self.port_radius,
            y=self._subwidget_y_locs[-1] - self.port_radius,
            parent=self,
            layout=ButtonLayout(),
            pressed=False,
            visible=True,
            size=2 * self.port_radius,
        )
        self.add_widget(self.collapse_button)

        button_layout = ButtonLayout()
        button_edge_offset = 5
        self.represent_button = RepresentButtonWidget(
            x=self.width - button_layout.width - button_edge_offset,
            y=button_edge_offset,
            parent=self,
            layout=button_layout,
        )
        self.add_widget(self.represent_button)

    def on_click(
        self, last_selected_object: Optional[CanvasWidget]
    ) -> NodeWidget | None:
        if last_selected_object == self:
            return self
        else:
            if last_selected_object is not None:
                last_selected_object.deselect()
            self.select()
            try:
                self.screen.open_node_control(self.node)
                return self
            except Exception as e:
                self.screen.print(
                    f"Failed to handle selection of {self} with exception {e}"
                )
                self.screen.close_node_control()
                self.deselect()
                return None

    def on_double_click(self) -> None:
        self.delete()
        return None

    @staticmethod
    def _draw_before_updating(node: Node, inp: int) -> None:
        node.widget._updating = True
        with hold_canvas(node.widget.canvas):
            node.widget.draw()

    @staticmethod
    def _draw_after_updating(node: Node, inp: int) -> None:
        node.widget._updating = False
        with hold_canvas(node.widget.canvas):
            node.widget.draw()

    @property
    def color(self) -> str:
        if self._updating:
            return self.layout.updating_color
        elif self.selected:
            return self.layout.selected_color
        else:
            return self.layout.background_color

    def draw_title(self) -> None:
        self.canvas.fill_style = self.node.color
        self.canvas.fill_rect(self.x, self.y, self.width, self._title_box_height)
        self.canvas.font = self.layout.font_string
        self.canvas.fill_style = self.layout.font_color
        x = self.x + (self.width * 0.04)
        y = self.y + self._title_box_height - 8
        self.canvas.fill_text(self.title[: self.layout.max_title_chars], x, y)

    def _add_ports(
        self,
        radius: Number,
        inputs: Optional[list[NodeInputBP]] = None,
        outputs: Optional[list[NodeOutputBP]] = None,
        border: Number = 1.4,
    ) -> None:
        if inputs is not None:
            x = radius * border
            data = inputs
            title_alignment = "start"
        elif outputs is not None:
            x = self.width - radius * border
            data = outputs
            title_alignment = "end"
        else:
            return

        n_ports = len(data)
        for i_port in range(n_ports):
            port = data[i_port]
            data_or_exec = port.type_
            self.add_widget(
                PortWidget(
                    x=x,
                    y=self._subwidget_y_locs[i_port],
                    parent=self,
                    layout=self.port_layouts[data_or_exec],
                    port=port,
                    hidden_x=x,
                    hidden_y=self._subwidget_y_locs[0],
                    radius=radius,
                    title_alignment=title_alignment,
                )
            )
            if data_or_exec == "exec" and inputs is not None:
                button_layout = ButtonLayout()
                self.add_widget(
                    ExecButtonWidget(
                        x=x + radius,
                        y=self._subwidget_y_locs[i_port] - 0.5 * button_layout.height,
                        parent=self,
                        layout=button_layout,
                        port=port,
                    )
                )

    def add_inputs(self) -> None:
        self._add_ports(radius=self.port_radius, inputs=self.inputs)

    def add_outputs(self) -> None:
        self._add_ports(radius=self.port_radius, outputs=self.outputs)

    def delete(self) -> None:
        self.screen.ensure_node_not_presented(self)
        self.screen.ensure_node_not_controlled(self.node)
        for c in self.flow.connections[
            ::-1
        ]:  # Reverse to make sure we traverse whole thing even if we delete
            # Todo: Can we be more efficient than looping over all nodes?
            if (c.inp.node == self.node) or (c.out.node == self.node):
                self.flow.remove_connection(c)
        self.flow.remove_node(self.node)
        self.parent.objects_to_draw.remove(self)

    def deselect(self) -> None:
        super().deselect()
        self.screen.ensure_node_not_controlled(self.node)

    @property
    def port_widgets(self) -> list[PortWidget]:
        return [o for o in self.objects_to_draw if isinstance(o, PortWidget)]

    def expand_io(self):
        self._height = self._expanded_height
        for o in self.port_widgets:
            o.show()
        self.collapse_button.unpress()

    def collapse_io(self):
        self._height = self._collapsed_height
        for o in self.port_widgets:
            o.hide()
        self.expand_button.unpress()


class ButtonNodeWidget(NodeWidget):
    def __init__(
        self,
        x: Number,
        y: Number,
        parent: FlowCanvas | CanvasWidget,
        layout: NodeLayout,
        node: Node,
        selected: bool = False,
        title: Optional[str] = None,
        port_radius: Number = 10,
    ):
        super().__init__(
            x=x,
            y=y,
            parent=parent,
            layout=layout,
            node=node,
            selected=selected,
            title=title,
            port_radius=port_radius,
        )

        button_layout = ButtonLayout()
        self.exec_button = ExecButtonWidget(
            x=0.8 * (self.width - button_layout.width),
            y=self._subwidget_y_locs[0] - 0.5 * button_layout.height,
            parent=self,
            layout=button_layout,
            port=self.node.outputs[0],
        )
        self.add_widget(self.exec_button)
