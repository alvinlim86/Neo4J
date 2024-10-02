import win32com.client as win32 #import COM

def openHysys(hyFilePath):
    hyApp = win32.Dispatch('HYSYS.Application')
    hyCase = hyApp.SimulationCases.Open(hyFilePath)
    hyCase.Visible = True

    # def AccessFlowsheets()
    material_streams = hyCase.Flowsheet.MaterialStreams
    energy_streams = hyCase.Flowsheet.EnergyStreams
    current_operations = hyCase.Flowsheet.Operations

#def set_components(args):
    componentsList = ["Water", "Methane"]
    componentsMolarFraction = [0.9, 0.1]

#def add_material_stream()
    new_stream = material_streams.add("1")
    new_stream.MassFlow.setValue(1000, "kg/h")
    new_stream.Temperature.setValue(25, "C")
    new_stream.Pressure.setValue(1, "bar_g")
    new_stream.MolarFraction.setValue(componentsMolarFraction)
    #to test new_stream.Components.Add(componentsList, componentsMolarFraction)

#def print_feedstream_pressure()
    #streamPress = hyCase.Flowsheet.MaterialStreams.Item("FeedStream").Pressure.setValue(3,"bar_g")
    streamPress = hyCase.Flowsheet.MaterialStreams.Item("FeedStream").Pressure.setValue(400,"kPa")
    streamPress = hyCase.Flowsheet.MaterialStreams.Item("FeedStream").Pressure.getValue("kPa")
    print(streamPress," kPa")

    streamPress = hyCase.Flowsheet.MaterialStreams.Item("FeedStream").Pressure.getValue("bar_g")
    print(streamPress, " bar_g")

#def print_operation_properties()
    compEff = hyCase.Flowsheet.Operations.Item("K-100").CompPolytropicEff
    exArea = hyCase.Flowsheet.Operations.Item("E-101").HeatTransferArea
    print(compEff, " %")
    print(exArea," m2")

    return()

if __name__ == "__main__":
    # Set constants and variables
    hyFilePath = r"C:\Users\Documents\test.hsc"
        
    # Call functions, depends whether async is necessary
    openHysysCase = openHysys(hyFilePath)