#make sure to change filepath for creating a new gdb, setting a workplace, importing both the hospital and populated places datasets, and exporting the csv

import arcpy as ap
import pandas as pd
#set arcpy to 'ap' and pandas as 'pd' to save typing as you write code

#allow to overwrite data
ap.env.overwriteOutput = True
print("\n\nStarting Program...")

#Create new geodatabase
ap.management.CreateFileGDB(r"E:\School\Geog428\Assign3", "ScratchAssign3.gdb")
print("Created new file geodatabase...")

#set workspace
gdb = r"E:\School\Geog428\Assign3\ScratchAssign3.gdb"
ap.env.workspace = gdb
print("Workspace GDB set...")

#Task 2: Import datasets into a newly created geodatabase.
#Copy shapefiles to feature classes in gdb 
#Set local variables for Hospitals
inFeaturesHospital = r"E:\School\Geog428\Assign3\Data\Hospitals\HOSPITALS_point.shp"
outLocationHospital = gdb
outFeatureClassNameHospital = 'hospitals'

#FeatureClass To FeatureClass Hospitals
ap.FeatureClassToFeatureClass_conversion(inFeaturesHospital, outLocationHospital, outFeatureClassNameHospital)
print("Copied Hospital Feature Class...")

#Set local variables for Hospitals
inFeaturesPop = r"E:\School\Geog428\Assign3\Data\Populations\POP_PL_1M_point.shp"
outLocationPop = gdb
outFeatureClassNamePop = 'popPlaces'

#FeatureClass To FeatureClass Hospitals
ap.FeatureClassToFeatureClass_conversion(inFeaturesPop, outLocationPop, outFeatureClassNamePop)
print("Copied Cities Feature Class...")
print("Import Data and Copy Feature Classes Complete...")

#Task 3: Assign datasets and fields as variables
#assign variables
hospitals = 'hospitals'
popPlaces = 'popPlaces'
print("Variables for Hospitals and Population Places set...")

#look up column field headings in population places
print("Looking up field column names...")
'''
fieldList = ap.ListFields(popPlaces)
for field in fieldList:
    print(field.name)
'''
#assign variables to popPlaces fields
cityNameCol = "NAME"
estPopCol = "EST_POP"
print("Assigned variables to city names and estimated populations...")
print(cityNameCol)
print(estPopCol)

#find name of city assigned
print("\nFinding city name assigned...")
whereExpr = cityNameCol + " LIKE 'Honey%'"
with ap.da.SearchCursor(popPlaces, (cityNameCol), whereExpr) as cursor:
    for i in cursor:
        print(i)

#assign city name
city = 'Honeymoon Bay'
print("Variable for " + city + " assigned.")

#
#
#
#Task 4
#create variables to fill in search cursor for loop
print("\nStarting Task 4...")
average = 0
totalPop = 0
recordsCounted= 0

#search cursor to calculate average pop. of all populated places
with ap.da.SearchCursor(popPlaces, (estPopCol)) as cursor:
    for i in cursor:
        totalPop += i[0]
        recordsCounted += 1
average = totalPop / recordsCounted
print("\nThe average population for all cities is ", str(round(average)), " people.")
print("Task 4 Complete!")

#
#
#
#Task 5: Determine the population size of your assigned city, and the distance of this city to the nearest hospital
#assign closest hospital to each city
print("\nStarting Task 5...")

nearHospital = ap.Near_analysis('popPlaces', 'hospitals')

#look up column name for nearest hospital to each city
print("Looking up field column names...")
'''
fieldList = ap.ListFields(popPlaces)
for field in fieldList:
    print(field.name)
'''
#assign variable to near field
nearDist = "NEAR_DIST"
print("Assigned variable to 'Near' distance field...")
print(nearDist)

#find population and distance to nearest hospital from assigned city
print("Finding city name assigned...")
whereExpr = "(" + cityNameCol + " = '" + city + "')"
print("SQL expression = " + whereExpr + "\n")

