#!/usr/bin/python
#

import getopt
import os
import sys

import numpy
from annotation import Annotation
# python imports
from anue_labels import name2label

# Image processing
try:
    import PIL
    print("Pillow version:", PIL.__version__)
except ImportError:
    print("Please install the module 'Pillow' for image processing, e.g.")
    print("pip install pillow")
    sys.exit(-1)

try:
    import PIL.Image as Image
    import PIL.ImageDraw as ImageDraw
except ImportError:
    print("Failed to import the image processing packages.")
    sys.exit(-1)


sys.path.append(os.path.normpath(os.path.join(
    os.path.dirname(__file__), '..', 'helpers')))

# Print the information
def printHelp():
    print('{} [OPTIONS] inputJson outputImg'.format(
        os.path.basename(sys.argv[0])))
    print('')
    print('Reads labels as polygons in JSON format and converts them to label images,')
    print('where each pixel has an ID that represents the ground truth label.')
    print('')
    print('Options:')
    print(' -h                 Print this help')
    print(' -t                 Use the "trainIDs" instead of the regular mapping. See "labels.py" for details.')


def printError(message):
    print('ERROR: {}'.format(message))
    print('')
    print('USAGE:')
    printHelp()
    sys.exit(-1)


def createLabelImage(inJson, annotation, encoding, outline=None):
    size = (annotation.imgWidth, annotation.imgHeight)

    if encoding == "id":
        background = name2label['unlabeled'].id
    elif encoding == "csId":
        background = name2label['unlabeled'].csId
    elif encoding == "csTrainId":
        background = name2label['unlabeled'].csTrainId
    elif encoding == "level4Id":
        background = name2label['unlabeled'].level4Id
    elif encoding == "level3Id":
        background = name2label['unlabeled'].level3Id
    elif encoding == "level2Id":
        background = name2label['unlabeled'].level2Id
    elif encoding == "level1Id":
        background = name2label['unlabeled'].level1Id
    elif encoding == "color":
        background = name2label['unlabeled'].color
    else:
        print("Unknown encoding '{}'".format(encoding))
        return None

    if encoding == "color":
        labelImg = Image.new("RGBA", size, background)
    else:
        labelImg = Image.new("L", size, background)

    drawer = ImageDraw.Draw(labelImg)

    for obj in annotation.objects:
        label = obj.label
        polygon = obj.polygon

        if obj.deleted or len(polygon) < 3:
            continue

        if (not label in name2label) and label.endswith('group'):
            label = label[:-len('group')]

        if not label in name2label:
            print("Label '{}' not known.".format(label))
            tqdm.write("Something wrong in: " + inJson)
            continue

        if name2label[label].id < 0:
            continue

        if encoding == "id":
            val = name2label[label].id
        elif encoding == "csId":
            val = name2label[label].csId
        elif encoding == "csTrainId":
            val = name2label[label].csTrainId
        elif encoding == "level4Id":
            val = name2label[label].level4Id
        elif encoding == "level3Id":
            val = name2label[label].level3Id
        elif encoding == "level2Id":
            val = name2label[label].level2Id
        elif encoding == "level1Id":
            val = name2label[label].level1Id
        elif encoding == "color":
            val = name2label[label].color

        try:
            if outline:
                drawer.polygon(polygon, fill=val, outline=outline)
            else:
                drawer.polygon(polygon, fill=val)
        except:
            print("Failed to draw polygon with label {}".format(label))
            raise

    return labelImg


def json2labelImg(inJson, outImg, encoding="ids"):
    annotation = Annotation()
    annotation.fromJsonFile(inJson)
    labelImg = createLabelImage(inJson, annotation, encoding)
    labelImg.save(outImg)


def main(argv):
    trainIds = False
    try:
        opts, args = getopt.getopt(argv, "ht")
    except getopt.GetoptError:
        printError('Invalid arguments')
    for opt, arg in opts:
        if opt == '-h':
            printHelp()
            sys.exit(0)
        elif opt == '-t':
            trainIds = True
        else:
            printError("Handling of argument '{}' not implementend".format(opt))

    if len(args) == 0:
        printError("Missing input json file")
    elif len(args) == 1:
        printError("Missing output image filename")
    elif len(args) > 2:
        printError("Too many arguments")

    inJson = args[0]
    outImg = args[1]

    if trainIds:
        json2labelImg(inJson, outImg, "trainIds")
    else:
        json2labelImg(inJson, outImg)


if __name__ == "__main__":
    main(sys.argv[1:])
