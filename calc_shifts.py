##
#name: calc_shifts.py
#
#purpose: takes in a list of fits files and calculates the shift of each with respect to the first file
#
#date last edited: 3/10/17
#
#author: Grayson Petter
#
##

from astropy.io import ascii
from astropy.table import Table
import os
import sewpy
import sys
from pyraf import iraf

imgfile=''

cur_dir=os.getcwd()

#uncomment this if sewpy throws an error
#import logging
#logging.basicConfig(format='(levelname)s: %(name)s(%(funcName)s): %(message)s', level=logging.DEBUG)

#get list of images from command line
if len(sys.argv)>1:
    imgfile = sys.argv[1]
else:
    imgfile = raw_input("Please provide a .txt file as your image list: ")

#path names for work and output folders
mypath=cur_dir+'/shifts/'
mypath2=cur_dir+'/work/'


#create work/output directories if they don't already exist
if not os.path.exists(mypath):
    os.makedirs(mypath)
if not os.path.exists(mypath2):
    os.makedirs(mypath2)


imglist = []
matchlist=[]
sexlist = []
trimmed_list = []
shiftlist = []


#configure source extractor
sew=sewpy.SEW(params=["NUMBER", "X_IMAGE", "Y_IMAGE", "FLAGS", "CLASS_STAR"], config={"MAG_ZEROPOINT":32.78, "PIXEL_SCALE":0.20099988, "SEEING_FWHM":0.8, "DETECT_THRESH":5.0, "FILTER_NAME":"gauss_4.0_7x7.conv"})

xlist=[]
ylist=[]

#add .fits files to imglist
fimg = open(imgfile, "r")
lines=fimg.readlines()
for x in lines:
    x=x.replace('\n', '')
    if x.endswith('.fits'):
        imglist.append(x)

#output Sextractor list
for num in range(0, imglist.__len__()):
    #run Sextractor
    out=sew(imglist[num])
    #write table to 'sexout.txt' file
    str1=imglist[num].split('.fits')[0]
    name1='%s_sexout.txt' % (str1)
    sexlist.append(name1)
    fullname=mypath2+name1
    ascii.write(out["table"], fullname, overwrite=True)


#removes objects that throw flags or aren't likely stars
#places remaining coordinates in /work/ directory with '_extracted.txt' suffix
for num in range(0, sexlist.__len__()):
    thefile=mypath2+sexlist[num]
    f = open(thefile, "r")
    lines = f.readlines()
    for x in lines:
        #check if flags equal 0 and class_star is high
        if x.startswith('N') == False and x.split()[3] == '0' and x.split()[4]>0.98:
            xlist.append(x.split()[1])
            ylist.append(x.split()[2])
    f.close()
    str = imglist[num].split('.')[0]
    name='%s_extracted.txt' % (str)
    full=mypath2+name
    ascii.write([xlist, ylist], full, names=('#x', 'y'), overwrite=True)
    xlist=[]
    ylist=[]

#read in table which has been cut for quality
for file in os.listdir(mypath2):
    if file.endswith('extracted.txt'):
        trimmed_list.append(file)

#use xyxymatch to calculate shifts
for x in range(1, trimmed_list.__len__()):
    str1=mypath2+trimmed_list[0]
    str = mypath2 + trimmed_list[x]
    str_out = mypath2 + trimmed_list[0].split('_extracted')[0] + "--" + trimmed_list[x].split('_extracted')[0] + "_match.txt"
    iraf.xyxymatch(input=str, reference=str1, output=str_out, tolerance=15, separation=.01, verbose="no")

for file in os.listdir(mypath2):
    if file.endswith('match.txt'):
        matchlist.append(file)

#read xyxymatch's results, find shifts
string=mypath2 + trimmed_list[0].split('_extracted')[0] + "--"
for x in range(1, matchlist.__len__()+1):
    thefile=string+trimmed_list[x].split('_extracted')[0]+"_match.txt"
    f=open(thefile)
    lines=f.readlines()

    for y in lines:
        if y.startswith("# dx"):


            if y.split()[2]!="0.00":
                xlist.append(y.split()[2])
                ylist.append(y.split()[4])

str3=imglist[0].split('.')[0]+"_"
imglist.pop(0)

#write file with all calculated shifts in respect to the first image provided
ascii.write([imglist,xlist,ylist], (mypath+str3+"shifts.txt"), names=('#|image|', '|x_shift|','|y_shift|'), overwrite=True)
