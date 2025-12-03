

def selection_neha_noLengthEnergy( frame, topology ):
    """
    Cascade: 1
    Double: 2
    Track: 3
    
    FinalTopology does not contain extra high energy/low length cut to move
    high energy NuE out of the double cascade sample
    """

    print("selection_neha_noLengthEnergy", frame["FinalTopology"], topology, frame["FinalTopology"] == topology)
    return frame["FinalTopology"] == topology

def selection_neha_withLengthEnergy( frame, topology ):
    """
    Cascade: 1
    Double: 2
    Track: 3
    
    FinalTopology does not contain extra high energy/low length cut to move
    high energy NuE out of the double cascade sample
    """

    print("selection_neha_noLengthEnergy", frame["FinalEventClass"], topology, frame["FinalEventClass"] == topology)
    return frame["FinalEventClass"] == topology
