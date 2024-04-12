import sys
import os
import PIL.Image
from datetime import datetime
import shutil
import logging

def main():
    now = datetime.now()
    ext = (".gif", ".jpeg", ".jpg", ".png")
    input_verify()
    os.chdir(sys.argv[1])
    logging.basicConfig(format='%(levelname)s (%(asctime)s): %(message)s (line: %(lineno)d [%(filename)s])', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO, filename="photobackup.log")
    create_completed()
    filelist = os.listdir()
    logging.info("Begining Backup")
    for file in filelist:
        datedict = None
        os.chdir(sys.argv[1])
        if file.lower().endswith(ext):
            datedict = exifextract(file)
            if(datedict):
                logging.info("Date metadata extracted for " + file)
                create_path(datedict)
            else:
                logging.info("No Date Metadata found for " + file + ". Proceeding with Runtime based sorting")
                year = str(now.year)
                month = str(now.month)
                datedict = {"year":(year),"month":(month),"file":file}
                create_path(datedict)
            transferto_destination(datedict)
            logging.info ("Moving " + file + " to the Completed Folder.")
            shutil.move(file, "completed")
    logging.info("Backup Complete")

def exifextract(file):

    datedict = {"year":None,"month":None,"day":None}
    #file = "test.jpg"
    img = PIL.Image.open(file)
    exif_data = img._getexif()

    try:
        datetimesplit = (exif_data[306]).split(" ")
        datesplit = (datetimesplit[0]).split(":")
        year = datesplit[0]
        month = datesplit[1]
        month = month.lstrip("0")
        datedict.update({"year":year,"month":month,"file":file})   
    except:TypeError

    if datedict["year"]:
        return(datedict)
    else:
        return None
    
def input_verify():
    if len(sys.argv) != 3:
        print("Incorrect number of command line arguments")
        sys.exit(1)
    if(os.path.exists(sys.argv[1]) is False or os.path.isdir(sys.argv[1]) is False):
        print("Starting Path is invalid")
        sys.exit(1)
    if(os.path.exists(sys.argv[2]) is False or os.path.isdir(sys.argv[2]) is False):
        print("Destination Path is invalid")
        sys.exit(1)

def create_completed():

    if(os.path.isdir("completed")):
        logging.info ("Completed Directory Already Created")
    else:
        os.mkdir("completed")
        logging.info("Creating Completed Directory")

def create_path(datedict):
    
    year = (datedict["year"])
    month = (datedict["month"])
    os.chdir(sys.argv[2])
    if(os.path.isdir(year)):
        logging.info("Year directory already present.")
    else:
        logging.info("Creating folder named " + year + " .")
        os.mkdir(year)
    os.chdir(year)
    
    if(os.path.isdir(month)):
        logging.info("Month directory already present.")
    else:
        logging.info("Creating folder named " + month + " .")
        os.mkdir(month)
    os.chdir(month)

def transferto_destination(datedict):
    if '\\' in sys.argv:
        slash = '\\'
    else:
        slash = '/'
    os.chdir(sys.argv[1])
    year = (datedict["year"])
    month = (datedict["month"])
    file = (datedict["file"])
    destpath = sys.argv[2] + slash + year + slash + month + slash + file
    if(os.path.exists(destpath)):
        logging.info(file + " already exists at destination.")
    else:
        logging.info("Copying " + file + " to destination")
        shutil.copy2(file, destpath)

       



if __name__ == "__main__":
    main()


