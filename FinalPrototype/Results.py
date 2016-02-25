####### ADE Global Health 2016 ####
import argparse
import importlib

class Results(object):
	# """
 #    >>> a=Results(bloodBlobDetection "prototype1NumMask.png maskSquare.png 12")
 #    >>> a.handleResults()
 #    {1: ['negative', 1], 2: ['positive', 5], 3: ['negative', 1], 4: ['negative', 1], 5: ['negative', 1], 6: ['positive', 5], 7: ['negative', 1], 8: ['positive', 5], 9: ['negative', 1], 10: ['negative', 1], 11: ['positive', 5], 12: ['negative', 1]}
	# """
	def __init__(self, imagingClass, classInputs):

		self.imagingClass=imagingClass(classInputs)

	def handleResults(self):
		"""
		Runs the "main" function of the imaging class and prints out the results in a dictionary
		in the form {1: [positive, 5], 2:[negative,1]}

		"""
		self.imagingClass.main()
		self.results = self.imagingClass.results
		return self.results
	
if __name__ == '__main__':
	import doctest
	doctest.testmod()

	ap=argparse.ArgumentParser()
	ap.add_argument("-f", "--filename", help="the path to the file where the imaging class is located")
	ap.add_argument("-c", "--class", help="name of the imaging class")
	ap.add_argument("-i", "--classInputs", help = "inputs that the imaging class takes in, needs to be given in the form of a list")

	# ## what these arguments are:
	args = vars(ap.parse_args())
	filename = args["filename"]
	imagingClass = args["class"]
	classInputs = args["classInputs"]

	# my_module = importlib.import_module("{}.{}.{}".format(args["filename"], args["class"], "main()"))
	# find_module(imagingClass) 
	# loader = importlib.find_loader(imagingClass, ["home/pinar/Desktop/ADE/oasis-ade/FinalPrototype/blobTubeLocations_withMarker.py"])
	# import loader
	from blobTubeLocations_withMarker import bloodBlobDetection
	r=Results(bloodBlobDetection, classInputs.split() )
	print r.handleResults()

	


	# _a = __import__(filename, globals(), locals(), [str(imagingClass)], -1)
	# b= _a.imagingClass
	# imagingObject = __import__(filename, globals(), locals(), [imagingClass], -1).object


