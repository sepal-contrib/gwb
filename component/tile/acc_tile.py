import json

import ipyvuetify as v
from sepal_ui.scripts import utils as su

from component import parameter as cp
from component import widget as cw
from component.message import cm

from .gwb_tile import GwbTile


class AccTile(GwbTile):
    def __init__(self, model):

        # create the widgets
        connectivity = v.Select(
            label=cm.acc.connectivity,
            items=cp.connectivity,
            v_model=cp.connectivity[0]["value"],
        )
        res = v.TextField(
            label=cm.acc.res, type="number", v_model=None, hint=cm.acc.res_hint
        )
        thresholds = cw.Thresholds(label=cm.acc.thresholds)
        options = v.Select(
            label=cm.acc.options,
            items=cp.acc_options,
            v_model=cp.acc_options[0]["value"],
        )
        big_3_pink = v.Switch(label=cm.acc.big3pink, v_model=True)

        # bind to the
        (
            model.bind(connectivity, "connectivity")
            .bind(res, "res")
            .bind(thresholds.save, "thresholds")
            .bind(options, "options")
            .bind(big_3_pink, "big_3_pink")
        )

        # extra js behaviour
        res.on_event("focusout", self._on_focus_out)

        super().__init__(
            model=model, inputs=[connectivity, res, thresholds, options, big_3_pink]
        )

    @su.loading_button()
    def _on_click(self, widget, event, data):

        # check inputs
        if not all(
            [
                self.alert.check_input(self.model.connectivity, cm.acc.no_connex),
                self.alert.check_input(self.model.res, cm.acc.no_res),
                self.alert.check_input(
                    json.loads(self.model.thresholds), cm.acc.no_thres
                ),
                self.alert.check_input(self.model.options, cm.acc.no_options),
                self.alert.check_input(self.model.bin_map, cm.bin.no_bin),
            ]
        ):
            return

        super()._on_click(widget, event, data)

        return

    def _on_focus_out(self, widget, event, data):

        # clear error
        widget.error_messages = None

        # get out if v_model is none
        if not widget.v_model:
            return self

        valid = True
        try:

            value = int(widget.v_model)

            if value < 0:
                valid = False

        except ValueError:
            valid = False

        if not valid:
            widget.v_model = None
            widget.error_messages = [cm.acc.res_hint]

        return self
