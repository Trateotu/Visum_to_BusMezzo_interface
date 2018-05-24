import numpy as np

from visumAttributes import *
from fileWriter import *


def make_Demand(Visum):
    MAIN_PATH = Visum.GetPath(2)

    od_list = Visum.Lists.CreateLineRouteList
    od_list.AddColumn("BM_Start_Node_No")
    od_list.AddColumn("BM_End_Node_No")

    in_list = od_list.SaveToArray()

    zeros_column = np.zeros((len(in_list),1))
    in_list = np.hstack((in_list, zeros_column))
    ATTR_LIST_ODPAIRS = np.vstack({tuple(od_path) for od_path in in_list})
    TYPE_LIST_ODPAIRS = [int, int, float]

    file = open(MAIN_PATH+'demand.dat', 'w')
    file.write("od_pairs: " + str(len(ATTR_LIST_ODPAIRS)) + LINE_NEW)
    file.write("scale: 1.0" + LINE_NEW)
    addTable(file,"",ATTR_LIST_ODPAIRS, TYPE_LIST_ODPAIRS)
    file.close()

def make_Hist_Times(Visum):
    MAIN_PATH = Visum.GetPath(2)

    file = open(MAIN_PATH+'\\histtimes.dat', 'w')
    file.write("links: " + str(Visum.Net.Links.CountActive) + LINE_NEW)
    file.write("periods: 1" + LINE_NEW)
    file.write("periodlength: 3600" + LINE_NEW)
    addTable(file, "", Visum.Net.Links.GetMultipleAttributes(ATTR_LIST_LINKS_HISTTIMES, True), TYPE_LIST_LINKS_HISTTIMES)
    file.close()

def make_Net(Visum):
    MAIN_PATH = Visum.GetPath(2)

    file = open(MAIN_PATH+'\\net.dat', 'w')
    addTable(file,"servers",[[0,0,0,0,0]], [int, int, int, int, int])
    addTable(file,"nodes",Visum.Net.Nodes.GetMultipleAttributes(ATTR_LIST_NODES), TYPE_LIST_NODES)
    addTable(file,"sdfuncs",Visum.Net.LinkTypes.GetMultipleAttributes(ATTR_LIST_LINKTYPES, True), TYPE_LIST_LINKTYPES)
    addTable(file,"links",Visum.Net.Links.GetMultipleAttributes(ATTR_LIST_LINKS, True), TYPE_LIST_LINKS)
    file.close()

def make_Turnings(Visum):
    MAIN_PATH = Visum.GetPath(2)
    file = open(MAIN_PATH+'\\turnings.dat', 'w')
    addTable(file, "turnings",Visum.Net.Turns.GetMultipleAttributes(ATTR_LIST_TURNS, True), TYPE_LIST_TURNS)
    file.write("giveways:0")
    file.close()

def make_Vehicle_Mix(Visum):
    MAIN_PATH = Visum.GetPath(2)
    file = open(MAIN_PATH+'\\vehiclemix.dat', 'w')
    file.write("vtypes: 5" + LINE_NEW)
    file.write(LIST_BEGIN + "1 NewCars 0.410 6.0" + LIST_END_NL)
    file.write(LIST_BEGIN + "2 OldCars 0.400 6.0" + LIST_END_NL)
    file.write(LIST_BEGIN + "3 Taxis 0.100 6.0" + LIST_END_NL)
    file.write(LIST_BEGIN + "5 Trucks 0.090 16.0" + LIST_END_NL)
    file.write(LIST_BEGIN + "4 Buses 0.000 13.0" + LIST_END_NL)
    file.close()

def make_Routes(Visum):
    MAIN_PATH = Visum.GetPath(2)
    file = open(MAIN_PATH+'\\routes.dat', 'w')
    addTable(file, "routes",Visum.Net.LineRoutes.GetMultipleAttributes(ATTR_LIST_ROUTES), TYPE_LIST_ROUTES)
    file.close()

# BusMezzo input files

