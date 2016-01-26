# oasis-ade

This directory is created for the Global Health project in ADE at Olin College
and currently contains the work of Fall 2015 team.


##Final prototype
is the python file named **"blobTubeLocations_withMarker.py"**.

It takes in command line arguments: 
--image: the filepath to the image taken by rasPi camera
--mask : the filepath to the mask file we have created
--divisions: number of radial sections we'd like to divide the image into (12)

The final prototype folder also contains the file named **"greenMarkerDetect.py"**
however, it is already integrated into blobTubeLocations_withMarker.py

##Prototype 1 
contains python files:

**"blob.py"**: Initial blob detection code.
**"contours.py"**: Contouring the "red sections" based on hsv values. Ask Anne Wilkinson for more info.
**"blob_and_hsv.py"**: An attempt to run blob detection code on the image masked depending on hsv values.
**""**:I am not sure what the difference between this and contours.py is. Ask Anne Wilkinson for more info.

##RasPi: 
Has images taken using rasPi camera and 
**"test_video.py"**: code to stream video on rasPi (ask Celine for more info)

##CalibrationImages:
Images used for calibrating the rasPi camera

##resolutionTesting:
Images with various resolutions used to test if resolution matters a lot for blob detection to work properly.

##Thresholding-Bilateral:
Playing with images with thresholding etc.
