import sys

from PySide.QtCore import *
from PySide.QtGui import *

from IPython import embed

class ToolPaletteGroup(QVBoxLayout):
    
    def __init__(self,*args,**kwargs):
        QVBoxLayout.__init__(self,*args,**kwargs)
        self._widget_groups = {}
        self._width_groups = {}
        self._all_widths_linked = False
    
    # Creates and appends a new ToolPalette to this group
    # A reference to the new ToolPalette is returned
    def append_new_palette(self,name,*args,**kwargs):
        if name in self._widget_groups:
            raise RuntimeError('The tool palette group already has a palette named %s'%name)
            
        # Create the tool palette and store a reference to it and an index indicating the order of Tool Palettes
        tool_palette = ToolPalette(self,name,*args,**kwargs)
        push_button = QPushButton(name)        
        push_button.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
        
        def create_callback(name):
            return lambda: self._on_button_clicked(name)
            
        push_button.clicked.connect(create_callback(name))
        self._widget_groups[name] = (len(self._widget_groups),tool_palette, push_button)
        
        # append to the layout
        self.addWidget(push_button)
        self.addWidget(self._widget_groups[name][1])
        
        return tool_palette
     
    def _on_button_clicked(self,name):
        # work out if it is shown or hidden
        #call show or hide method
        if self._widget_groups[name][1].isHidden():
            self.show_palette(name)
        else:
            self.hide_palette(name)
        
        
    def show_palette(self,name):
        if name not in self._widget_groups:
            raise RuntimeError('The tool palette does not have a palette named %s'%name)
            
        self._widget_groups[name][1].show()
        #TODO: Update icon on the button
            
    def show_palette_by_index(self,index):
        self.show_palette(self.get_name_from_index(index))
    
    def hide_palette(self,name):    
        if name not in self._widget_groups:
            raise RuntimeError('The tool palette does not have a palette named %s'%name)
        
        self._widget_groups[name][1].hide()
        
        #TODO: Update icon on the button
    
    def hide_palette_by_index(self,index):
        self.hide_palette(self.get_name_from_index(index))
     
    # Creates and inserts a new ToolPalette at the specified index.
    # A reference to the new ToolPalette is returned
    def insert_new_palette(self,index,name,*args,**kwargs):
        # insert ...
        pass
    
    def get_palette(self,name):        
        if name not in self._widget_groups:
            raise RuntimeError('The tool palette group does not contain a palette named %s'%name)
            
        return self._widget_groups[name][1]
    
    def get_palette_by_index(self,index):
        return self.get_palette(self.get_name_from_index(index))
    
    def reorder_palette(self,name,new_index):
        if name not in self._widget_groups:
            raise RuntimeError('The tool palette group does not contain a palette named %s'%name)
            
        return self.reorder_palette_by_index(self.get_index_from_name(name),new_index)
    
    def reorder_palette_by_index(self,old_index,new_index):
        if old_index < 0 or old_index >= count(self._widget_groups):
            raise RuntimeError('The specified old_index is out of bounds')
            
        if new_index < 0 or new_index >= count(self._widget_groups):
            raise RuntimeError('The specified new_index is out of bounds')    
            
        # TODO: now perform the reorder
        
        # TODO: recreate the layout
        
    def remove(self,name):
        if name not in self._widget_groups:
            raise RuntimeError('The tool palette group does not contain a palette named %s'%name)
            
        # TODO: Remove
        
    def remove_by_index(self,index):
       return self.remove(self.get_name_from_index(index))
    
    def get_name_from_index(self,index):
        for name, palette_data in self._widget_groups.items():
            if palette_data[0] == index:
                return name
                
        raise RuntimeError('The tool palette group does not contain a palette with index %d'%index)
        
    def get_index_from_name(self,name):
        if name not in self._widget_groups:
            raise RuntimeError('The tool palette group does not contain a palette named %s'%name)
            
        return self._widget_groups[name][0]
    
    ############################################################################################################################
    # The code below is related solely to linking the widths of items within several tool palettes that are part of this group #
    ############################################################################################################################
    
    # This property links the widths of all ToolPalettes in the ToolPalette group
    # It is a convenience property so that you don't have to create a linked_width_group conatining all Tool palettes in the tool palette group
    # and maintain the linked_width_group after ading new Tool Palettes to the Tool Palette Group
    @property
    def widths_linked(self):
        return self._all_widths_linked
    
    @widths_linked.setter
    def widths_linked(self,value):
        if self._width_groups and self._all_widths_linked:
            raise RuntimeError('You cannot link the widths of all tool palettes if you have already created a linked width group')
    
        self._all_widths_linked = value
    
    # This function links the widths of items in several ToolPalettes.
    def create_linked_width_group(self,width_group_name,names):
        if self._all_widths_linked:
            raise RuntimeError('You cannot create a linked_width_group if you have already linked all widths via the widths_linked_property')
    
        if width_group_name in self._width_groups:
            raise RuntimeError('The tool palette group already has a width group named %s'%width_group_name)
        
        # check if anything in names is already in another width group
        for width_group_name,width_group_data in self._width_groups.items():
            for name in names:
                if name in width_group_data[1]:
                    raise RuntimeError('The tool pallete named %s is already in the linked width group %s'%(name,width_group_name))
        
        # create width group
        self._width_groups[width_group_name] = (self._create_find_max_function(width_group_name),names)
    
    # This function adds the toolpallete called 'name' to the linked_width_group 'width_group_name'
    def add_to_linked_width_group(self,width_group_name,name):
        if self._all_widths_linked:
            raise RuntimeError('You cannot add to a linked_width_group if you have already linked all widths via the widths_linked_property')
            
        if width_group_name not in self._width_groups:
            raise RuntimeError('The tool palette group does not have a width group named %s'%width_group_name)
    
        for width_group_name,width_group_data in self._width_groups.items():
            if name in width_group_data[1]:
                raise RuntimeError('The tool pallete named %s is already in the linked width group %s'%(name,width_group_name))
        
        self._width_groups[width_group_name][1].append(name)
        # recreate the find_max_item_width function
        self._width_groups[width_group_name] = (self._create_find_max_function(width_group_name),self._width_groups[width_group_name][1])
    
    def remove_from_linked_width_group(self,width_group_name,name):
        pass
        #TODO:
    
    # This function creates and returns a reference to a function which finds the widest item in all Tool palettes in the specified
    # linked_width_group.
    def _create_find_max_function(self,width_group_name):
        def find_max_item_width():
            largest_item_width = 0
            for tp_name in self._width_groups[width_group_name][1]:
                item_width = self._widget_groups[tp_name][1]._find_max_item_width()
                if item_width > largest_item_width:
                    largest_item_width = item_width                    
            return largest_item_width            
        return find_max_item_width
        
    # This function gives the tool palletes a function to call to find out the widest item in their linked_width_group
    def _find_max_item_width(self,name):
        if self._all_widths_linked:
            return lambda: max([palette[1]._find_max_item_width() for palette in self._widget_groups.values()])
            
        # Look up to see if the tool palette is in a linked_width_group
        width_group = None
        for width_group_name,width_group_list in self._width_groups.items():
            if name in width_group_list[1]:
                width_group = width_group_name
                break
        
        if width_group:
            return self._width_groups[width_group][0]
        else:
            return self._widget_groups[name][1]._find_max_item_width
        
        
