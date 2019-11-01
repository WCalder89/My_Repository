#This model takes the principles from the data derivation models which were
#previously hosted on Arc Toolbox(s)

#Import Modules

import os
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

HA_Lochs= "\\\\sepa-app-frm01\\frmdata\Working\\Flood Risk\\Hazard Maps\\Post Processing and Data Derivation\\Data Derivation\\Data Derivation Toolboxes\\FLUVIAL_Lochs.gdb\\"+HA

if len(HA)==6:
    arcpy.AddMessage("HA format OK")
    arcpy.AddMessage("Creating folders and file geodatabases")
else:
    arcpy.AddMessage("Please enter HA information in the format of \"HA_019\" and restart")
    sys.exit()

#CHECK IF FOLDERS/GDBs ALREADY EXIST- IF NOT THEM CREATE THEM



if os.path.exists(outputFolder+"\\"+HA)== True:
    MainFolder=(outputFolder,HA)
else:
    MainFolder= arcpy.CreateFolder_management(outputFolder,HA)
        
if os.path.exists(str(MainFolder)+"\\"+"Version_"+str(Version))== True:
    VersionFolder=(str(MainFolder)+"\\"+"Version_"+str(Version))
else:
    VersionFolder= arcpy.CreateFolder_management(MainFolder,"Version_"+str(Version))

if os.path.exists(str(VersionFolder)+"\\"+str(HA)+"_Data_Derivation_v"+str(Version)):
    DDFolder=(VersionFolder+"\\"+str(HA)+"_Data_Derivation_v"+str(Version))
else:
    DDFolder= arcpy.CreateFolder_management(VersionFolder,str(HA)+"_Data_Derivation_v"+str(Version))
        
if os.path.exists(str(DDFolder)+"\\"+ str(HA)+"_DD_R3_TEMP_v"+str(Version)+".gdb"):
    R3TEMP=(str(DDFolder)+"\\"+ str(HA)+"_DD_R3_TEMP_v"+str(Version)+".gdb")
else:
    R3TEMP= arcpy.CreateFileGDB_management(str(DDFolder), str(HA)+"_DD_R3_TEMP_v"+str(Version)+".gdb")     

if os.path.exists(str(DDFolder)+"\\"+ str(HA)+"_DD_R3_FINAL_v"+str(Version)+".gdb"):
    R3FINAL=(str(DDFolder)+"\\"+ str(HA)+"_DD_R3_FINAL_v"+str(Version)+".gdb")
else:
    R3FINAL= arcpy.CreateFileGDB_management(str(DDFolder), str(HA)+"_DD_R3_FINAL_v"+str(Version)+".gdb")

if os.path.exists(str(DDFolder)+"\\"+ str(HA)+"_DD_R4_TEMP_v"+str(Version)+".gdb"):
    R4TEMP=(str(DDFolder)+"\\"+ str(HA)+"_DD_R4_TEMP_v"+str(Version)+".gdb")
else:
    R4TEMP= arcpy.CreateFileGDB_management(str(DDFolder), str(HA)+"_DD_R4_TEMP_v"+str(Version)+".gdb")     

if os.path.exists(str(DDFolder)+"\\"+ str(HA)+"_DD_R4_FINAL_v"+str(Version)+".gdb"):
    R4FINAL=(str(DDFolder)+"\\"+ str(HA)+"_DD_R4_FINAL_v"+str(Version)+".gdb")
else:
    R4FINAL= arcpy.CreateFileGDB_management(str(DDFolder), str(HA)+"_DD_R4_FINAL_v"+str(Version)+".gdb")     

if os.path.exists(str(DDFolder)+"\\"+ str(HA)+"_VD_PP_Datasets_v"+str(Version)+".gdb"):
    VDPP=(str(DDFolder)+"\\"+ str(HA)+"_VD_PP_Datasets_v"+str(Version)+".gdb")
