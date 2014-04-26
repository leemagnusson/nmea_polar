# import lessgps
# from lessgps import testdata
from pprint import pprint
import sys
from pyparsing import *
import datetime
import math


# parser = lessgps.Parser('lessgps/data/nmea.yaml')
print sys.argv[1]

def to_lat(s,l,toks):
    if toks:
        value = float(toks[0][:2]) + float(toks[0][2:])/60 # ddmm.mmmm
        if toks[1] == 'S':
            value *= -1
        return value
    else:
        return 0

def to_lon(s,l,toks):
    if toks:
        value = float(toks[0][:3]) + float(toks[0][3:])/60 # dddmm.mmmm
        if toks[1] == 'W':
            value *= -1
        return value
    else:
        return 0
		
def to_utc(s,l,toks):
	d = dict(toks)
	if 'Time (UTC)' in d:
		dt = datetime.datetime.strptime(d['Time (UTC)'],'%H%M%S')
		return datetime.time(dt.hour,dt.minute,dt.second)
	else:
		return None
    
def to_datetime(toks):
	if 'Datetime (UTC)' in dict(toks):
		di = dict(toks['Datetime (UTC)'])
		d = datetime.datetime.strptime(di['Year']+di['Month']+di['Day'],'%y%m%d')
		t = di['Time (UTC)']
		dt = d.replace(hour=t.hour,minute=t.minute,second=t.second)
		return dt
	else:
		return None
    #return datetime.datetime(toks['Year'], toks['Month'], toks['Day'])
def to_dict_value(toks):
#	print dict(dict(toks).values()[0])
	return dict(dict(toks).values()[0])
	
def to_float(toks):
	print 'in to_float'
	print toks

def parse(s):
	d = Suppress(',')
	pref = LineStart() + '$'
	talker = Word(alphas, exact=2)('Talker')
	r = Word('+-.' + nums).setParseAction(to_float)
	ro = Optional(r)
	gps_quality = oneOf('0 1 2')('GPS Quality')
	utc = r.setParseAction(to_utc)('Time (UTC)')
	ns = oneOf('N S')
	ew = oneOf('E W')
	lat = (r + d + ns).setParseAction(to_lat)('Latitude')
	lon = (r + d + ew).setParseAction(to_lon)('Longitude')
	num_sats = r('Num Sats')
	altitude_m = (r('Value') + d + Literal('M')('Unit')).setParseAction(to_dict_value)('Altitude')
	geoid_sep_m = Group(r('Value') + d + Literal('M')('Unit')).setParseAction(to_dict_value)('Geoidal Separation')
	dgps = Group(ro('Age') + d + ro('Station ID')).setParseAction(to_dict_value)('DGPS')
	checksum = '*' + Word(nums + 'ABCDEF')('CheckSum')
	valid = oneOf('A V')
	selection_mode = oneOf('A')('Selection Mode')
	arrival = Optional(oneOf('A V'))
	dt = Group(utc + d + r('Day') + d + r('Month') + d + r('Year')).setParseAction(to_datetime)('Datetime (UTC)')
	
	gga = pref + talker + Literal('GGA')('Type') + d + utc + d + lat + d + lon + d + gps_quality + d + num_sats + d + r('Dilution') + d + altitude_m + d + geoid_sep_m + d + dgps + checksum
	#pprint(grammer)
	gll = pref + talker + Literal('GLL')('Type') + d + lat + d + lon + d + utc + d + valid('Valid1') + d + valid('Valid2') + checksum
	gsa = pref + talker + Literal('GSA')('Type') + d + selection_mode + d + r('Mode') + d + ro('Id1') + d + ro('Id2') + d + ro('Id3') + d + ro('Id4') + d + ro('Id5') + d + ro('Id6') + d + ro('Id7') + d + ro('Id8') + d + ro('Id9') + d + ro('Id10') + d + ro('Id11') + d + ro('Id12') + d + ro('PDOP') + d + ro('HDOP') + d + ro('VDOP') + checksum
	gsv = pref + talker + Literal('GSV')('Type') + d
	vtg = pref + talker + Literal('VTG')('Type') + d + r('Track Degrees True') + d + 'T' + d + r('Track Degrees Magnetic') + d + 'M' + d + r('Speed Knots') + d + 'N' + d + r('Speed kmh') + d + 'K' + d + 'A' + checksum
	zda = pref + talker + Literal('ZDA')('Type') + d + dt + d + r('Offset') + d + ro('Unknown') + checksum
	aam = pref + talker + Literal('AAM')('Type') + d + arrival('Arrival Circle') + d + arrival('Perpendicular Past Waypoint') + \
                                                       d + r('Arrival circle radius') + d + 'N' + d + Optional(Word(alphanums))('Waypoint ID') + checksum
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
	vhw = pref + talker + Literal('VHW')('Type') + d + r('Water Heading Degrees True') + d + 'T' + d + r('Water Heading Degrees Magnetic') + d + 'M' + d + r('SOW Knots') + d + 'N'
	hdg = pref + talker + Literal('HDG')('Type') + d + r('Magnetic Heading')
	mwv = pref + talker + Literal('MWV')('Type') + d + ro('Wind Angle Relative') + d + 'R' + d + ro('Wind Speed Relative') + \
                                                       d + 'N'
      #  mwvt = pref + talker + Literal('MWV')('Type') + d + r('Wind Angle True') + d + 'T'
	
	grammer = gga | gll | gsa | gsv | vtg | zda | aam | apb | bod | bwc | bwr | rmb | rmc | xte | dbt | dpt | mtw | vlw | vhw | hdg | mwv
        try:
            return grammer.parseString(s).asDict()
	except Exception as e:
            print e
            print s
            return {}



