




'''
	from goodest.adventures.squishy.venture import squishy_venture
	squishy_venture ()
'''

#~~~~
#
from goodest.adventures.squishy.configs import retrieve_path
#
#
import pathlib
from os.path import dirname, join, normpath
import sys
import os
#
#~~~~

this_directory = str (pathlib.Path (__file__).parent.resolve ())
cwd = str (normpath (join (this_directory, "apps/web")))



def squishy_venture ():
	rubber = retrieve_path ("rubber.NFT")

	return {
		"name": "squishy",
		"kind": "process_identity",
		
		"turn on": {
			"adventure": [
				"nft", 
				"-f",
				f"{ rubber }"
			],
			
			"Popen": {},
		}
	}

