import logging
import sys
import datetime
import certstream


def lev(a, b):
    if not a: return len(b)
    if not b: return len(a)
    return min(lev(a[1:], b[1:])+(a[0] != b[0]), lev(a[1:], b)+1, lev(a, b[1:])+1)

def main(message,context):
	with open("baseBanquesFR.txt") as bdd:
		for line in bdd:
			print(lev(line, message['data']['source']['url']))

logging.basicConfig(format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s',level=logging.INFO)

certstream.listen_for_events(main)

main(message,context)
