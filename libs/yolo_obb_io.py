#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import codecs
from libs.constants import DEFAULT_ENCODING
import json

JSON_EXT = '.json'
ENCODE_METHOD = DEFAULT_ENCODING

class YOLOOBBWriter:

    def __init__(self, foldername, filename, imgSize, databaseSrc='Unknown', localImgPath=None):
        self.foldername = foldername
        self.filename = filename
        self.databaseSrc = databaseSrc
        self.imgSize = imgSize
        self.boxlist = []
        self.localImgPath = localImgPath
        self.verified = False

    def addBndBox(self, centre_x, centre_y, height, width, angle, name, difficult):
        bndbox = {'centre_x': centre_x, 'centre_y': centre_y, 'height': height, 'width': width, 'angle': angle}
        bndbox['name'] = name
        bndbox['difficult'] = difficult
        self.boxlist.append(bndbox)

    def save(self, classList=[], targetFile=None):

        out_file = None #Update yolo .txt
        out_class_file = None   #Update class list .txt

        if targetFile is None:
            out_file = open(
            self.filename + JSON_EXT, 'w', encoding=ENCODE_METHOD)
            classesFile = os.path.join(os.path.dirname(os.path.abspath(self.filename)), "classes.txt")
            out_class_file = open(classesFile, 'w')

        else:
            out_file = codecs.open(targetFile, 'w', encoding=ENCODE_METHOD)
            classesFile = os.path.join(os.path.dirname(os.path.abspath(targetFile)), "classes.txt")
            out_class_file = open(classesFile, 'w')

        # out_file.write("YOLO_OBB\n")
        json_data = []

        for box in self.boxlist:
            boxName = box['name']
            if boxName not in classList:
                classList.append(boxName)
            classIndex = classList.index(boxName)

            json_data.append({
                "Class": classIndex,
                "X": box['centre_x'],
                "Y": box['centre_y'],
                "Width": box['width'],
                "Height": box['height'],
                "Angle": -box['angle']
            })
        json.dump(json_data, out_file, indent=4)
        # print (classList)
        # print (out_class_file)
        for c in classList:
            out_class_file.write(c+'\n')

        out_class_file.close()
        out_file.close()



class YoloOBBReader:

    def __init__(self, filepath, image, classListPath=None):
        # shapes type:
        # [labbel, [(x1,y1), (x2,y2), (x3,y3), (x4,y4)], color, color, difficult]
        self.shapes = []
        self.filepath = filepath

        if classListPath is None:
            dir_path = os.path.dirname(os.path.realpath(self.filepath))
            self.classListPath = os.path.join(dir_path, "classes.txt")
        else:
            self.classListPath = classListPath

        # print (filepath, self.classListPath)

        classesFile = open(self.classListPath, 'r')
        self.classes = classesFile.read().strip('\n').split('\n')

        # print (self.classes)

        imgSize = [image.height(), image.width(),
                      1 if image.isGrayscale() else 3]

        self.imgSize = imgSize

        self.verified = False
        # try:
        self.parseYoloOBBFormat()
        # except:
            # pass

    def getShapes(self):
        return self.shapes

    def addShape(self, label, centre_x, centre_y, height, width, angle, difficult):
        self.shapes.append((label, float(centre_x), float(centre_y), float(height), float(width), float(angle), None, None, difficult)) # The 2 None's are for shape colors

    def parseYoloOBBFormat(self):
        with open(self.filepath, 'r') as f:
            data = json.load(f)
            for item in data:
                classIndex = item["Class"]
                centre_x = item["X"]
                centre_y = item["Y"]
                width = item["Width"]
                height = item["Height"]
                angle = -item["Angle"]
                label = self.classes[int(classIndex)]
                self.addShape(label, centre_x, centre_y, height, width, angle, False)
