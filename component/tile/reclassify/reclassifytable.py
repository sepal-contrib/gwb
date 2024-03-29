from functools import partial

import ipyvuetify as v
import sepal_ui.sepalwidgets as sw
from traitlets import Dict


class ReclassifyTable(v.SimpleTable, sw.SepalWidget):

    matrix = Dict({}).tag(sync=True)

    def __init__(self, *args, **kwargs):
        """Widget to reclassify raster/feature_class into local classes."""
        self.dense = True

        # Create table
        super().__init__(*args, **kwargs)

    def _get_matrix(self, code_fields, classes_file=""):
        """Init table reading local classes file and code/categories fields.

        Args:
            code_fields (list) : List of codes/categories of raster/feature collection
            classes_file (str) : Classes file containing code/category and description
        """
        self.matrix = {}

        # Set empty items if there is not a file selected
        self.items = []

        if classes_file:
            self.items = self.read_classes_from_file(classes_file)

        headers = ["From: user code", "To: Custom Code"]

        # Instantiate an empty dictionary with code as
        # keys and empty values
        for code in code_fields:
            self.matrix[code] = ""

        header = [
            v.Html(
                tag="tr", children=([v.Html(tag="th", children=[h]) for h in headers])
            )
        ]

        rows = [
            v.Html(
                tag="tr",
                children=[
                    v.Html(tag="td", children=[str(code)]),
                    self.get_classes(code),
                ],
            )
            for code in code_fields
        ]

        self.children = [v.Html(tag="tbody", children=header + rows)]

    def read_classes_from_file(self, class_file):
        """Read classes from .csv file.

        Args:
            class_file (str): classes .csv file containing lines of (code_class, description)
        """
        items = []
        with open(class_file) as f:
            for cl in f.readlines():
                # c:code, d:description
                item = [
                    {"value": c, "text": f"{c}: " + d.replace("\n", "")}
                    for c, d in [cl.split(",")]
                ]
                items += item

        return items

    def store(self, code, change):
        """Store user row code and new select value (file class)."""
        self.matrix[code] = change["new"]

    def get_classes(self, code):
        """Get class selector on the fly and store code to matrix.

        Args:
            code (str) : id to link local (raster, fc) with new classes (from file)
        """
        select = v.Combobox(
            _metadata={"name": code},
            items=self.items,
            v_model=None,
            dense=True,
            hide_details=True,
        )

        select.observe(partial(self.store, code), "v_model")

        return select
