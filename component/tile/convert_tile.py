from sepal_ui import sepalwidgets as sw
import ipyvuetify as v
import rasterio as rio

from component.message import cm
from component import scripts as cs

class FourBytes(sw.Tile):
    
    def __init__(self, io):
        
        # gather the io 
        self.io = io
        
        # create the widgets
        self.file = sw.FileInput(['.tif', '.tiff'])
        self.background = v.Select(label = 'background', items = None, v_model = None, chips = True, multiple = True)
        self.foreground = v.Select(label = 'foreground', items = None, v_model = None, chips = True, multiple = True)
        self.spe_background_1 = v.Select(label = 'spetial background 1', items = None, v_model = None, chips = True, multiple = True)
        self.spe_background_2 = v.Select(label = 'spetial background 2', items = None, v_model = None, chips = True, multiple = True)
        
        requirements = sw.Markdown(cm.requirement._4)

        # bind it to the io
        self.output = sw.Alert() \
            .bind(self.file, self.io, 'file') \
            .bind(self.background, self.io, 'background') \
            .bind(self.foreground, self.io, 'foreground') \
            .bind(self.spe_background_1, self.io, 'spe_background_1') \
            .bind(self.spe_background_2, self.io, 'spe_background_2')
        
        # create the btn 
        btn = sw.Btn("Convert the imag classes")
        
        super().__init__(
            self.io.tile_id,
            "Select map classes",
            inputs = [
                requirements,
                self.file,
                self.background,
                self.foreground,
                self.spe_background_1, 
                self.spe_background_2, 
            ],
            output = self.output,
            btn = btn
        
        )
        
        # bind js event
        btn.on_event('click', self._on_click)
        self.file.observe(self._on_change, 'v_model')
        
    def _on_click(self, widget, event, data):
            
        # silence the btn 
        widget.toggle_loading()
            
        # check variables
        if not self.output.check_input(self.io.file, cm.bin.no_file): return widget.toggle_loading()
        if not self.output.check_input(len(self.io.foreground), cm.bin.no_classes): return widget.toggle_loading()
            
        # compute the bin map
        try:
        
            # update byte list 
            self.io.update_byte_list()
        
            # create a bin map 
            bin_map = cs.set_byte_map(
                self.io.byte_list, 
                self.io.file, 
                self.io.process, 
                self.output
            )
            
            self.io.set_bin_map(bin_map)
            
            # add the bin map to the download btn
            
        except Exception as e:
            self.output.add_live_msg(str(e), 'error')
                
            
        # release the btn 
        widget.toggle_loading()
            
        return 
    
    def _on_change(self, change):
        """update the list according to the file selection"""
        
        # empty all select
        self.background.v_model = None
        self.foreground.model = None
        self.spe_background_1.model = None 
        self.spe_background_2.model = None 
                
        # get all unique values from the image
        features = cs.unique(change['new'])
        
        # add the new list as items 
        self.background.items = features
        self.foreground.items = features
        self.spe_background_1.items = features 
        self.spe_background_2.items = features
        
        return
    
class TwoBytes(sw.Tile):
    
    def __init__(self, io):
        
        # gather the io 
        self.io = io
        
        # create the widgets
        self.file = sw.FileInput(['.tif', '.tiff'])
        self.background = v.Select(label = 'background', items = None, v_model = None, chips = True, multiple = True)
        self.foreground = v.Select(label = 'foreground', items = None, v_model = None, chips = True, multiple = True)
        
        requirements = sw.Markdown(cm.requirement._2)

        # bind it to the io
        self.output = sw.Alert() \
            .bind(self.file, self.io, 'file') \
            .bind(self.background, self.io, 'background') \
            .bind(self.foreground, self.io, 'foreground')
        
        # create the btn 
        btn = sw.Btn("Convert the imag classes")
        
        super().__init__(
            self.io.tile_id,
            "Select map classes",
            inputs = [
                requirements,
                self.file,
                self.background,
                self.foreground
            ],
            output = self.output,
            btn = btn
        
        )
        
        # bind js event
        btn.on_event('click', self._on_click)
        self.file.observe(self._on_change, 'v_model')
        
    def _on_click(self, widget, event, data):
            
        # silence the btn 
        widget.toggle_loading()
            
        # check variables
        if not self.output.check_input(self.io.file, cm.bin.no_file): return widget.toggle_loading()
        if not self.output.check_input(len(self.io.foreground), cm.bin.no_classes): return widget.toggle_loading()
            
        # compute the bin map
        try:
        
            # update byte list 
            self.io.update_byte_list()
        
            # create a bin map 
            bin_map = cs.set_byte_map(
                self.io.byte_list, 
                self.io.file, 
                self.io.process, 
                self.output
            )
            
            self.io.set_bin_map(bin_map)
            
            # add the bin map to the download btn
            
        except Exception as e:
            self.output.add_live_msg(str(e), 'error')
                
            
        # release the btn 
        widget.toggle_loading()
            
        return 
    
    def _on_change(self, change):
        """update the list according to the file selection"""
        
        # empty all select
        self.background.v_model = None
        self.foreground.model = None
                
        # get all unique values from the image
        features = cs.unique(change['new'])
        
        # add the new list as items 
        self.background.items = features
        self.foreground.items = features
        
        return
        
        
