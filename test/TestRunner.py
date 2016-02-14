import json

def RunTestsOnFile(filepath_to_json):
	data = {}
	with open(filepath_to_json) as f:
		data = json.load(f)
		print()

LoadTest("example.json")