def make_Transit_Demand(Visum):
    MAIN_PATH = Visum.GetPath(2)

    MatNo = str(int(Visum.Net.DemandSegments.ItemByKey("X").ODMatrix.AttValue("No")))

    ### previous version - passenger demand derived from the PuT stop-level matrix:

    ### !!! make sure that the [StopPoint-level PuT matrix] is already calculated in Visum !!! ###
    ### Calculate -> General procedure settings -> PuT settings -> Assignment -> ...           ###
    ### ... -> tick [Save the volume matrix between stop points on the path level] -> ...      ###
    ### ... -> run [PuT Assignment] -> save the .ver file                                      ###

    # od_list = Visum.Lists.CreatePuTStopPointVolumeMatrixPathList
    # od_list.AddColumn("FromStopPointNo")
    # od_list.AddColumn("ToStopPointNo")
    # od_list.AddColumn("Volume(AP)")

    # ATTR_LIST_TRANSITODPAIRS = od_list.SaveToArray()
    # TYPE_LIST_TRANSITODPAIRS = [int, int, int]

    file = open(MAIN_PATH+'\\transit_demand.dat', 'w')
    file.write("passenger_rates: " + str(Visum.Net.ODPairs.Count) + LINE_NEW)
    file.write("format: 3" + LINE_NEW)

    ATTR_LIST_TRANSITODPAIRS.append("MatValue({})".format(MatNo))
    addTable(file, "", Visum.Net.ODPairs.GetMultipleAttributes(ATTR_LIST_TRANSITODPAIRS), TYPE_LIST_TRANSITODPAIRS)
    file.close()

def make_Transit_Fleet(Visum):
    MAIN_PATH = Visum.GetPath(2)

    file = open(MAIN_PATH + '\\transit_fleet.dat', 'w')
    ATTR_LIST_DWELL_TIME_FUNCTIONS = [[1,11,0.0,2.0,2.0,2.0,0.0,2.0],[2,11,0.0,2.0,2.0,2.0,0.0,2.0]]
    TYPE_LIST_DWELL_TIME_FUNCTIONS = [int, int, float, float, float, float, float, float]
    addTable(file, "dwell_time_functions",ATTR_LIST_DWELL_TIME_FUNCTIONS, TYPE_LIST_DWELL_TIME_FUNCTIONS)
    addTable(file, "vehicle_types",Visum.Net.VehicleUnits.GetMultipleAttributes(ATTR_LIST_VEHICLEUNITS), TYPE_LIST_VEHICLEUNITS)
    addTable(file, "vehicle_scheduling",Visum.Net.VehicleJourneys.GetMultipleAttributes(ATTR_LIST_VEHICLEJOURNEYS), TYPE_LIST_VEHICLEJOURNEYS)
    file.close()

