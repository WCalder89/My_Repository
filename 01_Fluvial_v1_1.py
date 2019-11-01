#This model takes the principles from the data derivation models which were
#previously hosted on Arc Toolbox(s)

#Import Modules

import os, os.path
import sys
import datetime
import arcpy
from arcpy import env
from arcpy.sa import *
import glob

arcpy.CheckOutExtension("Spatial")
now = datetime.datetime.now()
arcpy.AddMessage("Start time : ")
arcpy.AddMessage(now.strftime("%Y-%m-%d %H:%M:%S"))

arcpy.env.overwriteOutput = True
arcpy.env.workspace = arcpy.GetParameterAsText(0)


#01 Create GDBs and set up folders
#Set variables

HA= arcpy.GetParameterAsText(1)
Version= arcpy.GetParameterAsText(2) #default 1_4
GDBHoldingFolder = arcpy.GetParameterAsText(3)
outputFolder= arcpy.GetParameterAsText(4)
HABoundarySource= "\\\\sepa-app-frm01\\frmdata\\Working\\Flood Risk\\Hazard Maps\\Post Processing and Data Derivation\\Data Derivation\\Data Derivation Toolboxes\\FLUVIAL_Coastline_Clip_Polygons.gdb\\"
Grid150= "\\\\sepa-app-frm01\\frmdata\\Working\\Flood Risk\\Hazard Maps\\River_Velocity_Direction_Derivation\\Grid_150m_Scotland.shp"
Year10Extent= arcpy.GetParameterAsText(5)
Year200Extent= arcpy.GetParameterAsText(6)
Year1000Extent= arcpy.GetParameterAsText(7)
Year200CCExtent= arcpy.GetParameterAsText(8)

HA_Lochs= "\\\\sepa-app-frm01\\frmdata\Working\\Flood Risk\\Hazard Maps\\Post Processing and Data Derivation\\Data Derivation\\Data Derivation Toolboxes\\FLUVIAL_Lochs.gdb\\"+str(HA)

if len(HA)==6:
    arcpy.AddMessage("HA format OK")
    arcpy.AddMessage("Creating folders and file geodatabases")
else:
    arcpy.AddMessage("Please enter HA information in the format of \"HA_019\" and restart")
    sys.exit()

#CHECK IF FOLDERS/GDBs ALREADY EXIST- IF NOT THEN CREATE THEM
MainFolder=(outputFolder+"\\"+str(HA))
VersionFolder=(str(MainFolder)+"\\"+"Version_"+str(Version))
DDFolder=(str(VersionFolder)+"\\"+str(HA)+"_Data_Derivation_v"+str(Version))
R3TEMP= (DDFolder+"\\"+str(HA)+"_DD_R3_TEMP_v"+str(Version)+".gdb")
R3FINAL= (DDFolder+"\\"+str(HA)+"_DD_R3_FINAL_v"+str(Version)+".gdb")
R4TEMP= (DDFolder+"\\"+str(HA)+"_DD_R4_TEMP_v"+str(Version)+".gdb")
R4FINAL= (DDFolder+"\\"+str(HA)+"_DD_R4_FINAL_v"+str(Version)+".gdb")
VDPP= (DDFolder+"\\"+str(HA)+"_VD_PP_Datasets_v"+str(Version)+".gdb")

#Make raw stings
MainFolderstr= str(MainFolder)
VersionFolderstr= str(VersionFolder)
DDFolderstr= str(DDFolder)
R3TEMPstr= str(R3TEMP)
R3FINALstr= str(R3FINAL)
R4TEMPstr= str(R4TEMP)
R4FINALstr= str(R4FINAL)
VDPPstr= str(VDPP)

R3TEMPcrt=(str(HA)+"_DD_R3_TEMP_v"+str(Version)+".gdb")
R3FINALcrt=(str(HA)+"_DD_R3_FINAL_v"+str(Version)+".gdb")
R4TEMPcrt= (str(HA)+"_DD_R4_TEMP_v"+str(Version)+".gdb")
R4FINALcrt= (str(HA)+"_DD_R4_FINAL_v"+str(Version)+".gdb")
VDPPcrt= (str(HA)+"_VD_PP_Datasets_v"+str(Version)+".gdb")

FolderList= [MainFolderstr, VersionFolderstr, DDFolderstr] 
for i in FolderList:
    if not os.path.exists(i):
        arcpy.AddMessage(str(i)+ "  CREATED")
        os.makedirs(i)
    else:
        arcpy.AddMessage(str(i)+ "  ALREADY EXISTS")

