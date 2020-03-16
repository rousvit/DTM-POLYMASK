# ****************************** #
# This script will open xyz file with points
# and make a shapefile from it.
# ****************************** #

import pandas as pd
import os

# First, load the layer and validate it
vectorLyr =  QgsVectorLayer('D:\\OneDrive\\AA_grania\\00_projekty\\podklady_mapove\\body\\point_mask.shp', 'Polygon' , "ogr")
vectorLyr.isValid()

# access the layer's data provider
vpr = vectorLyr.dataProvider()

# set path for data files
indir = # set full path here

# set file list in txt in the data folder
file_list = indir + '\\' + 'file_list.txt'
line_list = [line. rstrip('\n') for line in open(file_list)]

skip_counter = 0

# load files in folder and build a polygon
for root, dirs, files in os.walk(indir):        
    for file in files:
        fullname = os.path.join(root, file).replace('\\', '/')
        filename = os.path.splitext(os.path.basename(fullname))[0]
        
        if filename in line_list:
            skip_counter += 1
            
        else:
            if file.endswith('.xyz'):
                print("processing new point file" + " " + filename)
                
                # find maximal and minimal coordinate values
                point_table = pd.read_csv(fullname, delimiter=' ', header=None)
                x_max = point_table[0].max()
                x_min = point_table[0].min()
                y_max = point_table[1].max()
                y_min = point_table[1].min()
                
                # build a list of points for the polygon
                points = []
                points.append(QgsPointXY(x_min, y_min))
                points.append(QgsPointXY(x_max, y_min))
                points.append(QgsPointXY(x_max, y_max))
                points.append(QgsPointXY(x_min, y_max))
                
                # create a geometry object and ingest the points as a polygon. 
                # We nest our list of points in another list because a polygon 
                # can have inner rings, which will consist of additional lists 
                # of points being added to this list:
                poly = QgsGeometry.fromPolygonXY([points])
                
                # get the fields object for the layer
                fields = vpr.fields()
                
                # build the feature object and add the points and set geometry
                f = QgsFeature(fields)
                f.setGeometry(poly)
                
                # Adding an attribute
                f['nazev'] = filename
                
                vpr.addFeatures([f])
                vectorLyr.updateExtents()
                
                # open text file with already processed file names
                # and append the new filename
                file = open(file_list, "a")
                file.write(filename + "\n")
                file.close()
                
                print(filename + " " + "processed, file_list.txt updated")
                print("")
                
print(str(skip_counter) + " " + "files skiped")
