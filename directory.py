# server python file
from flask import Flask, render_template, abort,  send_file #, safe_join
# from flask.helpers import safe_join
from pathlib import Path
import os
import datetime as dt
import pandas as pd
import numpy as np

# create a server instance
app = Flask(__name__)
FolderPath = r"C:\Users\Hostbooks\Desktop\EmailAutoFlask\static\excel"

@app.route('/')
# def index():
#     return "Hello World!!!"

def getReadableByteSize(num, suffix='B') -> str:
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)

def getTimeStampString(tSec: float) -> str:
    tObj = dt.datetime.fromtimestamp(tSec)
    tStr = dt.datetime.strftime(tObj, '%Y-%m-%d %H:%M:%S')
    return tStr

def getIconClassForFilename(fName):
    fileExt = Path(fName).suffix
    fileExt = fileExt[1:] if fileExt.startswith(".") else fileExt
    fileTypes = ["aac", "ai", "bmp", "cs", "css", "csv", "doc", "docx", "exe", "gif", "heic", "html", "java", "jpg", "js", "json", "jsx", "key", "m4p", "md", "mdx", "mov", "mp3",
                 "mp4", "otf", "pdf", "php", "png", "pptx", "psd", "py", "raw", "rb", "sass", "scss", "sh", "sql", "svg", "tiff", "tsx", "ttf", "txt", "wav", "woff", "xlsx", "xml", "yml"]
    fileIconClass = f"bi bi-filetype-{fileExt}" if fileExt in fileTypes else "bi bi-file-earmark"
    return fileIconClass

# route handler
@app.route('/reports/', defaults={'reqPath': ''})
@app.route('/reports/<path:reqPath>')
def getFiles(reqPath):
    # Join the base and the requested path
    # could have done os.path.join, but safe_join ensures that files are not fetched from parent folders of the base folder
    # absPath = safe_join(FolderPath, reqPath)
    absPath=FolderPath+reqPath

    # Return 404 if path doesn't exist
    if not os.path.exists(absPath):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(absPath):
        return send_file(absPath)

    # Show directory contents
    def fObjFromScan(x):
        fileStat = x.stat()
        # return file information for rendering
        return {'name': x.name,
                'fIcon': "bi bi-folder-fill" if os.path.isdir(x.path) else getIconClassForFilename(x.name),
                'relPath': os.path.relpath(x.path, FolderPath).replace("\\", "/"),
                'mTime': getTimeStampString(fileStat.st_mtime),
                'size': getReadableByteSize(fileStat.st_size)}
    fileObjs = [fObjFromScan(x) for x in os.scandir(absPath)]
    # get parent directory url
    parentFolderPath = os.path.relpath(
        Path(absPath).parents[0], FolderPath).replace("\\", "/")
    return render_template('directory.html', data={'files': fileObjs,
                                                 'parentFolder': parentFolderPath})
@app.route('/view/<reqPath>')
def view(reqPath):
    # Read the File using Flask request
    # file = request.files['file']
    print(reqPath)
    file = "C:/Users/Hostbooks/Desktop/EmailAutoFlask/junk/"+reqPath
    # Parse the data as a Pandas DataFrame type
    data = pd.read_excel(file)
    # data = pd.read_excel(dfs)
    df = data.replace(np.NaN, '')
    # Return HTML snippet that will render the table
    return df.to_html()

# run the server
app.run(host="0.0.0.0", port=50100, debug=True)