from Orange.data import Table
from Orange.data.pandas_compat import table_from_frame, table_to_frame
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui
from Orange.widgets.settings import Setting

class OWDuplicateChecker(OWWidget):
    name = "Duplicate Checker"
    description = "Checks for duplicate rows in dataset"
    icon = "icons/2.svg"
    priority = 10
    
    class Inputs:
        data = Input("Data", Table)
        
    class Outputs:
        output_data = Output("Output Data", Table)
        
    want_main_area = False
    want_control_area = True
    
    filter_option = Setting(0) # 0: All Data, 1: Without Duplicates, 2: Only Duplicates
    
    def __init__(self):
        super().__init__()
        self.data = None
        self.duplicate_count = 0
        
        self.info_label = gui.label(self.controlArea, self, "Info: ")
        self.filter_box = gui.radioButtons(
            self.controlArea, self, "filter_option",
            btnLabels=["All Data", "Without Duplicates", "Only Duplicates"],
            callback=self.apply_filter
        )
    
    @Inputs.data
    def set_data(self, data):
        """Set input data."""
        self.data = data
        if data is not None:
            self.process_data(data)
        else:
            self.Outputs.output_data.send(None)
    
    def process_data(self, data):
        """Process the input data."""
        df = table_to_frame(data)
        duplicate_flags = df.duplicated(keep=False)
        self.duplicate_count = duplicate_flags.sum()
        self.info_label.setText(f"Info: {self.duplicate_count} duplicate rows found.")
        
        self.df = df.assign(Status=['Duplicate' if is_dup else 'Unique' for is_dup in duplicate_flags])
        self.apply_filter()
        
    def apply_filter(self):
        """Apply the selected filter to the data"""
        if self.data is None:
            return
        
        if self.filter_option == 0:
            filter_df = self.df
        elif self.filter_option == 1:
            filter_df = self.df[self.df['Status'] == 'Unique']
        elif self.filter_option == 2:
            filter_df = self.df[self.df['Status'] == 'Duplicate']
            
        out_data = table_from_frame(filter_df.drop(columns=['Status']))
        self.Outputs.output_data.send(out_data)
        