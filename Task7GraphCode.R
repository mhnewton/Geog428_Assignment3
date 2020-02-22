install.packages("ggplot2")
library("ggplot2")

#Set working directory
dir <- "/Users/mikenewton/Desktop/Geog428/Assign3/Data"
setwd(dir)

#Reading in dataset
popPlaces <- read.csv("popPlaces_Qualitative_Results.csv")
colnames(popPlaces)
head(popPlaces)

#subset columns
popPlaces <- popPlaces[,c(6,13,18,19,20)]
#Change the column names 
colnames(popPlaces) <- c("Population", "Name", "NearHospital", "Distance", "Size")

#convert hospital distance and population values to log
popPlaces$NearHospital <- log(popPlaces$NearHospital)
popPlaces$Population <- log(popPlaces$Population)
head(popPlaces)

#scatterplot
png("./Scatterplot.png", width = 8, height = 6, units = "in", res = 300) #create a png file
ggplot(popPlaces, aes(x=Population, y=NearHospital, color=Distance, shape=Size)) + #classify x and y, qualitative classes
  geom_point(size = 3) + #set point size
  scale_shape_manual(values=c(16,15,17)) + 
  scale_color_manual(values=c('#E6E600','#A80000', '#267300')) +
  labs(title = "City population vs. distance to nearest hospital in British Columbia", x = "City Population (log)", y = "Distance to Closest Hospital (log(m))", 
       caption = "Figure 1: Scatterplot of cities in British Columbia and the distance to the nearest hospital. City populations were classified as\nsmall (≤500),medium (>500 and ≤10,000), and large (>10,000). Distances to the nearest hospital were classified as very close\n(≤1km), close (>1 and ≤10km), and far (>10km).") + #label plot, x axis, y axis
  theme_classic() + #set the theme to classic (removes background and borders etc.)
  theme(plot.title = element_text(face = "bold", hjust = 0.5), plot.caption = element_text(hjust = 0)) #set title to center and bold
dev.off()

#bargraph
png("./BarGraph.png", width = 8, height = 6, units = "in", res = 300) #create a png file
ggplot(popPlaces, aes(x=Size, fill=Distance)) + #classify x and y, qualitative classes
  geom_bar(position = "dodge") +
  scale_fill_manual(values=c('#E6E600','#A80000', '#267300')) +
  labs(title = "City size and distance to nearest hospital in British Columbia", x = "City Size", y = "Frequency", 
       caption = "Figure 2: Bargraph of cities in British Columbia and the distance to the nearest hospital. City populations were classified as\nsmall (≤500),medium (>500 and ≤10,000), and large (>10,000). Distances to the nearest hospital were classified as very close\n(≤1km), close (>1 and ≤10km), and far (>10km).") + #label plot, x axis, y axis
  theme_bw() + #set the theme to classic (removes background and borders etc.)
  theme(plot.title = element_text(face = "bold", hjust = 0.5), plot.caption = element_text(hjust = 0)) #set title to center and bold
dev.off()
