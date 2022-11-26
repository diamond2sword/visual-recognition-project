import ast
import shutil
import os

classDictFile = open("classDict.json", "r")
classDictStr = classDictFile.read()
classDict = ast.literal_eval(classDictStr)
classes = classDict.keys()

from bing_image_downloader import downloader

pics_per_class = 3
downloadsPath = "downloadedPictures"
samplesPath = "picsFolder/anyClass"
for label in classes:
    query_string = classDict[label]["strings"]["search_query"]
    downloader.download(query_string, limit=pics_per_class, output_dir=downloadsPath, adult_filter_off=True, force_replace=False, timeout=60)
    classPicsPath = f"{downloadsPath}/{query_string}"
    for picName in os.listdir(classPicsPath):
        newPicName = f"{label}_{picName}"
        downloadPath = f"{classPicsPath}/{picName}"
        samplePath = f"{samplesPath}/{newPicName}"
        shutil.copyfile(downloadPath, samplePath)
