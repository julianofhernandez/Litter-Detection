## Abstract
Abstract—This study combines photo metadata and computer vision to quantify where uncollected litter is present. Images from the Trash Annotations in Context (TACO) dataset were used to teach an algorithm to detect 10 categories of garbage. Although it worked well with smartphone photos, it struggled when trying to process images from vehicle mounted cameras. However, increasing the variety of perspectives and backgrounds in the dataset will help it improve in unfamiliar situations. These data are plotted onto a map which, as accuracy improves, could be used for measuring waste management strategies and quantifying trends.

## The Problem
The world is increasingly relying on plastics for food packaging, electronics, single use containers, etc. In the 1960s they made up less than 1% of municipal solid waste, by 2005 this number rose to 10%. Post-consumer waste alone accounts for about 5% of total greenhouse gas emissions each year and costs over $200 billion each year. The world bank estimated the global waste production will continue to double roughly every decade, and won't plateu until the end of the century.
![plastic pollution](docs/images/plastic-pollution.png)

## Our Research
Based on recent advances in computer vision, an automated trash detection system could help answer these two questions: Where is waste located? How much is there? This is done by leveraging images from smartphones and dashcams to analyze specific geographic areas. With only a few dedicated vehicles, daily or weekly, snapshots could be taken to show how much litter there is over time. This information will be used to produce a human readable map that could be used by policy makers and non-profit organizations to evaluate and improve litter reduction programs.
![litter map](docs/images/litter-map.png)

## Algorithm: Mask R-CNN
This research uses Masked Regional Convolutional Neural network (Mask R-CNN), a computer vision algorithm that was made open source by Facebook in 2018. This performs both object detection (placing it into a category), and instance segmentation (creating an outline of where it is). Although training is a long process, detection only takes a few seconds, and can be run on a small mobile device with fast results 
![detections](docs/images/taco-sample-2.png)

## Datasets
### TACO
The Trash Annotations in Context (TACO) dataset contains publicly uploaded images of litter that have been outlined and labeled.
![detections](docs/images/taco-sample-1.png)

### Mapillary
Mapillary contains user submitted dashcam footage that has been scrubbed of personally identifiable information.

### CSUS Clean Up
Handheld images taken from a smartphone were collected on and around Sac State, these are similar to what a volunteer clean up group could collecting during the day to estimate category totals.