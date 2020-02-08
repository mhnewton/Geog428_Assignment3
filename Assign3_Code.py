import arcpy as ap
#set arcpy to 'ap' to save typing as you write code

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
print("\nImport Data and Copy Feature Classes Complete...")

#Task 3: Assign datasets and fields as variables
#assign variables
hospitals = 'hospitals'
popPlaces = 'popPlaces'
print("Variables for Hospitals and Population Places set...")

#look up column field headings in population places
print("\nLooking up field column names...")
'''
fieldList = ap.ListFields(popPlaces)
for field in fieldList:
    print(field.name)
'''
#assign variables to popPlaces fields
cityNameCol = "NAME"
estPopCol = "EST_POP"
print("\nAssigned variables to city names and estimated populations...")
print(cityNameCol)
print(estPopCol)

#find name of city assigned
print("\nFinding city name assigned...\n")
whereExpr = cityNameCol + " LIKE 'Honey%'"
with ap.da.SearchCursor(popPlaces, (cityNameCol), whereExpr) as cursor:
    for i in cursor:
        print(i)

#assign city name
city = 'Honeymoon Bay'
print("\nVariable for " + city + " assigned...")

#
#
#
#Task 4
#create variables to fill in search cursor for loop
average = 0
totalPop = 0
recordsCounted= 0

#search cursor to calculate average pop. of all populated places
with ap.da.SearchCursor(popPlaces, (estPopCol)) as cursor:
    for i in cursor:
        totalPop += i[0]
        recordsCounted += 1
average = totalPop / recordsCounted
print("\n\nThe average population for all cities is ", str(round(average)), " people.\n")

#
#
#
#Task 5: Determine the population size of your assigned city, and the distance of this city to the nearest hospital
#assign closest hospital to each city
nearHospital = ap.Near_analysis('popPlaces', 'hospitals')

#look up column name for nearest hospital to each city
print("\nLooking up field column names...")
'''
fieldList = ap.ListFields(popPlaces)
for field in fieldList:
    print(field.name)
'''
#assign variable to near field
nearDist = "NEAR_DIST"
print("\nAssigned variable to 'Near' distance field...")
print(nearDist)

#find population and distance to nearest hospital from assigned city
print("\nFinding city name assigned...\n")
whereExpr = "(" + cityNameCol + " = '" + city + "')"
print("SQL expression = " + whereExpr)

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

#
#
#
#Task 6:Calculate the average distance to hospitals for cities +/- 10% of your assigned city
averageDist = 0
totalDist = 0
recordsCounted = 0

print("\nFinding cities +/- 10% of assigned city...")
whereExpr = "(" + estPopCol + " >= %s" %minPop + ") And (" + estPopCol + " <= %s" %maxPop + ")"
print("SQL expression = " + whereExpr)
with ap.da.SearchCursor(popPlaces, (cityNameCol, estPopCol, nearDist), whereExpr) as cursor:
    for i in cursor:
        similarCities = i[0]
        similarCityPop = i[1]
        totalDist += i[2]
        recordsCounted += 1
        averageDist = (totalDist / recordsCounted) / 1000

    print("\nThere were " + str(recordsCounted) + " cities that were +/- 10% population of " + city + ".")
    print("\nThe average distance to the nearest hospital for cities +/- 10% population of " + city + " is " + str(round(averageDist, 2)) + "km.")









