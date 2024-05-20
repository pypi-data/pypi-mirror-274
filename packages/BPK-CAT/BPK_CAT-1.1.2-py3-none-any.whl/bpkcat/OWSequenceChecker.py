import pandas as pd
from Orange.data import Table
from Orange.data.pandas_compat import table_from_frame, table_to_frame
from Orange.widgets.widget import OWWidget, Input, Output

class OWSequenceChecker(OWWidget):
    name = "Sequence Checker"
    description = "Checks sequence of numbers"
    icon = "icons/1.svg"
    priority=10
    
    class Inputs:
        data = Input("Data", Table)
        
    class Outputs:
        ouput_data = Output("Output Data", Table)
        
    want_main_area = False
    want_control_area = False
    
    def __init__(self):
        super().__init__()
        self.data = None
        
    @Inputs.data
    def set_data(self, data):
        """Set input data."""
        self.data = data
        if data is not None:
            self.process_data(data)
            
    def process_data(self, data):
        """Process the input data."""
        df = table_to_frame(data)
        checkColumn = len(df.columns)
        
        if checkColumn == 1:
            result = []
            seedinit = df.iloc[:, 0]
            anchor = seedinit.iloc[0]
            for i in seedinit:
                if anchor > i:
                    tmp = (str(i) + 'Error Sequence')
                else:
                    tmp = str(i)
                result.append(tmp)
                anchor = i
        else:
            result = ["Must select one column to test"]
        
        doutput = {"SeqID": result}
        df_output = pd.DataFrame(doutput)
        out_data = table_from_frame(df_output)
        
        self.Outputs.ouput_data.send(out_data)    
        