else:
    VDPP= arcpy.CreateFileGDB_management(str(DDFolder), str(HA)+"_VD_PP_Datasets_v"+str(Version)+".gdb")          
        
HABoundary= (HABoundarySource+HA+"_Coast_Clip")
HABoundaryCopy= (str(VDPP)+"\\"+str(HA)+"_Boundary_v"+str(Version))
Grid150Copy= arcpy.Copy_management(HABoundary,HABoundaryCopy,str(VDPP)+"\\"+str(HA)+"_150m_GRID_PG_v"+str(Version))
Grid150HAClip10Yr= arcpy.Clip_analysis(Grid150Copy, Year10Extent, str(VDPP)+"\\"+str(HA)+"_150m_GRID_PG_10_D_v"+str(Version))
Grid150HAClip200Yr= arcpy.Clip_analysis(Grid150Copy, Year200Extent, str(VDPP)+"\\"+str(HA)+"_150m_GRID_PG_200_D_v"+str(Version))
Grid150HAClip1000Yr= arcpy.Clip_analysis(Grid150Copy, Year1000Extent, str(VDPP)+"\\"+str(HA)+"_150m_GRID_PG_1000_D_v"+str(Version))
Grid150HAClip200CCYr= arcpy.Clip_analysis(Grid150Copy, Year200CCExtent, str(VDPP)+"\\"+str(HA)+"_150m_GRID_PG_200_D_2080H_v"+str(Version))
Grid150HAClip10YrPT= arcpy.FeatureToPoint_management(Grid150HAClip10Yr, str(VDPP)+"\\"+str(HA)+"_150m_GRID_PT_10_D_v"+str(Version), "INSIDE")
Grid150HAClip200YrPT= arcpy.FeatureToPoint_management(Grid150HAClip200Yr, str(VDPP)+"\\"+str(HA)+"_150m_GRID_PT_200_D_v"+str(Version), "INSIDE")
Grid150HAClip1000YrPT= arcpy.FeatureToPoint_management(Grid150HAClip1000Yr, str(VDPP)+"\\"+str(HA)+"_150m_GRID_PT_1000_D_v"+str(Version), "INSIDE")
Grid150HAClip200CCYrPT= arcpy.FeatureToPoint_management(Grid150HAClip200CCYr, str(VDPP)+"\\"+str(HA)+"_150m_GRID_PT_200_D_2080H_v"+str(Version), "INSIDE")
    

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
    exit

arcpy.env.workspace= arcpy.GetParameterAsText(0)

#03 Convert D-V-V-D Raster to Classified FeatureClasses
#Set variables
arcpy.AddMessage("Converting Rasters to Classified FeatureClasses")

#...DEPTHS
Depth10D= GDBHoldingFolder+"\\"+str(Version)+"\\"+str(HA)+"_Final_10_D_v"+str(Version)+".gdb"+"\\"+str(HA)+"_DEPTH_10_d_v"+str(Version)
Depth200D= GDBHoldingFolder+"\\"+str(Version)+"\\"+str(HA)+"_Final_200_D_v"+str(Version)+".gdb"+"\\"+str(HA)+"_DEPTH_200_d_v"+str(Version)
Depth1000ND= GDBHoldingFolder+"\\"+str(Version)+"\\"+str(HA)+"_Final_1000_ND_v"+str(Version)+".gdb"+"\\"+str(HA)+"_DEPTH_1000_nd_v"+str(Version)
Depth200CCD= GDBHoldingFolder+"\\"+str(Version)+"\\"+str(HA)+"_Final_200_D_2080H_67_v"+str(Version)+".gdb"+"\\"+str(HA)+"_DEPTH_200_D_2080H_67_v"+str(Version)

arcpy.AddMessage("Converting DEPTH Rasters to Classified FeatureClasses")
DepthList= [Depth10D, Depth200D, Depth1000ND, Depth200CCD]

