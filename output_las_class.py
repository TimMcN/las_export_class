import argparse
import os
import json
from osgeo import ogr
from osgeo import gdal



def arguments():
    parser = argparse.ArgumentParser(description='LAS/LAZ -> GTiff Converter')
    parser.add_argument('input_filename')
    parser.add_argument('output_filename')
    parser.add_argument('--pointclass', type=int, default=1,
                        help = "Set the resolution of the output GTiff")
    parser.add_argument('--in_epsg', type =str, default="2157",
                        help = "--myDictObjInEPSG <EPSG Code>, if left blank input EPSG is assumed to be 2157")
    parser.add_argument('--out_epsg', type =str, default="2157",
                        help = "--OutEPSG <EPSG Code>, if left blank output EPSG is defaults to 2157")
    return parser.parse_args()


def buildPipeInput(in_epsg,out_epsg, filename):
    if filename.split('.')[1]=="las"or filename.split('.')[1]=="laz":
        epsg = in_epsg
        myDictObj = {"pipeline":[{"type": "readers.las", "spatialreference": "EPSG:"+epsg,
        "filename":filename},
        {"type":"filters.reprojection", "in_srs": "EPSG:"+in_epsg,
        "out_srs":"EPSG:"+out_epsg},
        ]}
        return myDictObj
    else:
        print("Error: Invalid input file")

def appendClassFilter(myDictObj):
    myDictObj["pipeline"].append({
    "type":"filters.range",
    "limits":("Classification[%i:%i]" %(args.pointclass,args.pointclass))
    })
    return myDictObj

def append_las_writer(myDictObj, output_filename):
    myDictObj["pipeline"].append({
    "type":"writers.las",
    "filename": output_filename,
    })
    return myDictObj

def output_las():
    myDictObj = buildPipeInput(args.in_epsg, args.out_epsg, args.input_filename)
    myDictObj = appendClassFilter(myDictObj)
    myDictObj = append_las_writer(myDictObj, args.output_filename.split('.')[0]+".las")
    with open ('scratchpipeline.json', 'w') as outfile:
        json.dump(myDictObj, outfile)
    os.system("pdal pipeline scratchpipeline.json")
    #cleanup()

def cleanup():
    files = os.listdir()
    for file in files:
        if (file.startswith("scratch")):
            os.remove(file)

args = arguments()
output_las()
