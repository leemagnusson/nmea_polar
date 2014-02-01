import lessgps
from lessgps import testdata
from pprint import pprint
import sys

parser = lessgps.Parser('lessgps/data/nmea.yaml')
print sys.argv[1]
print parser.grammar
n = 0
with open(sys.argv[1]) as f:
	for line in f:
		n = n+1
		if line.strip() and not chr(0) in line:
			print "line (", n, "): ", line
			pprint(parser.parse(line))

#for sentence in testdata.strings:
#    print sentence
#    pprint(parser.parse(sentence))
		