GDBList=[R3TEMPcrt, R3FINALcrt, R4TEMPcrt, R4FINALcrt, VDPPcrt]
for i in GDBList:
    Pathway=DDFolder+"\\"+i
    if not os.path.exists(Pathway):
        arcpy.AddMessage(Pathway+ "  CREATED")
        arcpy.CreateFileGDB_management(str(DDFolder), i)
    else:
        arcpy.AddMessage(Pathway+ "  ALREADY EXISTS")


HABoundary= (HABoundarySource+str(HA)+"_Coast_Clip")
HABoundaryCopy= str(VDPP)+"\\"+str(HA)+"_Boundary_v"+str(Version)

arcpy.AddMessage("Preparing empty feature classes")
copyOutput= VDPPstr+"\\"+str(HA)+"_150m_GRID_PG_v"+str(Version)
Grid150Copy= arcpy.Copy_management(HABoundary,HABoundaryCopy,copyOutput)
Grid150HAClip10Yr= arcpy.Clip_analysis(Grid150Copy, Year10Extent, VDPPstr+"\\"+str(HA)+"_150m_GRID_PG_10_D_v"+str(Version))
Grid150HAClip200Yr= arcpy.Clip_analysis(Grid150Copy, Year200Extent, VDPPstr+"\\"+str(HA)+"_150m_GRID_PG_200_D_v"+str(Version))
Grid150HAClip1000Yr= arcpy.Clip_analysis(Grid150Copy, Year1000Extent, VDPPstr+"\\"+str(HA)+"_150m_GRID_PG_1000_D_v"+str(Version))
Grid150HAClip200CCYr= arcpy.Clip_analysis(Grid150Copy, Year200CCExtent, VDPPstr+"\\"+str(HA)+"_150m_GRID_PG_200_D_2080H_v"+str(Version))
Grid150HAClip10YrPT= arcpy.FeatureToPoint_management(Grid150HAClip10Yr, VDPPstr+"\\"+str(HA)+"_150m_GRID_PT_10_D_v"+str(Version), "INSIDE")
Grid150HAClip200YrPT= arcpy.FeatureToPoint_management(Grid150HAClip200Yr, VDPPstr+"\\"+str(HA)+"_150m_GRID_PT_200_D_v"+str(Version), "INSIDE")
Grid150HAClip1000YrPT= arcpy.FeatureToPoint_management(Grid150HAClip1000Yr, VDPPstr+"\\"+str(HA)+"_150m_GRID_PT_1000_D_v"+str(Version), "INSIDE")
Grid150HAClip200CCYrPT= arcpy.FeatureToPoint_management(Grid150HAClip200CCYr, VDPPstr+"\\"+str(HA)+"_150m_GRID_PT_200_D_2080H_v"+str(Version), "INSIDE")
    

#02 Check for ASCII files in data source folder
#Set variables

RasterFolder= arcpy.GetParameterAsText(8)

arcpy.AddMessage("Checking for ASCII rasters in; "+ str(RasterFolder))

if os.path.exists(RasterFolder):
    arcpy.env.workspace= RasterFolder
    ASCIICheck = arcpy.ListRasters("*asc","ALL")
    if not ASCIICheck:
        arcpy.AddMessage("No ASCII rasters found- OK")
    else:
        arcpy.AddMessage("ASCII rasters found, converting to ")
        for i in ASCIICheck:
            RasterOutput= RasterFolder+"\\"+(i[:-4])+"_G.tif"
            RasterInput= RasterFolder+"\\"+i
            arcpy.AddMessage(RasterInput)
            arcpy.ASCIIToRaster_conversion(RasterInput,RasterOutput,"FLOAT")
else:
    arcpy.AddMessage("Raster folder location not found, please check and try again.")
    sys.exit

arcpy.env.workspace= arcpy.GetParameterAsText(0)

#03 Convert D-V-V-D Raster to Classified FeatureClasses
#Set variables
arcpy.AddMessage("Converting Rasters to Classified FeatureClasses")
from arcpy.sa import *


#...DEPTHS
Depth10D= GDBHoldingFolder+"\\"+str(HA)+"_10_D_v"+str(Version)+".gdb"+"\\"+str(HA)+"_DEPTH_10_D_v"+str(Version)
Depth200D= GDBHoldingFolder+"\\"+str(HA)+"_200_D_v"+str(Version)+".gdb"+"\\"+str(HA)+"_DEPTH_200_D_v"+str(Version)
Depth1000ND= GDBHoldingFolder+"\\"+str(HA)+"_1000_ND_v"+str(Version)+".gdb"+"\\"+str(HA)+"_DEPTH_1000_ND_v"+str(Version)
Depth200CCD= GDBHoldingFolder+"\\"+str(HA)+"_200_D_2080H_67_v"+str(Version)+".gdb"+"\\"+str(HA)+"_DEPTH_200_D_2080H_67_v"+str(Version)