class ThreeBytes(sw.Tile):
    
    def __init__(self, io):
        
        # gather the io 
        self.io = io
        
        # create the widgets
        self.file = sw.FileInput(['.tif', '.tiff'])
        self.lc_1 = v.Select(label = 'Dominant land cover 1 (Agriculture)', items = None, v_model = None, chips = True, multiple = True)
        self.lc_2 = v.Select(label = 'Dominant land cover 2 (Natural)', items = None, v_model = None, chips = True, multiple = True)
        self.lc_3 = v.Select(label = 'Dominant land cover 3 (developped)', items = None, v_model = None, chips = True, multiple = True)
        
        requirements = sw.Markdown(cm.requirement._3)

        # bind it to the io
        self.output = sw.Alert() \
            .bind(self.file, self.io, 'file') \
            .bind(self.lc_1, self.io, 'lc_1') \
            .bind(self.lc_2, self.io, 'lc_2') \
            .bind(self.lc_3, self.io, 'lc_3')
        
        # create the btn 
        btn = sw.Btn("Convert the image classes")
        
        super().__init__(
            self.io.tile_id,
            "Select map classes",
            inputs = [
                requirements,
                self.file,
                self.lc_1,
                self.lc_2,
                self.lc_3
            ],
            output = self.output,
            btn = btn
        
        )
        
        # bind js event
        btn.on_event('click', self._on_click)
        self.file.observe(self._on_change, 'v_model')
        
    def _on_click(self, widget, event, data):
            
        # silence the btn 
        widget.toggle_loading()
            
        # check variables
        if not self.output.check_input(self.io.file, cm.bin.no_file): return widget.toggle_loading()
        if not self.output.check_input(len(self.io.lc_1), cm.bin.no_classes): return widget.toggle_loading()
            
        # compute the bin map
        try:
        
            # update byte list 
            self.io.update_byte_list()
        
            # create a bin map 
            bin_map = cs.set_byte_map(
                self.io.byte_list, 
                self.io.file, 
                self.io.process, 
                self.output
            )
            
            self.io.set_bin_map(bin_map)
            
            # add the bin map to the download btn
            
        except Exception as e:
            self.output.add_live_msg(str(e), 'error')
                
            
        # release the btn 
        widget.toggle_loading()
            
        return 
    
    def _on_change(self, change):
        """update the list according to the file selection"""
        
        # empty all select
        self.lc_1.v_model = None
        self.lc_2.model = None
        self.lc_3.model = None 
                
        # get all unique values from the image
        features = cs.unique(change['new'])
        
        # add the new list as items 
        self.lc_1.items = features
        self.lc_2.items = features
        self.lc_3.items = features
        
        return
    
class ZeroBytes(sw.Tile):
    
    def __init__(self, io):
        
        # gather the io 
        self.io = io
        
        # create the widgets
        self.file = sw.FileInput(['.tif', '.tiff'])
        
        requirements = sw.Markdown(cm.requirement._0)

        # bind it to the io
        self.output = sw.Alert() \
            .bind(self.file, self.io, 'file') 
        
        # create the btn 
        btn = sw.Btn("Convert the image classes")
        
        super().__init__(
            self.io.tile_id,
            "Select map classes",
            inputs = [
                requirements,
                self.file, 
            ],
            output = self.output,
            btn = btn
        
        )
        
        # bind js event
        btn.on_event('click', self._on_click)
        
    def _on_click(self, widget, event, data):
            
        # silence the btn 
        widget.toggle_loading()
            
        # check variables
        if not self.output.check_input(self.io.file, cm.bin.no_file): return widget.toggle_loading()
            
        # compute the bin map
        try:
        
            # update byte list 
            self.io.update_byte_list()
        
            # create a bin map 
            bin_map = cs.set_byte_map(
                self.io.byte_list, 
                self.io.file, 
                self.io.process, 
                self.output
            )
            
            self.io.set_bin_map(bin_map)
            
            # add the bin map to the download btn
            
        except Exception as e:
            self.output.add_live_msg(str(e), 'error')
                
            
        # release the btn 
        widget.toggle_loading()
            
        return
        