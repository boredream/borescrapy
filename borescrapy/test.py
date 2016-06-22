import urllib2

url = 'http://vcntv.dnion.com/flash/mp4video47/TMS/2015/11/13/8d9824f36db5436c93374b4206061489_h264818000nero_aac32-10.mp4'

try:
    f = urllib2.urlopen(url)
except urllib2.HTTPError, e:
    print 'errorrrrrrrrrrrrrrrrrrrrrrrr ~ ' + str(e)
finally:
    print "successsssssssssssssssssssssssss ~ " + str(f)
