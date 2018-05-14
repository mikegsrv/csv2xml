import csv
import sys
import argparse
import os
from PIL import Image

#TODO: add progress status
example_text = '''Usage: python[3] csv2xml.py csvfile.csv /path/to/images /output/folder'''
descript="""Python script created to parse CSV file provided with
Russian Traffic Signs Dataset (RTSD) to XML files needed by
Darkflow / Darknet implementations. 

Big thanks to the creators of RTSD - Vladislav Shakhuro and Anton Konushin.
http://graphics.cs.msu.ru/ru/node/1266"""

parser = argparse.ArgumentParser(description=descript,
                                 epilog=example_text,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("csvfile", help="path to CSV file")
parser.add_argument("/path/to/images", help="path to folder with dataset images (without trailing slash)")
parser.add_argument("/output/folder/", help="path to place output XML files")

parser.parse_args()


f = open(sys.argv[1])
folder = sys.argv[2]
output = sys.argv[3]

if not os.path.exists(output):
    os.makedirs(output)

csv_f = csv.reader(f)
next(csv_f, None)


def convertRow(r, f, w, h):
    return """
    <?xml version="1.0"?>
    <annotation>
        <folder>"%s"</folder>
        <filename>"%s"</filename>
        <size>
            <width>"%s"</width>
            <height>"%s"</height>
        </size>
        <object>
            <name>"%s"</name>
            <bndbox>
                <xmin>"%s"</xmin>
                <ymin>"%s"</ymin>
                <xmax>"%s"</xmax>
                <ymax>"%s"</ymax>
            </bndbox>
        </object>
    </annotation>""" % (f, r[0], w, h, r[6], r[1], r[2], r[1] + r[3], r[2] + r[4])


for row in csv_f:
    im = Image.open(folder + "/" + row[0])
    width, height = im.size
    data = convertRow(row, folder, width, height)
    xml = os.path.join(output, row[0])
    count = ""
    while os.path.isfile(xml + str(count) + ".xml"):
        count += 1

    f = open(xml + count + ".xml", "w+")
    f.write(data)
    f.close()
