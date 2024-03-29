import ipyvuetify as v
from sepal_ui.scripts import utils as su

from component import parameter as cp
from component.message import cm

from .gwb_tile import GwbTile


class MspaTile(GwbTile):
    def __init__(self, model):

        # create the widgets
        connectivity = v.Select(
            label=cm.acc.connectivity,
            items=cp.connectivity,
            v_model=cp.connectivity[0]["value"],
        )
        edge_width = v.Slider(
            label=cm.mspa.edge_width, min=1, max=100, v_model=1, thumb_label=True
        )
        transition = v.Switch(
            label=cm.mspa.transition, false_value=0, true_value=1, v_model=1
        )
        int_ext = v.Switch(
            label=cm.mspa.int_ext, false_value=0, true_value=1, v_model=1
        )
        disk = v.Switch(label=cm.mspa.disk, false_value=0, true_value=1, v_model=0)
        stats = v.Switch(label=cm.mspa.stats, false_value=0, true_value=1, v_model=0)

        # bind to the io
        (
            model.bind(connectivity, "connectivity")
            .bind(edge_width, "edge_width")
            .bind(transition, "transition")
            .bind(int_ext, "int_ext")
            .bind(disk, "disk")
            .bind(stats, "statistics")
        )

        super().__init__(
            model=model,
            inputs=[connectivity, edge_width, transition, int_ext, disk, stats],
        )

    @su.loading_button()
    def _on_click(self, widget, event, data):

        # check inputs
        if not all(
            [
                self.alert.check_input(self.model.connectivity, cm.acc.no_connex),
                self.alert.check_input(self.model.edge_width, cm.mspa.no_edge_width),
                self.alert.check_input(self.model.bin_map, cm.bin.no_bin),
            ]
        ):
            return

        super()._on_click(widget, event, data)

        return
