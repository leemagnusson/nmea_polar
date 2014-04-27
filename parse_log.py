
import tarfile
import argparse
import parse_file2
import os.path

parser = argparse.ArgumentParser(description='convert nmea to csv')
parser.add_argument('file', nargs=1,
                   help='file')

args = parser.parse_args()

print args.file

tar = tarfile.open(args.file[0], 'r')
print [x for x in tar]
a = list(tar)
#tar.extract(a[2],'tmp')

for item in a:
    if os.path.isfile('tmp2/' + item.name):
        print 'item exists: ' + item.name
    else:
        tar.extract(item,'tmp2')
        parse_file2.parse_file('tmp2/{0}'.format(item.name),\
                          'tmp2/{0}.csv'.format(item.name))