def make_Transit_Network(Visum):

    # STOPS data:
    MAIN_PATH = Visum.GetPath(2)

    file = open(MAIN_PATH + '\\transit_network.dat', 'w')
    addTable(file, "stops",Visum.Net.StopPoints.GetMultipleAttributes(ATTR_LIST_STOPPOINTS), TYPE_LIST_STOPPOINTS)

    # STOPS_DISTANCES{...} - list export and processing steps:

    ### 1. STOP_AREA_TRANSFERS - within-stop walking links
    # 1a. create StopArea transfer matrix
    walk_list = Visum.Lists.CreateStopTransferWalkTimeList
    walk_list.AddColumn("FromStopAreaNo")
    walk_list.AddColumn("ToStopAreaNo")
    walk_list.AddColumn("Time(W)")
    # walk_list.AddColumn("ToStopAreaNo",GroupOrAggrFunction=10)
    # walk_list.AddColumn("Time(W)",GroupOrAggrFunction=10)
    in_list = np.array(walk_list.SaveToArray())

    # 1b. remove duplicates and transfers within the same stop
    for row in in_list:
        if row[0] == row[1]:
            row[0:2] = 0
        else:
            pass
    in_list = in_list[~(in_list==0).all(1)]

    # 1c. finally - prepare a BusMezzo-adequate input list
    out_list = dict()
    from_stops = [r[0] for r in in_list]
    for r in in_list:
        if r[0] in out_list.keys():     # apparently this is not accessed
            out_list[r[0]][-1].append([r[1], r[2]])
        else:
            toAdd = []
            toAdd.append([r[1], r[2]])
            out_list[r[0]] = [[r[0], from_stops.count(r[0]), toAdd[0]]]

    ATTR_LIST_STOPAREAS = out_list.values()
    # quick-fix -  remove outer brackets
    ATTR_LIST_STOPAREAS = [i[0] for i in ATTR_LIST_STOPAREAS]
    ### !!! sprawdzic to jeszcze
    TYPE_LIST_STOPAREAS = [int, int, int, float]

    ### 2. ORIGIN/DESTINATION TRANSFERS - map Connectors(Zone<=>Stop) into additional walking links

    # 2a. create list of Connector walking links
    conn_list = Visum.Lists.CreateConnectorList
    conn_list.AddColumn("BM_OrigPointData")
    conn_list.AddColumn("BM_DestPointData")
    conn_list.AddColumn("T0_TSys(W)")
    in_conn_list = [[str(x) for x in row] for row in np.array(conn_list.SaveToArray())]
    out_conn_list = []

    # 2b. prepare a BusMezzo-adequate input list
    for connector in in_conn_list:
        if connector[0] == '':      # skip non-origin connectors
            pass
        else:                       # add origin connectors' data only
            zone_connections = []
            orig_point = connector[0]
            dest_points = connector[1].split(',')
            conn_walk_time = connector[2]
            num_connections = len(dest_points)
            stop_connections = []
            for i in dest_points:
                stop_connections.append([int(i), float(conn_walk_time)])
            zone_connections.append(int(orig_point))
            zone_connections.append(num_connections)
            for list_of_walk_connections in stop_connections:
                zone_connections.append(list_of_walk_connections)

        out_conn_list.append(zone_connections)

    ATTR_LIST_CONNECTORS = out_conn_list
    # quick-fix -  remove outer brackets
    # ATTR_LIST_CONNECTORS = [i[0] for i in ATTR_LIST_STOPAREAS]
    ### !!! sprawdzic to jeszcze
    TYPE_LIST_CONNECTORS = [int, int, int, float]

    ### 3. WRITE OUTPUT TO .DAT FILE

    file.write("stops_distances: " + str(len(out_list)) + LINE_NEW)
    file.write("format: 1" + LINE_NEW)
    addTable(file, "", ATTR_LIST_STOPAREAS, TYPE_LIST_STOPAREAS)
    addTable(file, "", ATTR_LIST_CONNECTORS, TYPE_LIST_CONNECTORS)

    # LINES / TRIPS data:

    file.write("lines: " + str(Visum.Net.LineRoutes.Count) + LINE_NEW)
    addTable(file,"",Visum.Net.LineRoutes.GetMultipleAttributes(ATTR_LIST_LINEROUTES), TYPE_LIST_LINEROUTES)
    file.write("trips: " + str(Visum.Net.LineRoutes.Count) + LINE_NEW)
    # if trips format:2
    file.write("format: 2" + LINE_NEW)
    addTable(file,"",Visum.Net.TimeProfiles.GetMultipleAttributes(ATTR_LIST_TIMEPROFILES_format2), TYPE_LIST_TIMEPROFILES_format2)
    # if trips format:3
    file.write("format: 3" + LINE_NEW)
    addTable(file,"",Visum.Net.TimeProfiles.GetMultipleAttributes(ATTR_LIST_TIMEPROFILES_format3), TYPE_LIST_TIMEPROFILES_format3)

    file.write("travel_time_disruptions: 0" + LINE_NEW)
    file.close()

def make_Transit_Routes(Visum):
    MAIN_PATH = Visum.GetPath(2)

    file = open(MAIN_PATH + '\\transit_routes.dat', 'w')
    addTable(file, "routes", Visum.Net.LineRoutes.GetMultipleAttributes(ATTR_LIST_ROUTES), TYPE_LIST_ROUTES)
    file.close()

if __name__ == "__main__":
    pass