arcpy.AddMessage("Converting DEPTH Rasters to Classified FeatureClasses")
DepthList= [Depth10D, Depth200D, Depth1000ND, Depth200CCD]

for i in DepthList:
    if DepthList.index(i) == 0: 
        RP= "10_D"
    elif DepthList.index(i) == 1:
        RP= "200_D"
    elif DepthList.index(i) == 2:
        RP= "1000_ND"
    elif DepthList.index(i) == 3:
        RP= "200_D_2080H_67"

    #The following used map algebra rather than raster calc (which is not really meant to be used outside of desktop)
    inRaster= Raster(i)*1000
    ReclassRaster= Reclassify(inRaster, "VALUE", RemapRange([[0,300,1],[300.000001,1000,2],[1000.000001,99999.99,3],[100000,1000000,999],["NODATA","NODATA"]]))
    OutPolygon= arcpy.RasterToPolygon_conversion(ReclassRaster, R3FINALstr+"\\"+str(HA)+"_DEPTH_"+str(RP)+"_v"+str(Version)+"_pg_v"+str(Version),"NO_SIMPLIFY","VALUE")
arcpy.AddMessage("Converting DEPTH Rasters to Classified FeatureClasses- COMPLETE")


#...VELOCITY
#Set Variables
Velocity10D= GDBHoldingFolder+"\\"+str(HA)+"_10_D_v"+str(Version)+".gdb"+"\\"+str(HA)+"_VELOCITY_10_D_v"+str(Version)
Velocity200D= GDBHoldingFolder+"\\"+str(HA)+"_200_D_v"+str(Version)+".gdb"+"\\"+str(HA)+"_VELOCITY_200_D_v"+str(Version)
Velocity1000ND= GDBHoldingFolder+"\\"+str(HA)+"_1000_ND_v"+str(Version)+".gdb"+"\\"+str(HA)+"_VELOCITY_1000_ND_v"+str(Version)
Velocity200CCD= GDBHoldingFolder+"\\"+str(HA)+"_200_D_2080H_67_v"+str(Version)+".gdb"+"\\"+str(HA)+"_VELOCITY_200_D_2080H_67_v"+str(Version)

arcpy.AddMessage("Converting VELOCITY Rasters to Classified FeatureClasses")
VelocityList= [Velocity10D, Velocity200D, Velocity1000ND, Velocity200CCD]

for i in VelocityList:
    if VelocityList.index(i) == 0: 
        RP= "10_D"
    elif VelocityList.index(i) == 1:
        RP= "200_D"
    elif VelocityList.index(i) == 2:
        RP= "1000_ND"
    elif VelocityList.index(i) == 3:
        RP= "200_D_2080H_67"

    #The following used map algebra rather than raster calc (which is not really meant to be used outside of desktop)
    inRaster= Raster(i)*1000
    ReclassRaster= Reclassify(inRaster, "VALUE", RemapRange([[0,1000,1],[1000.000001,2000,2],[2000.000001,99999.99,3],[100000,1000000,999],["NODATA","NODATA"]]))
    OutPolygon= arcpy.RasterToPolygon_conversion(ReclassRaster, R3FINALstr+"\\"+str(HA)+"_VELOCITY_"+str(RP)+"_v"+str(Version)+"_pg_v"+str(Version),"NO_SIMPLIFY","VALUE")
    Expression= "\"gridcode\"=999"
    Velocity999= arcpy.Select_analysis(OutPolygon, VDPPstr+"\\"+str(HA)+"_VELOCITY_"+str(RP)+"_v"+str(Version)+"_pg_999"+"_v"+str(Version), Expression)
    
arcpy.AddMessage("Converting VELOCITY Rasters to Classified FeatureClasses- COMPLETE")   


#VELOCITY DIRECTION

arcpy.AddMessage("Converting VELOCITY DIRECTION Rasters to Classified FeatureClasses")
VelocityDirList= [Grid150HAClip10YrPT, Grid150HAClip200YrPT, Grid150HAClip1000YrPT, Grid150HAClip200CCYrPT]

