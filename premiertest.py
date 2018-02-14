import re
import certstream
import tqdm
import entropy
import logging
import stix2
from tld import get_tld
from Levenshtein import distance
from termcolor import colored, cprint
from datetime import date

import GeoIP

gi = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
def callback(message,context):
	# Tout d'abord, on ouvre le fichier contenant notre base de données
	with open("baseBanquesFR.txt") as bdd:
		# on fait les tests pour chaque ligne de la bdd
		for line in bdd:
			# si on se trouve dans le cas d'une mose à jour de certificat on compare avec la distance de Levenshtein le nom de domaine du site à tester et une ligne de la base
			if message['message_type'] == "certificate_update":
				domain = message['data']['leaf_cert']['all_domains']
				score = distance(str(line), str(domain[0]))
				# si la distance est inférieure à la moitié de la longueur de la ligne de la base, on montre les deux lignes sur le shell
				if (score < len(line)/2):
					tqdm.tqdm.write("%s" % str(domain[0]))
					tqdm.tqdm.write("%s" % str(line))
					# si le site n'est pas hébergé en France, on l'écrit dans un fichier
					if (gi.country_code_by_name(str(domain[0])) != "FR"):
						with open("sitesMisEnAlerte.txt","a") as file : 
							file.write("url : " + domain[0] + ", date : " + str(date.today()) + '\n')
					

logging.basicConfig(format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s',level=logging.INFO)

certstream.listen_for_events(callback)