for i in DepthList:
    if DepthList.index(i) == 0: 
        RP= "10_d"
    elif DepthList.index(i) == 1:
        RP= "200_d"
    elif DepthList.index(i) == 2:
        RP= "1000_nd"
    elif DepthList.index(i) == 3:
        RP= "200_D_2080H_67"

    RasterCalcOutput= str(R3TEMP)+"\\"+str(HA)+"_DEPTH_"+str(RP)+"_v"+str(Version)+"_T_v"+str(Version)
    arcpy.AddMessage(RasterCalcOutput)
    expression= (i*1000)
    inRaster= arcpy.gp.RasterCalculator_sa(expression, RasterCalcOutput)
    ReclassRaster= Reclassify(inRaster, "VALUE", RemapRange([[0,300,1],[300.000001,1000,2],[1000.000001,99999.99,3],[100000,1000000,999],["NODATA","NODATA"]]))
    OutPolygon= arcpy.RasterToPolygon_conversion(ReclassRaster, str(R3FINAL)+"\\"+str(HA)+"_DEPTH_"+str(RP)+"_v"+str(Version)+"_pg_v"+str(Version),"NO_SIMPLIFY","VALUE")

#...VELOCITY
#Set Variables
Velocity10D= GDBHoldingFolder+"\\"+Version+"\\"+HA+"_Final_10_D_v"+Version+".gdb"+"\\"+HA+"_VELOCITY_10_d_v"+Version
Velocity200D= GDBHoldingFolder+"\\"+Version+"\\"+HA+"_Final_200_D_v"+Version+".gdb"+"\\"+HA+"_VELOCITY_200_d_v"+Version
Velocity1000ND= GDBHoldingFolder+"\\"+Version+"\\"+HA+"_Final_1000_ND_v"+Version+".gdb"+"\\"+HA+"_VELOCITY_1000_nd_v"+Version
Velocity200CCD= GDBHoldingFolder+"\\"+Version+"\\"+HA+"_Final_200_D_2080H_67_v"+Version+".gdb"+"\\"+HA+"_VELOCITY_200_D_2080H_67_v"+Version

arcpy.AddMessage("Converting VELOCITY Rasters to Classified FeatureClasses")
VelocityList= [Velocity10D, Velocity200D, Velocity1000ND, Velocity200CCD]

for i in VelocityList:
    if index(i) == 0: 
        RP= "10_d"
    elif index(i) == 1:
        RP= "200_d"
    elif index(i) == 2:
        RP= "1000_nd"
    elif index(i) == 3:
        RP= "200_D_2080H_67"

    RasterCalcOutput= str(R3TEMP)+"\\"+str(HA)+"_VELOCITY_"+str(RP)+"_v"+str(Version)+"_T_v"+str(Version)
    expression= i*1000
    inRaster= arcpy.gp.RasterCalculator_sa(expression, RasterCalcOutput)
    ReclassRaster= Reclassify(inRaster, "VALUE", RemapRange([[0,1000,1],[1000.000001,2000,2],[2000.000001,99999.99,3],[100000,1000000,999],["NODATA","NODATA"]]))
    OutPolygon= arcpy.RasterToPolygon_conversion(ReclassRaster, str(R3FINAL)+"\\"+str(HA)+"_VELOCITY_"+str(RP)+"_v"+str(Version)+"_pg_v"+str(Version),"NO_SIMPLIFY","VALUE")
    expression= "GRIDECODE=999"
    Velocity999= arcpy.Select_analysis(OutPolygon, str(VDPP)+"\\"+str(HA)+"_VELOCITY_"+str(RP)+"_v"+str(Version)+"_pg_999"+str(Version), expression)
    

#VELOCITY DIRECTION

arcpy.AddMessage("Converting VELOCITY DIRECTION Rasters to Classified FeatureClasses")
VelocityDirList= [Grid150HAClip10YrPT, Grid150HAClip200YrPT, Grid150HAClip1000YrPT, Grid150HAClip200CCYrPT]

