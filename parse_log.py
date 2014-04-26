
import tarfile
import argparse
import parse_file

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
    tar.extract(item,'tmp')
    parse_file.parse_file('tmp/{0}'.format(item.name),\
                      'tmp/{0}.csv'.format(item.name))
