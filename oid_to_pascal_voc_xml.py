"""
Location: OIDv4_ToolKit parent directory

Usage: 
    Start from OIDv4_ToolKit root directory.

    The script will create directories called To_PASCAL_XML (similar to the Label directories) in the Dataset Subdirectories.
    These directories contain the XML files.
    You need to download the Images and generate ToolKit-Style-Labels via the OIDv4_ToolKit before using this script.
    """

import os
from tqdm import tqdm
from sys import exit
import argparse
import cv2
from textwrap import dedent
from lxml import etree


XML_DIR = 'To_PASCAL_XML'
FILENAMES_DIR = 'ImageSets'


#os.chdir(os.path.join("OID", "Dataset"))
os.chdir(os.path.join("..","..","Datasets","OpenImages_face_plate"))
DIRS = os.listdir(os.getcwd())

for DIR in DIRS:
    if os.path.isdir(DIR):
        os.chdir(DIR)

        print("Currently in Subdirectory:", DIR)

        CLASS_DIRS = os.listdir(os.getcwd())
        
        for CLASS_DIR in CLASS_DIRS:
            if os.path.isdir(CLASS_DIR):
                os.chdir(CLASS_DIR)

                print("\n" + "Creating PASCAL VOC XML Files for Class:", CLASS_DIR)
                # Create Directory for annotations if it does not exist yet
                if not os.path.exists(XML_DIR):
                    os.makedirs(XML_DIR)

                #Read Labels from OIDv4 ToolKit
                os.chdir("Label")

                filenames_str = [] #list of all files names

                #Create PASCAL XML
                for filename in tqdm(os.listdir(os.getcwd())):
                    if filename.endswith(".txt"):
                        filename_str = str.split(filename, ".")[0]
                        filenames_str.append(filename_str)


                        annotation = etree.Element("annotation")
                        
                        os.chdir("..")
                        folder = etree.Element("folder")
                        folder.text = os.path.basename(os.getcwd())
                        annotation.append(folder)

                        filename_xml = etree.Element("filename")
                        filename_xml.text = filename_str + ".jpg"
                        annotation.append(filename_xml)

                        path = etree.Element("path")
                        path.text = os.path.join(os.path.dirname(os.path.abspath(filename)), filename_str + ".jpg")
                        annotation.append(path)

                        source = etree.Element("source")
                        annotation.append(source)

                        database = etree.Element("database")
                        database.text = "Unknown"
                        source.append(database)

                        size = etree.Element("size")
                        annotation.append(size)

                        width = etree.Element("width")
                        height = etree.Element("height")
                        depth = etree.Element("depth")

                        img = cv2.imread(filename_xml.text)

                        width.text = str(img.shape[1])
                        height.text = str(img.shape[0])
                        depth.text = str(img.shape[2])

                        size.append(width)
                        size.append(height)
                        size.append(depth)

                        segmented = etree.Element("segmented")
                        segmented.text = "0"
                        annotation.append(segmented)

                        os.chdir("Label")
                        label_original = open(filename, 'r')

                        # Labels from OIDv4 Toolkit: name_of_class X_min Y_min X_max Y_max
                        for line in label_original:
                            line = line.strip()
                            l = line.split(' ')
                            l_size = len(l)
                            class_name = ' '.join(str(l[e]) for e in range(0, l_size-4))
                            xmin_l = str(int(float(l[l_size-4])))
                            ymin_l = str(int(float(l[l_size-3])))
                            xmax_l = str(int(float(l[l_size-2])))
                            ymax_l = str(int(float(l[l_size-1])))
                            
                            obj = etree.Element("object")
                            annotation.append(obj)

                            name = etree.Element("name")
                            name.text = class_name
                            obj.append(name)

                            pose = etree.Element("pose")
                            pose.text = "Unspecified"
                            obj.append(pose)

                            truncated = etree.Element("truncated")
                            truncated.text = "0"
                            obj.append(truncated)

                            difficult = etree.Element("difficult")
                            difficult.text = "0"
                            obj.append(difficult)

                            bndbox = etree.Element("bndbox")
                            obj.append(bndbox)

                            xmin = etree.Element("xmin")
                            xmin.text = xmin_l
                            bndbox.append(xmin)

                            ymin = etree.Element("ymin")
                            ymin.text = ymin_l
                            bndbox.append(ymin)

                            xmax = etree.Element("xmax")
                            xmax.text = xmax_l
                            bndbox.append(xmax)

                            ymax = etree.Element("ymax")
                            ymax.text = ymax_l
                            bndbox.append(ymax)


                        # write xml to file
                        s = etree.tostring(annotation, pretty_print=True)
                        with open("../"+XML_DIR+"/"+filename_str + ".xml", 'wb') as f:
                            f.write(s)
                            f.close()

                os.chdir("..")
                # Create Directory for filenames if it does not exist yet
                if not os.path.exists(FILENAMES_DIR):
                    os.makedirs(FILENAMES_DIR)
                # write every file names in a file
                with open(FILENAMES_DIR+"/filenames_xml.txt", 'w') as f:
                    f.write('\n'.join(filenames_str))
                    f.close()
                os.chdir("..")
                   
        os.chdir("..")
                   