for i in VelocityDirList:
    if index(i) == 0:
        RP= "10_d"
    elif index(i) == 1:
        RP= "200_d"
    elif index(i) == 2:
        RP= "1000_nd"
    elif index(i) == 3:
        RP= "200_D_2080H_67"

    PreWBF= GDBHoldingFolder+"\\"+HA+"_"+RP+"_v"+Version+".gbd\\"+HA+"_VELOCITY_DIRECTION_"+RP+"_v"+Version+"_Pre_WBF"
    arcpy.AddSurfaceInformation_3d(i,PreWBF,"Z","BILINEAR")
    arcpy.AddField_management(i,"GRIDCODE", "SHORT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(i,"GRIDCODE", "!Z!", "PYTHON3")
    arcpy.DeleteField_management(i, ["id", "XMIN", "XMAX", "YMIN", "YMAX", "ORIG_FID", "Z"])
    arcpy.AddField_management(i,"SOURCE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(i,"SOURCE", "RIVER", "PYTHON3")    
    arcpy.AddField_management(i,"PROB", "TEXT", "", "", "","", "NULLABLE")
    
    if index(i) == 0:
        arcpy.CalculateField_management(i,"PROB", "H", "PYTHON3")     
    elif index(i) == 1:
        arcpy.CalculateField_management(i,"PROB", "M", "PYTHON3")     
    elif index(i) == 2:
        arcpy.CalculateField_management(i,"PROB", "L", "PYTHON3")
    elif index(i) == 3:
        arcpy.CalculateField_management(i,"PROB", "M_2080H_67", "PYTHON3")
        
    arcpy.AddField_management(i,"BAND_DESC", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(i,"BAND_DESC", "Flow Orientation from North", "PYTHON3")
    VelocityDirOutputFilePath= R3FINAL+"\\"+HA+"_VELOCITY_DIRECTION_1000_ND_v"+Version
    VelocityDirOutput= arcpy.CopyFeatures_management(i, VelocityDirOutputFilePath)
    VelocityDirFC= VDPP+"\\"+HA+"_150m_GRID_PTZ_"+RP+"_v"+Version
    arcpy.MakeFeatureLayer_management(VelocityDirOutput, VelocityDirFC)
    arcpy.SelectByLocation_management(VelocityDirFC, "INTERSECT", HA_Lochs)
    arcpy.CalculateField_management(VelocityDirFC,"GRIDCODE", "-9999", "PYTHON3")
    arcpy.CalculateField_management(VelocityDirFC,"BAND_DESC", "Data not Available", "PYTHON3")
    arcpy.SelectByLocation_management(VelocityDirFC, "INTERSECT", Velocity999)
    arcpy.CalculateField_management(VelocityDirFC,"GRIDCODE", "-9999", "PYTHON3")
    arcpy.CalculateField_management(VelocityDirFC,"BAND_DESC", "Data not Available", "PYTHON3")


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
    arcpy.CreateFeatureclass_management(R4FINAL, i, "POLYGON","","DISABLED", "DISABLED","BRITISH_NATIONAL_GRID")
    arcpy.AddField_management(i,"MAP_TYPE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.AddField_management(i,"SOURCE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.AddField_management(i,"METRIC", "TEXT", "", "", "","", "NULLABLE")
    arcpy.AddField_management(i,"PROB", "TEXT", "", "", "","", "NULLABLE")
    arcpy.AddField_management(i,"BAND_DESC", "TEXT", "", "", "","", "NULLABLE")
    arcpy.AddField_management(i,"GRIDCODE", "SHORT", "", "", "","", "NULLABLE")
    arcpy.AddField_management(i,"REFERENCE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.AddField_management(i,"VERSION", "TEXT", "", "", "","", "NULLABLE")
    arcpy.AddField_management(i,"Issue_Date", "DATE", "", "", "","", "NULLABLE")

#Depths

Depth10D= R3FINAL+"\\"+HA+"_DEPTH_10_d_v"+Version+"_pg_v"+Version
Depth200D= R3FINAL+"\\"+HA+"_DEPTH_200_d_v"+Version+"_pg_v"+Version
Depth1000D= R3FINAL+"\\"+HA+"_DEPTH_1000_nd_v"+Version+"_pg_v"+Version
Depth200CCD= R3FINAL+"\\"+HA+"_DEPTH_200_D_2080H_67_v"+Version+"_pg_v"+Version

arcpy.AddMessage("Combining DEPTH Classified FeatureClasses")
DepthReturnPeriods= [Depth10D, Depth200D, Depth1000D, Depth200CCD]

expression = "def myBlock(!GRIDCODE!,!BAND_DESC!)"
codeblock = """def myBlock(x,y):
    if x =3:
        y= "> 1.0m"
    elif x = 999:
        y="Data not Available"""

for i in DepthReturnPeriods:
    if index(i) == 0:
        RP= "10_d"
    elif index(i) == 1:
        RP= "200_d"
    elif index(i) == 2:
        RP= "1000_nd"
    elif index(i) == 3:
        RP= "200_D_2080H_67"
    FC= HA+"_DEPTH_"+RP+"_"+Version+"_pg_v"+Version+"_H_v"+Version
    arcpy.FeatureClassToFeatureClass_conversion(i, R4TEMP, FC)
    arcpy.AddField_management(FC,"MAP_TYPE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"MAP_TYPE", "HAZARD", "PYTHON3")
    arcpy.AddField_management(FC,"SOURCE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"SOURCE", "RIVER", "PYTHON3")
    arcpy.AddField_management(FC,"METRIC", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"METRIC", "DEPTH", "PYTHON3")
    arcpy.AddField_management(FC,"PROB", "TEXT", "", "", "","", "NULLABLE")
    if index(i) == 0:
        PROB= "H"
    elif index(i) == 1:
        PROB= "M"
    elif index(i) == 2:
        PROB= "L"
    elif index(i) == 3:
        PROB= "M_2080H_67"
    arcpy.CalculateField_management(FC,"PROB", PROB, "PYTHON3")
    arcpy.AddField_management(FC,"BAND_DESC", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"BAND_DESC", expression, codeblock)
    arcpy.AlterField_management(FC,"GRIDCODE", "OLD_GRIDCODE","","LONG","","NULLABLE")
    arcpy.AddField_management(FC,"GRIDCODE", "LONG", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"GRIDCODE", "!OLD_GRIDCODE!", codeblock)
    arcpy.DeleteField_management(FC, ["Id", "OLD_GRIDCODE"])
    arcpy.AddField_management(FC,"REFERENCE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"REFERENCE", HA,"PYTHON3")
    arcpy.AddField_management(FC,"VERSION_Path", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"VERSION_Path", Version,"PYTHON3")

Depth10D= R4TEMP+"\\"+HA+"_DEPTH_10_d_v"+Version+"_pg_v"+Version+"_H_v"+Version
Depth200D= R4TEMP+"\\"+HA+"_DEPTH_200_d_v"+Version+"_pg_v"+Version+"_H_v"+Version
Depth1000D= R4TEMP+"\\"+HA+"_DEPTH_1000_nd_v"+Version+"_pg_v"+Version+"_H_v"+Version
Depth200CCD= R4TEMP+"\\"+HA+"_DEPTH_200_D_2080H_67_v"+Version+"_pg_v"+Version+"_H_v"+Version
DepthFinal= R4TEMP+"\\"+DepthCombFC

arcpy.Append_management([Depth10D, Depth200D, Depth1000D, Depth200CCD],DepthFinal,"NO_TEST")


#EXTENT

EXTENT10D= R3FINAL+"\\"+HA+"_EXTENT_10_d_v"+Version+"_pg_v"+Version
EXTENT200D= R3FINAL+"\\"+HA+"_EXTENT_200_d_v"+Version+"_pg_v"+Version
EXTENT1000D= R3FINAL+"\\"+HA+"_EXTENT_1000_nd_v"+Version+"_pg_v"+Version
EXTENT200CCD= R3FINAL+"\\"+HA+"_EXTENT_200_D_2080H_67_v"+Version+"_pg_v"+Version

arcpy.AddMessage("Combining EXTENT Classified FeatureClasses")
EXTENTReturnPeriods= [EXTENT10D, EXTENT200D, EXTENT1000D, EXTENT200CCD]

expression = "def myBlock(!GRIDCODE!,!BAND_DESC!)"
codeblock = """def myBlock(x,y):
    if x =3:
        y= "> 1.0m"
    elif x = 999:
        y="Data not Available"""

for i in EXTENTReturnPeriods:
    if index(i) == 0:
        RP= "10_d"
    elif index(i) == 1:
        RP= "200_d"
    elif index(i) == 2:
        RP= "1000_nd"
    elif index(i) == 3:
        RP= "200_D_2080H_67"
    FC= HA+"_EXTENT_"+RP+"_"+Version+"_pg_v"+Version+"_H_v"+Version
    arcpy.FeatureClassToFeatureClass_conversion(i, R4TEMP, FC)
    arcpy.AddField_management(FC,"MAP_TYPE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"MAP_TYPE", "HAZARD", "PYTHON3")
    arcpy.AddField_management(FC,"SOURCE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"SOURCE", "RIVER", "PYTHON3")
    arcpy.AddField_management(FC,"METRIC", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"METRIC", "EXTENT", "PYTHON3")
    arcpy.AddField_management(FC,"PROB", "TEXT", "", "", "","", "NULLABLE")
    if index(i) == 0:
        PROB= "H"
    elif index(i) == 1:
        PROB= "M"
    elif index(i) == 2:
        PROB= "L"
    elif index(i) == 3:
        PROB= "M_2080H_67"
    arcpy.CalculateField_management(FC,"PROB", PROB, "PYTHON3")
    arcpy.AddField_management(FC,"BAND_DESC", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"BAND_DESC", "APPROPRIATE")
    arcpy.AlterField_management(FC,"GRIDCODE", "OLD_GRIDCODE","","LONG","","NULLABLE")
    arcpy.AddField_management(FC,"GRIDCODE", "LONG", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"GRIDCODE", "!OLD_GRIDCODE!", codeblock)
    arcpy.DeleteField_management(FC, ["Id", "OLD_GRIDCODE"])
    arcpy.AddField_management(FC,"REFERENCE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"REFERENCE", HA,"PYTHON3")
    arcpy.AddField_management(FC,"VERSION_Path", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"VERSION_Path", Version,"PYTHON3")

EXTENT10D= R4TEMP+"\\"+HA+"_EXTENT_10_d_v"+Version+"_pg_v"+Version+"_H_v"+Version
EXTENT200D= R4TEMP+"\\"+HA+"_EXTENT_200_d_v"+Version+"_pg_v"+Version+"_H_v"+Version
EXTENT1000ND= R4TEMP+"\\"+HA+"_EXTENT_1000_nd_v"+Version+"_pg_v"+Version+"_H_v"+Version
EXTENT200CCD= R4TEMP+"\\"+HA+"_EXTENT_200_D_2080H_67_v"+Version+"_pg_v"+Version+"_H_v"+Version
EXTENTFinal= R4TEMP+"\\"+ExtentCombFC

arcpy.Append_management([EXTENT10D, EXTENT200D, EXTENT1000ND, EXTENT200CCD],EXTENTFinal,"NO_TEST")


#VELOCITY

VELOCITY10D= R3FINAL+"\\"+HA+"_VELOCITY_10_d_v"+Version+"_pg_v"+Version
VELOCITY200D= R3FINAL+"\\"+HA+"_VELOCITY_200_d_v"+Version+"_pg_v"+Version
VELOCITY1000D= R3FINAL+"\\"+HA+"_VELOCITY_1000_nd_v"+Version+"_pg_v"+Version
VELOCITY200CCD= R3FINAL+"\\"+HA+"_VELOCITY_200_D_2080H_67_v"+Version+"_pg_v"+Version

arcpy.AddMessage("Combining VELOCITY Classified FeatureClasses")
VELOCITYReturnPeriods= [VELOCITY10D, VELOCITY200D, VELOCITY1000ND, VELOCITY200CCD]

expression = "def myBlock(!GRIDCODE!,!BAND_DESC!)"
codeblock = """def myBlock(x,y):
    if x =3:
        y= "> 1.0m"
    elif x = 999:
        y="Data not Available"""

for i in VELOCITYReturnPeriods:
    if index(i) == 0:
        RP= "10_d"
    elif index(i) == 1:
        RP= "200_d"
    elif index(i) == 2:
        RP= "1000_nd"
    elif index(i) == 3:
        RP= "200_D_2080H_67"
    FC= HA+"_VELOCITY_"+RP+"_"+Version+"_pg_v"+Version+"_H_v"+Version
    arcpy.FeatureClassToFeatureClass_conversion(i, R4TEMP, FC)
    arcpy.AddField_management(FC,"MAP_TYPE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"MAP_TYPE", "HAZARD", "PYTHON3")
    arcpy.AddField_management(FC,"SOURCE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"SOURCE", "RIVER", "PYTHON3")
    arcpy.AddField_management(FC,"METRIC", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"METRIC", "VELOCITY", "PYTHON3")
    arcpy.AddField_management(FC,"PROB", "TEXT", "", "", "","", "NULLABLE")
    if index(i) == 0:
        PROB= "H"
    elif index(i) == 1:
        PROB= "M"
    elif index(i) == 2:
        PROB= "L"
    elif index(i) == 3:
        PROB= "M_2080H_67"
    arcpy.CalculateField_management(FC,"PROB", PROB, "PYTHON3")
    arcpy.AddField_management(FC,"BAND_DESC", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"BAND_DESC", "APPROPRIATE")
    arcpy.AlterField_management(FC,"GRIDCODE", "OLD_GRIDCODE","","LONG","","NULLABLE")
    arcpy.AddField_management(FC,"GRIDCODE", "LONG", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"GRIDCODE", "!OLD_GRIDCODE!", codeblock)
    arcpy.DeleteField_management(FC, ["Id", "OLD_GRIDCODE"])
    arcpy.AddField_management(FC,"REFERENCE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"REFERENCE", HA,"PYTHON3")
    arcpy.AddField_management(FC,"VERSION_Path", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"VERSION_Path", Version,"PYTHON3")

VELOCITY10D= R4TEMP+"\\"+HA+"_VELOCITY_10_d_v"+Version+"_pg_v"+Version+"_H_v"+Version
VELOCITY200D= R4TEMP+"\\"+HA+"_VELOCITY_200_d_v"+Version+"_pg_v"+Version+"_H_v"+Version
VELOCITY1000ND= R4TEMP+"\\"+HA+"_VELOCITY_1000_nd_v"+Version+"_pg_v"+Version+"_H_v"+Version
VELOCITY200CCD= R4TEMP+"\\"+HA+"_VELOCITY_200_D_2080H_67_v"+Version+"_pg_v"+Version+"_H_v"+Version
VELOCITYFinal= R4TEMP+"\\"+VelocCombFC

arcpy.Append_management([VELOCITY10D, VELOCITY200D, VELOCITY1000ND, VELOCITY200CCD],VELOCITYFinal,"NO_TEST")


#VELOCITY DIRECTION

VELOCITYDIR10D= R3FINAL+"\\"+HA+"_VELOCITY_DIRECTION_10_d_v"+Version+"_pg_v"+Version
VELOCITYDIR200D= R3FINAL+"\\"+HA+"_VELOCITY_DIRECTION_200_d_v"+Version+"_pg_v"+Version
VELOCITYDIR1000D= R3FINAL+"\\"+HA+"_VELOCITY_DIRECTION_1000_nd_v"+Version+"_pg_v"+Version
VELOCITYDIR200CCD= R3FINAL+"\\"+HA+"_VELOCITY_DIRECTION_200_D_2080H_67_v"+Version+"_pg_v"+Version

arcpy.AddMessage("Combining VELOCITY DIRECTION Classified FeatureClasses")
VELOCITYDIRReturnPeriods= [VELOCITYDIR10D, VELOCITYDIR200D, VELOCITYDIR1000ND, VELOCITYDIR200CCD]

expression = "def myBlock(!GRIDCODE!,!BAND_DESC!)"
codeblock = """def myBlock(x,y):
    if x =3:
        y= "> 1.0m"
    elif x = 999:
        y="Data not Available"""

for i in VELOCITYDIRReturnPeriods:
    if index(i) == 0:
        RP= "10_d"
    elif index(i) == 1:
        RP= "200_d"
    elif index(i) == 2:
        RP= "1000_nd"
    elif index(i) == 3:
        RP= "200_D_2080H_67"
    FC= HA+"_VELOCITY_DIRECTION_"+RP+"_"+Version+"_pg_v"+Version+"_H_v"+Version
    arcpy.FeatureClassToFeatureClass_conversion(i, R4TEMP, FC)
    arcpy.AddField_management(FC,"MAP_TYPE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"MAP_TYPE", "HAZARD", "PYTHON3")
    arcpy.AddField_management(FC,"SOURCE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"SOURCE", "RIVER", "PYTHON3")
    arcpy.AddField_management(FC,"METRIC", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"METRIC", "VELOCITY-DIRECTION", "PYTHON3")
    arcpy.AddField_management(FC,"PROB", "TEXT", "", "", "","", "NULLABLE")
    if index(i) == 0:
        PROB= "H"
    elif index(i) == 1:
        PROB= "M"
    elif index(i) == 2:
        PROB= "L"
    elif index(i) == 3:
        PROB= "M_2080H_67"
    arcpy.CalculateField_management(FC,"PROB", PROB, "PYTHON3")
    arcpy.AddField_management(FC,"BAND_DESC", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"BAND_DESC", "APPROPRIATE")
    arcpy.AlterField_management(FC,"GRIDCODE", "OLD_GRIDCODE","","LONG","","NULLABLE")
    arcpy.AddField_management(FC,"GRIDCODE", "LONG", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"GRIDCODE", "!OLD_GRIDCODE!", codeblock)
    arcpy.DeleteField_management(FC, ["Id", "OLD_GRIDCODE"])
    arcpy.AddField_management(FC,"REFERENCE", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"REFERENCE", HA,"PYTHON3")
    arcpy.AddField_management(FC,"VERSION_Path", "TEXT", "", "", "","", "NULLABLE")
    arcpy.CalculateField_management(FC,"VERSION_Path", Version,"PYTHON3")

VELOCITYDIR10D= R4TEMP+"\\"+HA+"_VELOCITY_DIRECTION_10_d_v"+Version+"_pg_v"+Version+"_H_v"+Version
VELOCITYDIR200D= R4TEMP+"\\"+HA+"_VELOCITY_DIRECTION_200_d_v"+Version+"_pg_v"+Version+"_H_v"+Version
VELOCITYDIR1000ND= R4TEMP+"\\"+HA+"_VELOCITY_DIRECTION_1000_nd_v"+Version+"_pg_v"+Version+"_H_v"+Version
VELOCITYDIR200CCD= R4TEMP+"\\"+HA+"_VELOCITY_DIRECTION_200_D_2080H_67_v"+Version+"_pg_v"+Version+"_H_v"+Version
VELOCITYDIRFinal= R4TEMP+"\\"+VelocDirCombFC

arcpy.Append_management([VELOCITYDIR10D, VELOCITYDIR200D, VELOCITYDIR1000ND, VELOCITYDIR200CCD],VELOCITYDIRFinal,"NO_TEST")


arcpy.AddMessage("END OF PROCESS")
