# import lessgps
# from lessgps import testdata
from pprint import pprint
import sys
from pyparsing import *

# parser = lessgps.Parser('lessgps/data/nmea.yaml')
print sys.argv[1]

def to_latlon(s,l,toks):
    if toks:
        value = float(toks[0][:2]) + float(toks[0][2:])/60 # ddmm.mmmm
        if toks[1] == 'S' or toks[1] == 'W':
            value *= -1
        return value
    else:
        return 0
		
def to_utc(s,l,toks):
    return toks and toks[0] or '0'      # todo (Date also)

def parse(s):
	d = Suppress(',')
	pref = '$'
	talker = Word(alphas, exact=2)('Talker')
	r = Word('+-.' + nums)
	ro = Optional(r)
	gps_quality = oneOf('0 1 2')('GPS Quality')
	utc = r.setParseAction(to_utc)('Time (UTC)')
	ns = oneOf('N S')
	ew = oneOf('E W')
	lat = (r + d + ns).setParseAction(to_latlon)('Latitude')
	long = (r + d + ew).setParseAction(to_latlon)('Longitude')
	num_sats = r('Num Sats')
	altitude_m = Group(r('Value') + d + Literal('M')('Unit'))('Altitude')
	geoid_sep_m = Group(r('Value') + d + Literal('M')('Unit'))('Geoidal Separation')
	dgps = Group(ro('Age') + d + ro('Station ID'))('DGPS')
	checksum = '*' + Word(nums + 'ABCDEF')('CheckSum')
	valid = oneOf('A V')
	
	gga = pref + talker + Literal('GGA')('Type') + d + utc + d + lat + d + long + d + gps_quality + d + num_sats + d + r('Dilution') + d + altitude_m + d + geoid_sep_m + d + dgps + checksum
	#pprint(grammer)
	gll = pref + talker + Literal('GLL')('Type') + d + lat + d + long + d + utc + d + valid('Valid1') + d + valid('Valid2') + checksum
	gsa = pref + talker + Literal('GSA')('Type') + d 
	gsv = pref + talker + Literal('GSV')('Type') + d
	vtg = pref + talker + Literal('VTG')('Type') + d
	zda = pref + talker + Literal('ZDA')('Type') + d
	aam = pref + talker + Literal('AAM')('Type') + d
	apb = pref + talker + Literal('APB')('Type') + d
	bod = pref + talker + Literal('BOD')('Type') + d
	bwc = pref + talker + Literal('BWC')('Type') + d
	bwr = pref + talker + Literal('BWR')('Type') + d
	rmb = pref + talker + Literal('RMB')('Type') + d
	rmc = pref + talker + Literal('RMC')('Type') + d
	xte = pref + talker + Literal('XTE')('Type') + d
	dbt = pref + talker + Literal('DBT')('Type') + d
	dpt = pref + talker + Literal('DPT')('Type') + d
	mtw = pref + talker + Literal('MTW')('Type') + d
	vlw = pref + talker + Literal('VLW')('Type') + d
	vhw = pref + talker + Literal('VHW')('Type') + d
	hdg = pref + talker + Literal('HDG')('Type') + d
	mwv = pref + talker + Literal('MWV')('Type') + d
	
	grammer = gga | gll | gsa | gsv | vtg | zda | aam | apb | bod | bwc | bwr | rmb | rmc | xte | dbt | dpt | mtw | vlw | vhw | hdg | mwv
	return grammer.parseString(s).asDict()

n = 0
with open(sys.argv[1]) as f:
	for line in f:
		n = n+1
		if line.strip() and not chr(0) in line:
			print "line (", n, "): ", line
			pprint(parse(line))

#for sentence in testdata.strings:
#    print sentence
#    pprint(parser.parse(sentence))
		