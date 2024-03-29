import ipyvuetify as v
from sepal_ui import sepalwidgets as sw

from component import model as models
from component import tile
from component.message import cm
from component.widget.licence_dialog import LicenceDialog

tiles = {
    "acc": {"title": "Accounting of image objects and areas", "desc": "some desc"},
    "dist": {"title": "Euclidean Distance", "desc": "some desc"},
    "frag": {"title": "Fragmentation", "desc": "some desc"},
    "lm": {"title": "Landscape Mosaic", "desc": "some desc"},
    "mspa": {"title": "Morphological Spatial Pattern Analysis", "desc": "some desc"},
    "parc": {"title": "Parcellation", "desc": "some desc"},
    "rss": {"title": "Restoration Status Summary", "desc": "some desc"},
    "spa": {"title": "Simplified Pattern Analysis", "desc": "some desc"},
    "fad": {"title": "Forest Area Density", "desc": "some desc"},
    "p223": {
        "title": "Density (P2), Contagion (P22) or or FG-Adjacency (P23)",
        "desc": "some desc",
    },
}


# Create a landing tile, with a title, a description and one different
# Card for each of all the available tiles.


class ProcessDialog(v.Dialog):
    built_tiles = {}

    def __init__(self, *args, **kwargs):
        self.v_model = False
        super().__init__(max_width="950px", min_width="950px")

        self.title = v.CardTitle()
        self.btn_close = sw.Btn("Close", class_="mr-2")
        self.card_content = v.CardText(children=[])

        self.children = [
            v.Card(
                children=[
                    self.title,
                    self.card_content,
                ],
            ),
        ]

    def load_element(self, tile_id):
        """Load the element in the dialog."""
        if tile_id in self.built_tiles:
            self.card_content.children = self.built_tiles[tile_id]
            return

        # This is ugly but I need something quick and I don't have time to think about it

        if tile_id == "acc":
            model = models.AccModel()
            title = sw.Tile(
                model.tile_id, cm.acc.title, [sw.Markdown(cm.acc.description)]
            )
            convert = tile.ConvertByte(model, 4)
            process = tile.AccTile(model)

        elif tile_id == "dist":
            model = models.DistModel()
            title = sw.Tile(
                model.tile_id, cm.dist.title, [sw.Markdown(cm.dist.description)]
            )
            convert = tile.ConvertByte(model, 2)
            process = tile.DistTile(model)

        elif tile_id == "fad":
            process = tile.FadTile()
            self.built_tiles[tile_id] = [process]
            self.card_content.children = [process]
            return

        elif tile_id == "frag":
            model = models.FragModel()
            title = sw.Tile(
                model.tile_id, cm.frag.title, [sw.Markdown(cm.frag.description)]
            )
            convert = tile.ConvertByte(model, 4)
            process = tile.FragTile(model)

        elif tile_id == "lm":
            model = models.LmModel()
            title = sw.Tile(
                model.tile_id, cm.lm.title, [sw.Markdown(cm.lm.description)]
            )
            convert = tile.ConvertByte(model, 3)
            process = tile.LmTile(model)

        elif tile_id == "mspa":
            model = models.MspaModel()
            title = sw.Tile(
                model.tile_id, cm.mspa.title, [sw.Markdown(cm.mspa.description)]
            )
            convert = tile.ConvertByte(model, 2)
            process = tile.MspaTile(model)

        elif tile_id == "p223":
            process = tile.P223Tile()
            self.built_tiles[tile_id] = [process]
            self.card_content.children = [process]
            return

        elif tile_id == "parc":
            model = models.ParcModel()
            title = sw.Tile(
                model.tile_id, cm.parc.title, [sw.Markdown(cm.parc.description)]
            )
            convert = tile.ConvertByte(model, 0)
            process = tile.ParcTile(model)

        elif tile_id == "rss":
            model = models.RssModel()
            title = sw.Tile(
                model.tile_id, cm.rss.title, [sw.Markdown(cm.rss.description)]
            )
            convert = tile.ConvertByte(model, 2)
            process = tile.RssTile(model)

        elif tile_id == "spa":
            model = models.SpaModel()
            title = sw.Tile(
                model.tile_id, cm.spa.title, [sw.Markdown(cm.spa.description)]
            )
            convert = tile.ConvertByte(model, 2)
            process = tile.SpaTile(model)

        else:
            raise ValueError(f"Tile {tile_id} not found")

        self.built_tiles[tile_id] = [title, convert, process]

        self.card_content.children = [
            title,
            convert,
            process,
        ]

    def open_dialog(self, *_, tile_id: str):
        """Open dialog."""
        self.load_element(tile_id)
        self.v_model = True

    def close_dialog(self, *_):
        """Close dialog."""
        self.v_model = False


class LandingTile(sw.Tile):
    def __init__(self, **kwargs):
        super().__init__(
            "landing_tile",
            "Run Process",
        )
        self.class_ = "pa-4"
        self.cols = 12
        self.wrap = True

        # create the description

        def get_description(tile_id):
            """Get the description of the tile."""
            # if the description is larger than 100 characters, only show the first 100
            # and add a ... at the end
            if len(getattr(cm, tile_id).description) > 250:
                return sw.Markdown(getattr(cm, tile_id).description[:250] + "...")

        # Create the cards one for each tile
        cards = [
            v.Card(
                outlined=True,
                class_="ma-5",
                attributes={"id": tile_id},
                min_width="30px",
                min_height="200px",
                children=[
                    v.CardTitle(children=[v.Html(tag="h4", children=[vals["title"]])]),
                    v.CardText(
                        # cnter content
                        class_="text-center",
                        children=[v.Icon(children=["mdi-cogs"], size="80")],
                    ),
                    v.CardText(children=[get_description(tile_id)]),
                ],
            )
            for tile_id, vals in tiles.items()
        ]

        # Create events for each card
        for card in cards:
            card.on_event("click", self.open_dialog)

        self.process_dialog = ProcessDialog()
        license_dialog = LicenceDialog()

        self.children = [
            v.Flex(xs12=True, sm6=True, md3=True, children=[card]) for card in cards
        ] + [self.process_dialog, license_dialog]

    def open_dialog(self, widget, event, data):
        """Open the dialog for the selected tile."""
        widget.loading = True
        self.process_dialog.open_dialog(tile_id=widget.attributes["id"])
        widget.loading = False