with ap.da.SearchCursor(popPlaces, (cityNameCol, estPopCol, nearDist), whereExpr) as cursor:
    for i in cursor:
        nearDistanceKm = i[2] / 1000
        print(str(i[0]) + " has a population of  " + str(round(i[1])) + " and is " + str(round(nearDistanceKm, 2)) + "km from the nearest hospital.\n")

    #Calculate 10% above and 10% below assigned city pop.
        print("Calculate 10% above and 10% below assigned city pop...")
    maxPop = i[1] + (i[1]  * 0.1)
    minPop = i[1] - (i[1]  * 0.1)
    print("10% above " + str(i[0]) + "'s population: " + str(round(maxPop)))
    print("10% below " + str(i[0]) + "'s population: " + str(round(minPop)))
print("Task 5 Complete!")
#
#
#
#Task 6: Calculate the average distance to hospitals for cities +/- 10% of your assigned city
print("\nStarting Task 6...")
averageDist = 0
totalDist = 0
recordsCounted = 0


print("\nFinding cities +/- 10% of assigned city...")
whereExpr = "(" + estPopCol + " >= %s" %minPop + ") And (" + estPopCol + " <= %s" %maxPop + ")"
print("SQL expression = " + whereExpr)
with ap.da.SearchCursor(popPlaces, (cityNameCol, estPopCol, nearDist), whereExpr) as cursor:
    print("\nSimilar cities (+/- 10%) of " + city + "'s population...")
    for i in cursor:
        similarCityNames = i[0]
        print(similarCityNames)
        
        totalDist += i[2]
        recordsCounted += 1
        averageDist = (totalDist / recordsCounted) / 1000
    print("\nThere were " + str(recordsCounted) + " cities that were +/- 10% population of " + city + ".")
    print("The average distance to the nearest hospital for cities +/- 10% population of " + city + " is " + str(round(averageDist, 2)) + "km.")
print("Task 6 Complete!\n")

#
#
#
#Task 7: Provide a qualitative classification of distance to hospitals for different size cities
print("Starting Task 7...")

#create new fields for city size and distance to hospital
ap.AddField_management(popPlaces, "Dist_Hos", "TEXT")
ap.AddField_management(popPlaces, "CitySize", "TEXT")
qualDistHospital = "Dist_Hos"
qualCitySize = "CitySize"
print("\nFields created...")

#show fields to make sure that they were created correctly
'''
fieldList = ap.ListFields(popPlaces)
for field in fieldList:
    print(field.name)
'''
#create array for the fields
citySizeClass = ["Small", "Medium", "Large"]
distHospitalClass = ["Very Close", "Close", "Far"]
print("arrays created...")

#assign counters
counterCity = 0
counterHos = 0

#update city size field with qualitative classes
print("Updating qualitative city classes...\n\nList first 5 rows:")
with ap.da.UpdateCursor(popPlaces, (estPopCol, qualCitySize)) as cursor:
    for i in cursor:
        counterCity += 1        
        if i[0] <= 500:
            i[1] = citySizeClass[0]
        elif i[0] > 500 and i[0] <= 10000:
            i[1] = citySizeClass[1]
        else:
            i[1] = citySizeClass[2]

        if counterCity <= 5:
            print(i[1])
        cursor.updateRow(i)
    print("\nQualitative city sizes assigned...")

#update distance to hospital field with qualitative classes
print("Updating qualitative distance to hospital classes...\n\nList first 5 rows:")
with ap.da.UpdateCursor(popPlaces, (nearDist, qualDistHospital)) as cursor:   
    for j in cursor:
        counterHos += 1
        if j[0] <= 1000:
            j[1] = distHospitalClass[0]
        elif j[0] > 1000 and j[0] <= 10000:
            j[1] = distHospitalClass[1]
        else:
            j[1] = distHospitalClass[2]

        if counterHos <= 5:
            print(j[1])
        cursor.updateRow(j)
    print("\nQualitative distance to hospitals assigned...")

#export population place to csv
inTable = popPlaces
outLocation = r"E:\School\Geog428\Assign3\Data"
outTable = "popPlaces_Qualitative_Results.csv"

ap.conversion.TableToTable(inTable, outLocation, outTable)

print("CSV file created...")
print("Task 7 Complete!")
#use R code to create graphs based on csv file
