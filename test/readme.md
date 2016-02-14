
##Test Suite Introduction

###Goals
The purpose of the test suite is to quantify the accuracy of different methods of sickle cell detection. This is primarily so that we can assess how different methods work when compared to each other, but to also get some idea of how the accuracy of our test compares to the accuracy of human readers. 

###Technical Introduction
The test suite consists of a series of image files that have results already expected for them. The suite runs the detection code for all of the images and will log information about which images had issues. This can be found in testRunner.py 
Each individual test will create an instance of the ResultsObject class (described below) that is compared to a static JSON string of expected results

####ResultsObject
This class is a wrapper for a dictionary where each key is the number of the section on the rotor. The value for each key is a tuple where the first entry is a Boolean indicating if the test is positive or negative and the second entry is the 1-5 score that this sample would be read by a human as.

###Running tests
To run the tests simply type 
```python testRunner.py```
You will see output that indicates what percentage of results were successful and the logfile 
```test-methodName-MM/DD/YYYY-HH:MM:SS.log``` 
will contain more detailed results, including which images led to incorrect results. methodName will be the name of the openCV method we used to generate that testFile

###Adding tests
To add a new test image to the suite, you should follow this guide:

 1. Find the JSON file called tests.json
 - This file contains an array of JSON objects that have a path attribute and a results attribute. 
- The path attribute is the location of the image file
- The results attribute is the expected ResultsObject in JSON form
 2. Add the image path and expected ResultsObject for that image to the array.
	 - Example:  
	 ```json
	 {
	 "path" : "image/lives/here",
	 "results": {
		 1: "(True, 5)"
		 2: "(False, 1)"
		 3: "(False, 1)"
		 4: "(True, 5)"
		 }
	 }

	 ```