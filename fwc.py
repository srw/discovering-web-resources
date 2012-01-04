#!/usr/bin/python2.7

import argparse
import sys
from focused_web_crawler import FocusedWebCrawler
import logging
import code
import yaml
from constraint import Constraint

def main():
	logger = logging.getLogger('data_big_bang.focused_web_crawler')
	ap = argparse.ArgumentParser(description='Discover web resources associated with a site.')
	ap.add_argument('input', metavar='input.yaml', type=str, nargs=1, help ='YAML file indicating the sites to crawl.')
	ap.add_argument('output', metavar='output.yaml', type=str, nargs=1, help ='YAML file with the web resources discovered.')


	args = ap.parse_args()

	input = yaml.load(open(args.input[0], "rt"))

	fwc = FocusedWebCrawler()

	for e in input:
		e.update({'constraint': Constraint()})
		fwc.queue.put(e)

#	fwc.queue.put({'url': 'http://www.linkedin.com', 'constraint': Constraint()})
#	fwc.queue.put({'url': 'http://www.symantec.com', 'constraint': Constraint()})

#	fwc.queue.put({'url': 'http://www.dell.com', 'key':'dell', 'constraint': Constraint()})
#	fwc.queue.put({'url': 'http://www.apple.com', 'constraint': Constraint()})
#	fwc.queue.put({'url': 'http://www.apple.com', 'constraint': Constraint()})
#	fwc.queue.put({'url': 'http://www.matasano.com', 'constraint': Constraint()})
#	fwc.queue.put({'url': 'http://www.basecamphq.com', 'key': 'basecamp', 'constraint': Constraint()})
#	fwc.queue.put({'url': 'http://www.gnip.com', 'key':'gnip', 'constraint': Constraint()})
#	fwc.queue.put({'key':'datasift', 'url': 'http://www.datasift.com', 'constraint': Constraint()})
#	fwc.queue.put({'url': 'http://www.foundrygroup.com', 'constraint': Constraint()})
#	fwc.queue.put({'url': 'http://www.avc.com', 'constraint': Constraint()})

	







	fwc.start()
	fwc.join()

	with open(args.output[0], "wt") as s:
		yaml.dump(fwc.collection, s, default_flow_style = False)

#	locals = globals()
#	locals.update({'fwc':fwc})
#	code.InteractiveConsole(locals = locals).interact()

if __name__ == '__main__':
	main()