class DataItem:
    def __init__(self,name,type):
        self.name = name
        self.value = []
        self.type = type
    def append(self,value):
        self.value.append(self.type(value))
    def __repr__(self):
        if self.type is float:
            if self.value:
                return str(sum(self.value)/len(self.value))
            else:
                return ''
        else:
            return str(self.value)
 
fields = [('Latitude',float),('Longitude',float),
          ('Speed Knots',float),('Magnetic Heading',float),
          ('Wind Angle Relative',float), ('Wind Speed Relative',float),
          ('SOW Knots',float)]

class Data:
    def __init__(self,time):
        self.time = time
        self.data = {k:DataItem(k,v) for k,v in fields}
    def append(self,d):
        for k,v in d.items():
           # if k not in self.data:
           #     self.data[k] = DataItem(k)
            if k in self.data:
                self.data[k].append(v)
    def __repr__(self):
        return 'Time: {0}\tData: {1}'.format(self.time,self.data)
    def to_csv(self):
        return ', '.join([str(self.data[x[0]]) for x in fields])




def parse_file(file,file_out):
    n = 0
    last_time = None
    dd = []
    with open(file) as f, open(file_out,'w') as fout:
        fout.write(', '.join([x[0] for x in fields]) + '\n')
	for line in f:
		n = n+1
		if line.strip() and not chr(0) in line:
			#print "line (", n, "): ", line.strip()
			d = parse(line)
			
			if 'Time (UTC)' in d:
                            if d['Time (UTC)'] != last_time:
                                last_time = d['Time (UTC)'] 
                            #    print "\n********** New time **********\n", last_time
                                print last_time
                                dd.append(Data(last_time))
                                if len(dd) > 1:
                                    print dd[-2].to_csv()
                                    fout.write(dd[-2].to_csv() + '\n')
                                    fout.flush()

                        if last_time:
                            dd[-1].append(d)

                        #pprint(d)
			#print
#    pprint(dd)
#    print

            

#for sentence in testdata.strings:
#    print sentence
#    pprint(parser.parse(sentence))
		