for i in VelocityDirList:
    if VelocityDirList.index(i) == 0:
        RP= "10_D"
    elif VelocityDirList.index(i) == 1:
        RP= "200_D"
    elif VelocityDirList.index(i) == 2:
        RP= "1000_ND"
    elif VelocityDirList.index(i) == 3:
        RP= "200_D_2080H_67"


    PreWBF= GDBHoldingFolder+"\\"+str(HA)+"_"+str(RP)+"_v"+str(Version)+".gdb\\"+str(HA)+"_VELOCITY_DIRECTION_"+str(RP)+"_v"+str(Version)
    arcpy.AddSurfaceInformation_3d(i,PreWBF,"Z","BILINEAR")
    arcpy.AddField_management(i,"GRIDCODE", "SHORT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(i,"GRIDCODE", '!Z!', "PYTHON_9.3")
    arcpy.DeleteField_management(i, ["id", "XMIN", "XMAX", "YMIN", "YMAX", "ORIG_FID", "Z"])
    arcpy.AddField_management(i,"SOURCE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(i,"SOURCE", "RIVER")    
    arcpy.AddField_management(i,"PROB", "TEXT", "", "", "","", "NULLABLE")
    
    if VelocityDirList.index(i) == 0:
        arcpy.CalculateField_management(i,"PROB", '"""H"""', "PYTHON_9.3")     
    elif VelocityDirList.index(i) == 1:
        arcpy.CalculateField_management(i,"PROB", '"""M"""', "PYTHON_9.3")     
    elif VelocityDirList.index(i) == 2:
        arcpy.CalculateField_management(i,"PROB", '"""L"""', "PYTHON_9.3")
    elif VelocityDirList.index(i) == 3:
        arcpy.CalculateField_management(i,"PROB", '"""M_2080H_67"""', "PYTHON_9.3")
        
    arcpy.AddField_management(i,"BAND_DESC", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(i,"BAND_DESC", "\"Flow Orientation from North\"", "PYTHON_9.3")
    VelocityDirOutputFilePath= R3FINALstr+"\\"+HA+"_VELOCITY_DIRECTION_"+RP+"_v"+Version
    VelocityDirOutput= arcpy.CopyFeatures_management(i, VelocityDirOutputFilePath)
    VelocityDirFC= VDPPstr+"\\"+HA+"_150m_GRID_PTZ_"+RP+"_v"+Version
    arcpy.MakeFeatureLayer_management(VelocityDirOutput, VelocityDirFC)
    arcpy.MakeFeatureLayer_management(HA_Lochs, "HA_LochsFC")
    arcpy.SelectLayerByLocation_management(VelocityDirFC, "INTERSECT", "HA_LochsFC")
    arcpy.CalculateField_management(VelocityDirFC,"GRIDCODE", '-9999', "PYTHON_9.3")
    arcpy.CalculateField_management(VelocityDirFC,"BAND_DESC", "\"Data not Available\"", "PYTHON_9.3")
    arcpy.MakeFeatureLayer_management(VelocityDirFC, "Velocity999FC")
    arcpy.SelectLayerByLocation_management(VelocityDirFC, "INTERSECT", "Velocity999FC")
    arcpy.CalculateField_management(VelocityDirFC,"GRIDCODE", '-9999', "PYTHON_9.3")
    arcpy.CalculateField_management(VelocityDirFC,"BAND_DESC", "\"Data not Available\"", "PYTHON_9.3")
arcpy.AddMessage("Converting VELOCITY DIRECTION Rasters to Classified FeatureClasses- COMPLETE")


#04 COMBINED CLASSIFIED FEATURECLASSES
#Set Variables
arcpy.AddMessage("Combining Classified FeatureClasses")

VelocCombFC= "FRM_FH_VELOCITY_RIVER_"+HA+"_v"+Version
VelocDirCombFC= "FRM_FH_VELOCITY_DIRECTION_RIVER_"+HA+"_v"+Version
ExtentCombFC= "FRM_FH_EXTENT_RIVER_"+HA+"_v"+Version
DepthCombFC= "FRM_FH_DEPTH_RIVER_"+HA+"_v"+Version

arcpy.AddMessage("Adding attribute fields to Classified FeatureClasses")
CombiList= [VelocCombFC, VelocDirCombFC, ExtentCombFC, DepthCombFC]

for i in CombiList:
    arcpy.CreateFeatureclass_management(str(R4FINALstr), str(i), "POLYGON","#","#","#",str(Velocity10D))
    arcpy.AddField_management(str(R4FINALstr)+"\\"+str(i),"MAP_TYPE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.AddField_management(str(R4FINALstr)+"\\"+str(i),"SOURCE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.AddField_management(str(R4FINALstr)+"\\"+str(i),"METRIC", "TEXT", "", "", "","", "NULLABLE")
    arcpy.AddField_management(str(R4FINALstr)+"\\"+str(i),"PROB", "TEXT", "", "", "","", "NULLABLE")
    arcpy.AddField_management(str(R4FINALstr)+"\\"+str(i),"BAND_DESC", "TEXT", "", "", "","", "NULLABLE")
    arcpy.AddField_management(str(R4FINALstr)+"\\"+str(i),"GRIDCODE", "LONG", "", "", "","", "NULLABLE")
    arcpy.AddField_management(str(R4FINALstr)+"\\"+str(i),"REFERENCE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.AddField_management(str(R4FINALstr)+"\\"+str(i),"VERSION", "TEXT", "", "", "","", "NULLABLE")
    arcpy.AddField_management(str(R4FINALstr)+"\\"+str(i),"Issue_Date", "DATE", "", "", "","", "NULLABLE")

#Depths

Depth10D= R3FINALstr+"\\"+HA+"_DEPTH_10_D_v"+Version+"_pg_v"+Version
Depth200D= R3FINALstr+"\\"+HA+"_DEPTH_200_D_v"+Version+"_pg_v"+Version
Depth1000ND= R3FINALstr+"\\"+HA+"_DEPTH_1000_ND_v"+Version+"_pg_v"+Version
Depth200CCD= R3FINALstr+"\\"+HA+"_DEPTH_200_D_2080H_67_v"+Version+"_pg_v"+Version

arcpy.AddMessage("Combining DEPTH Classified FeatureClasses")
DepthReturnPeriods= [Depth10D, Depth200D, Depth1000ND, Depth200CCD]

expression = "def myBlock(!GRIDCODE!,!BAND_DESC!)"
codeblock = "def myBlock(x,y):\\n   if x ==1:\\n      y= \"< 0.3m\"\\n   elif x == 2:\\n      y=\"0.3m - 1.0m\"\\n   elif x==3:\\n      y=\">1.0m\"\\n   elif x==999:\\n      y=\"Data not Available\""

for i in DepthReturnPeriods:
    if DepthReturnPeriods.index(i) == 0:
        RP= "10_D"
    elif DepthReturnPeriods.index(i) == 1:
        RP= "200_D"
    elif DepthReturnPeriods.index(i) == 2:
        RP= "1000_ND"
    elif DepthReturnPeriods.index(i) == 3:
        RP= "200_D_2080H_67"
    FC= str(HA)+"_DEPTH_"+str(RP)+"_v"+str(Version)+"_pg_v"+str(Version)+"_H_v"+str(Version)
    arcpy.FeatureClassToFeatureClass_conversion(str(i), str(R4TEMPstr), str(FC))
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"MAP_TYPE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"MAP_TYPE", '"""HAZARD"""', "PYTHON_9.3")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"SOURCE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"SOURCE", '"""RIVER"""', "PYTHON_9.3")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"METRIC", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"METRIC", '"""DEPTH"""', "PYTHON_9.3")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"PROB", "TEXT", "", "", "","", "NULLABLE")
    if DepthReturnPeriods.index(i) == 0:
        PROB= '"""H"""'
    elif DepthReturnPeriods.index(i) == 1:
        PROB= '"""M"""'
    elif DepthReturnPeriods.index(i) == 2:
        PROB= '"""L"""'
    elif DepthReturnPeriods.index(i) == 3:
        PROB= '"""M_2080H_67"""'
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"PROB", PROB, "PYTHON_9.3")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"BAND_DESC", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"BAND_DESC", expression, "PYTHON_9.3", codeblock)
    arcpy.AlterField_management(str(R4TEMPstr)+"\\"+str(FC),"GRIDCODE", "OLD_GRIDCODE","","LONG","","NULLABLE")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"GRIDCODE", "LONG", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"GRIDCODE", '!OLD_GRIDCODE!', "PYTHON_9.3")
    arcpy.DeleteField_management(str(R4TEMPstr)+"\\"+str(FC), ["Id", "OLD_GRIDCODE"])
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"REFERENCE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"REFERENCE", "'"+HA+"'","PYTHON_9.3")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"VERSION_Path", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"VERSION_Path", "'"+Version+"'","PYTHON_9.3")

Depth10D= R4TEMPstr+"\\"+HA+"_DEPTH_10_D_v"+Version+"_pg_v"+Version+"_H_v"+Version+".shp"
Depth200D= R4TEMPstr+"\\"+HA+"_DEPTH_200_D_v"+Version+"_pg_v"+Version+"_H_v"+Version+".shp"
Depth1000D= R4TEMPstr+"\\"+HA+"_DEPTH_1000_ND_v"+Version+"_pg_v"+Version+"_H_v"+Version+".shp"
Depth200CCD= R4TEMPstr+"\\"+HA+"_DEPTH_200_D_2080H_67_v"+Version+"_pg_v"+Version+"_H_v"+Version+".shp"
DepthFinal= R4FINALstr+"\\"+DepthCombFC+".shp"

arcpy.Append_management([Depth10D, Depth200D, Depth1000D, Depth200CCD],DepthFinal,"NO_TEST")
arcpy.AddMessage("Combining DEPTH Classified FeatureClasses- COMPLETE")

#EXTENT

EXTENT10D= R3FINALstr+"\\"+HA+"_EXTENT_10_D_v"+Version+"_pg_v"+Version
EXTENT200D= R3FINALstr+"\\"+HA+"_EXTENT_200_D_v"+Version+"_pg_v"+Version
EXTENT1000ND= R3FINALstr+"\\"+HA+"_EXTENT_1000_ND_v"+Version+"_pg_v"+Version
EXTENT200CCD= R3FINALstr+"\\"+HA+"_EXTENT_200_D_2080H_67_v"+Version+"_pg_v"+Version

arcpy.AddMessage("Combining EXTENT Classified FeatureClasses")
arcpy.Copy_management(str(Year10Extent), str(EXTENT10D))
arcpy.Copy_management(str(Year200Extent), str(EXTENT200D))
arcpy.Copy_management(str(Year1000Extent), str(EXTENT1000ND))
arcpy.Copy_management(str(Year200CCExtent), str(EXTENT200CCD))

EXTENTReturnPeriods= [EXTENT10D, EXTENT200D, EXTENT1000ND, EXTENT200CCD]

for i in EXTENTReturnPeriods:
    if EXTENTReturnPeriods.index(i) == 0:
        RP= "10_D"
    elif EXTENTReturnPeriods.index(i) == 1:
        RP= "200_D"
    elif EXTENTReturnPeriods.index(i) == 2:
        RP= "1000_ND"
    elif EXTENTReturnPeriods.index(i) == 3:
        RP= "200_D_2080H_67"
    FC= str(HA)+"_EXTENT_"+str(RP)+"_v"+str(Version)+"_pg_v"+str(Version)+"_H_v"+str(Version)
    arcpy.FeatureClassToFeatureClass_conversion(str(i), str(R4TEMPstr), str(FC))
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"MAP_TYPE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"MAP_TYPE", '"""HAZARD"""', "PYTHON_9.3")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"SOURCE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"SOURCE", '"""RIVER"""', "PYTHON_9.3")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"METRIC", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"METRIC", '"""EXTENT"""', "PYTHON_9.3")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"PROB", "TEXT", "", "", "","", "NULLABLE")
    if EXTENTReturnPeriods.index(i) == 0:
        PROB= '"""H"""'
    elif EXTENTReturnPeriods.index(i) == 1:
        PROB= '"""M"""'
    elif EXTENTReturnPeriods.index(i) == 2:
        PROB= '"""L"""'
    elif EXTENTReturnPeriods.index(i) == 3:
        PROB= '"""M_2080H_67"""'
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"PROB", PROB, "PYTHON_9.3")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"BAND_DESC", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"BAND_DESC", '"""APPROPRIATE"""')
    arcpy.AlterField_management(str(R4TEMPstr)+"\\"+str(FC),"GRIDCODE", "OLD_GRIDCODE","","LONG","","NULLABLE")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"GRIDCODE", "LONG", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"GRIDCODE", '!OLD_GRIDCODE!', "PYTHON_9.3")
    arcpy.DeleteField_management(str(R4TEMPstr)+"\\"+str(FC), ["Id", "OLD_GRIDCODE"])
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"REFERENCE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"REFERENCE", "'"+HA+"'","PYTHON_9.3")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"VERSION_Path", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"VERSION_Path", "'"+Version+"'","PYTHON_9.3")

EXTENT10D= R4TEMPstr+"\\"+str(HA)+"_EXTENT_10_D_v"+str(Version)+"_pg_v"+str(Version)+"_H_v"+str(Version)+".shp"
EXTENT200D= R4TEMPstr+"\\"+str(HA)+"_EXTENT_200_D_v"+str(Version)+"_pg_v"+str(Version)+"_H_v"+str(Version)+".shp"
EXTENT1000ND= R4TEMPstr+"\\"+str(HA)+"_EXTENT_1000_ND_v"+str(Version)+"_pg_v"+str(Version)+"_H_v"+str(Version)+".shp"
EXTENT200CCD= R4TEMPstr+"\\"+str(HA)+"_EXTENT_200_D_2080H_67_v"+str(Version)+"_pg_v"+str(Version)+"_H_v"+str(Version)+".shp"
EXTENTFinal= R4FINALstr+"\\"+ExtentCombFC

arcpy.Append_management([EXTENT10D, EXTENT200D, EXTENT1000ND, EXTENT200CCD],EXTENTFinal,"NO_TEST")
arcpy.AddMessage("Combining EXTENT Classified FeatureClasses- COMPLETE")

#VELOCITY

VELOCITY10D= R3FINALstr+"\\"+str(HA)+"_VELOCITY_10_D_v"+Version+"_pg_v"+Version
VELOCITY200D= R3FINALstr+"\\"+str(HA)+"_VELOCITY_200_D_v"+Version+"_pg_v"+Version
VELOCITY1000ND= R3FINALstr+"\\"+str(HA)+"_VELOCITY_1000_ND_v"+Version+"_pg_v"+Version
VELOCITY200CCD= R3FINALstr+"\\"+str(HA)+"_VELOCITY_200_D_2080H_67_v"+Version+"_pg_v"+Version

arcpy.AddMessage("Combining VELOCITY Classified FeatureClasses")
VELOCITYReturnPeriods= [VELOCITY10D, VELOCITY200D, VELOCITY1000ND, VELOCITY200CCD]

expression = "def myBlock(!GRIDCODE!,!BAND_DESC!)"
codeblock = "def myBlock(x,y):\\n   if x ==1:\\n      y= \"< 1.0m/s\"\\n   elif x == 2:\\n      y=\"1.0m/s - 2.0m/s\"\\n   elif x == 3:\\n      y= \">2.0m/s\"\\n   elif x == 999:\\n      y= \"Data not Available\""

for i in VELOCITYReturnPeriods:
    if VELOCITYReturnPeriods.index(i) == 0:
        RP= "10_D"
    elif VELOCITYReturnPeriods.index(i) == 1:
        RP= "200_D"
    elif VELOCITYReturnPeriods.index(i) == 2:
        RP= "1000_ND"
    elif VELOCITYReturnPeriods.index(i) == 3:
        RP= "200_D_2080H_67"
    FC= HA+"_VELOCITY_"+RP+"_v"+Version+"_pg_v"+Version+"_H_v"+Version
    arcpy.FeatureClassToFeatureClass_conversion(str(i), str(R4TEMPstr), str(FC))
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"MAP_TYPE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"MAP_TYPE", '"""HAZARD"""', "PYTHON_9.3")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"SOURCE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"SOURCE", '"""RIVER"""', "PYTHON_9.3")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"METRIC", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"METRIC", '"""VELOCITY"""', "PYTHON_9.3")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"PROB", "TEXT", "", "", "","", "NULLABLE")
    if VELOCITYReturnPeriods.index(i) == 0:
        PROB= '"""H"""'
    elif VELOCITYReturnPeriods.index(i) == 1:
        PROB= '"""M"""'
    elif VELOCITYReturnPeriods.index(i) == 2:
        PROB= '"""L"""'
    elif VELOCITYReturnPeriods.index(i) == 3:
        PROB= '"""M_2080H_67"""'
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"PROB", PROB, "PYTHON_9.3")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"BAND_DESC", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"BAND_DESC", expression, "PYTHON_9.3", codeblock)
    arcpy.AlterField_management(str(R4TEMPstr)+"\\"+str(FC),"GRIDCODE", "OLD_GRIDCODE","","LONG","","NULLABLE")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"GRIDCODE", "LONG", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"GRIDCODE", '!OLD_GRIDCODE!', "PYTHON_9.3")
    arcpy.DeleteField_management(str(R4TEMPstr)+"\\"+str(FC), ["Id", "OLD_GRIDCODE"])
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"REFERENCE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"REFERENCE", "'"+HA+"'","PYTHON_9.3")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"VERSION_Path", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"VERSION_Path","'"+ Version+"'","PYTHON_9.3")

VELOCITY10D= R4TEMPstr+"\\"+HA+"_VELOCITY_10_D_v"+Version+"_pg_v"+Version+"_H_v"+Version+".shp"
VELOCITY200D= R4TEMPstr+"\\"+HA+"_VELOCITY_200_D_v"+Version+"_pg_v"+Version+"_H_v"+Version+".shp"
VELOCITY1000ND= R4TEMPstr+"\\"+HA+"_VELOCITY_1000_ND_v"+Version+"_pg_v"+Version+"_H_v"+Version+".shp"
VELOCITY200CCD= R4TEMPstr+"\\"+HA+"_VELOCITY_200_D_2080H_67_v"+Version+"_pg_v"+Version+"_H_v"+Version+".shp"
VELOCITYFinal= R4FINALstr+"\\"+VelocCombFC

arcpy.Append_management([VELOCITY10D, VELOCITY200D, VELOCITY1000ND, VELOCITY200CCD],VELOCITYFinal,"NO_TEST")
arcpy.AddMessage("Combining VELOCITY Classified FeatureClasses- COMPLETE")

#VELOCITY DIRECTION

VELOCITYDIR10D= R3FINALstr+"\\"+HA+"_VELOCITY_DIRECTION_10_D_v"+Version
VELOCITYDIR200D= R3FINALstr+"\\"+HA+"_VELOCITY_DIRECTION_200_D_v"+Version
VELOCITYDIR1000ND= R3FINALstr+"\\"+HA+"_VELOCITY_DIRECTION_1000_ND_v"+Version
VELOCITYDIR200CCD= R3FINALstr+"\\"+HA+"_VELOCITY_DIRECTION_200_D_2080H_67_v"+Version

arcpy.AddMessage("Combining VELOCITY DIRECTION Classified FeatureClasses")
VELOCITYDIRReturnPeriods= [VELOCITYDIR10D, VELOCITYDIR200D, VELOCITYDIR1000ND, VELOCITYDIR200CCD]

#expression = "def myBlock(!GRIDCODE!,!BAND_DESC!)"
#codeblock = "def myBlock(x,y):\\n   if x ==3:\\n      y= \"> 1.0m\"\\n   elif x == 999:\\n      y=\"Data not Available\""

for i in VELOCITYDIRReturnPeriods:
    if VELOCITYDIRReturnPeriods.index(i) == 0:
        RP= "10_D"
    elif VELOCITYDIRReturnPeriods.index(i) == 1:
        RP= "200_D"
    elif VELOCITYDIRReturnPeriods.index(i) == 2:
        RP= "1000_ND"
    elif VELOCITYDIRReturnPeriods.index(i) == 3:
        RP= "200_D_2080H_67"
    FC= HA+"_VELOCITY_DIRECTION_"+RP+"_v"+Version+"_pg_v"+Version+"_H_v"+Version
    arcpy.FeatureClassToFeatureClass_conversion(str(i), str(R4TEMPstr), str(FC))
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"MAP_TYPE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"MAP_TYPE", '"""HAZARD"""', "PYTHON_9.3")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"SOURCE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"SOURCE", '"""RIVER"""', "PYTHON_9.3")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"METRIC", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"METRIC", '"""VELOCITY-DIRECTION"""', "PYTHON_9.3")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"PROB", "TEXT", "", "", "","", "NULLABLE")
    if VELOCITYDIRReturnPeriods.index(i) == 0:
        PROB= '"""H"""'
    elif VELOCITYDIRReturnPeriods.index(i) == 1:
        PROB= '"""M"""'
    elif VELOCITYDIRReturnPeriods.index(i) == 2:
        PROB= '"""L"""'
    elif VELOCITYDIRReturnPeriods.index(i) == 3:
        PROB= '"""M_2080H_67"""'
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"PROB", PROB, "PYTHON_9.3")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"BAND_DESC", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"BAND_DESC","\"Flow Orientation from North\"", "PYTHON_9.3")
    arcpy.AlterField_management(str(R4TEMPstr)+"\\"+str(FC),"GRIDCODE", "OLD_GRIDCODE","LONG","","","NULLABLE")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"GRIDCODE", "LONG", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"GRIDCODE", '!OLD_GRIDCODE!', "PYTHON_9.3")
    arcpy.DeleteField_management(str(R4TEMPstr)+"\\"+str(FC), ["Id", "OLD_GRIDCODE"])
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"REFERENCE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"REFERENCE", "'"+HA+"'","PYTHON_9.3")
    arcpy.AddField_management(str(R4TEMPstr)+"\\"+str(FC),"VERSION_Path", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(str(R4TEMPstr)+"\\"+str(FC),"VERSION_Path", "'"+Version+"'","PYTHON_9.3")

VELOCITYDIR10D= R4TEMPstr+"\\"+HA+"_VELOCITY_DIRECTION_10_D_v"+Version+"_pg_v"+Version+"_H_v"+Version+".shp"
VELOCITYDIR200D= R4TEMPstr+"\\"+HA+"_VELOCITY_DIRECTION_200_D_v"+Version+"_pg_v"+Version+"_H_v"+Version+".shp"
VELOCITYDIR1000ND= R4TEMPstr+"\\"+HA+"_VELOCITY_DIRECTION_1000_ND_v"+Version+"_pg_v"+Version+"_H_v"+Version+".shp"
VELOCITYDIR200CCD= R4TEMPstr+"\\"+HA+"_VELOCITY_DIRECTION_200_D_2080H_67_v"+Version+"_pg_v"+Version+"_H_v"+Version+".shp"
VELOCITYDIRFinal= R4FINALstr+"\\"+VelocDirCombFC

arcpy.Append_management([VELOCITYDIR10D, VELOCITYDIR200D, VELOCITYDIR1000ND, VELOCITYDIR200CCD],VELOCITYDIRFinal,"TEST")
arcpy.AddMessage("Combining VELOCITY DIRECTION Classified FeatureClasses- COMPLETE")

arcpy.AddMessage("END OF PROCESS")
