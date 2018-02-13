import re
import certstream
import tqdm
import entropy
import logging
from tld import get_tld
from Levenshtein import distance
from termcolor import colored, cprint


def callback(message,context):
	with open("baseBanquesFR.txt") as bdd:
		for line in bdd:
			score = distance(str(line), str(message['data']['source']['url']))
			tqdm.tqdm.write("%s" % score)

logging.basicConfig(format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s',level=logging.INFO)

certstream.listen_for_events(callback)