class ToolPalette(QScrollArea):
    def __init__(self,parent,name,*args,**kwargs):
        QScrollArea.__init__(self,*args,**kwargs)
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
        # create the grid layout
        #self.setWidget(QWidget(self))
        #self.widget().setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self._layout = QGridLayout(self) 
        #self._layout.setMaximumSize(QSize(524287,524287))
        #self._layout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self._widget_list = []
        self._parent_group = parent
        self._name = name
        
        # need to keep track of these internally because the GridLayout returns the number of 
        # allocated rows/columns with columnCount()/RowCount() rather than the number of visible ones
        self._column_count = 0
        self._row_count = 0
        
    def addWidget(self,widget):
        # Append to end of tool pallete
        #widget.clicked.connect(embed)
        self._widget_list.append(widget)
        self._layout_widgets()
        
    def insertWidget(self,index,widget):
        # Insert into position 'index'
        self._widget_list.insert(index,widget)
        self._layout_widgets()
    
    def _find_max_item_width(self):
        # find the minimum size of the widest widget in the grid layout
        w_size_hints = [w.minimumSizeHint().width() for w in self._widget_list]
        if len(w_size_hints) < 1:
            return 0
        max_width = max(w_size_hints)
        return max_width
    
    def _layout_widgets(self):
        h_size_hints = [w.sizeHint().height() for w in self._widget_list]
        max_width = self._parent_group._find_max_item_width(self._name)()
        
        # find the width of the gridlayout
        layout_width = self.size().width()
        #layout_width = self._layout.sizeHint().width()
        layout_spacing = self._layout.horizontalSpacing()
        
        # How many widgets can fit in a row?
        # TODO: Work out hwy I need layout_spacing*3 here (we are getting the width of the scroll area, 
        # so need to take into account the borders around the grid layout? What are they?)
        num_widgets_per_row = int((layout_width-layout_spacing*3)/(max_width+layout_spacing))
        
        if num_widgets_per_row < 1:
            num_widgets_per_row = 1
        elif num_widgets_per_row > len(self._widget_list):
            num_widgets_per_row = len(self._widget_list)
            
        if num_widgets_per_row != self._column_count:            
            print 'changing number of columns'
            # remove all widgets
            for widget in self._widget_list:
                self._layout.removeWidget(widget)
            
            # re add all widgets into the grid layout
            row = 0
            column = 0
            for widget in self._widget_list:
                self._layout.addWidget(widget,row,column)
                column += 1
                if column >= num_widgets_per_row:
                    column = 0
                    row += 1
                    
            # This is here because the row count may have been increased at the end of the insertion
            # loop
            if column != 0:
                row += 1
            # update the row/column count
            self._column_count = num_widgets_per_row
            self._row_count = row

            # print (max(h_size_hints)+self._layout.verticalSpacing())*self._row_count+self._layout.verticalSpacing()*2
            # print max(h_size_hints)
            # print self._layout.verticalSpacing()
            # print self._row_count
            
            self.setMinimumSize(QSize(self.minimumSize().width(),(max(h_size_hints)+self._layout.verticalSpacing())*self._row_count+self._layout.verticalSpacing()*2))
            for i in range(self._layout.rowCount()):
                if i < self._row_count:
                    self._layout.setRowMinimumHeight(i,max(h_size_hints))
                else:
                    self._layout.setRowMinimumHeight(i,0)
        

    def resizeEvent(self, event):
        # overwrite the resize event!
        # print '---------'
        # print self._widget_list[0].size()
        # print self._widget_list[0].sizeHint()
        # print self._widget_list[0].minimumSizeHint()
        # print self._layout.rowMinimumHeight(0)
        # print self.size()
        # print self.minimumSize()
        # print self.sizeHint()
        # print self.minimumSizeHint()
        #pass resize event on to qwidget
        # call layout()
        QWidget.resizeEvent(self,event)
        self._layout_widgets()


# A simple test!
if __name__ == '__main__':
    
    qapplication = QApplication(sys.argv)
    
    window = QWidget()
    layout = QVBoxLayout(window)
    widget = QWidget()
    layout.addWidget(widget)
    tpg = ToolPaletteGroup(widget)
    toolpalette = tpg.append_new_palette('Digital Outputs')
    toolpalette2 = tpg.append_new_palette('Digital Outputs 2')
    #toolpalette = ToolPalette()
    #layout.addWidget(toolpalette)
    #layout.addItem(tpg)
    #toolpalette.show()
    
    layout.addItem(QSpacerItem(0,0,QSizePolicy.Minimum,QSizePolicy.MinimumExpanding))
    for i in range(20):
        button = QPushButton('Button %d'%i)
        
        button.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        toolpalette.addWidget(button)
        
    for i in range(20):
        button = QPushButton('very very long Button %d'%i)
        
        button.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        toolpalette2.addWidget(button)
    
    #tpg.create_linked_width_group("Digital outs", ['Digital Outputs','Digital Outputs 2'])
    
    window.show()
    
    
    sys.exit(qapplication.exec_())
    