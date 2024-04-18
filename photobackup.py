import sys
import os
import PIL.Image
from datetime import datetime
import shutil
import logging
import argparse

#Define user inputted arguments 
parser = argparse.ArgumentParser()

parser.add_argument("--path", "-p", type=str, dest= "startpath", required=True)
parser.add_argument("--destinationpath", "-dp", type=str, dest= "destinationpath", required=True)
args = parser.parse_args()

#Provision for Windows paths
if '\\' in args:
    slash = '\\'
else:
    slash = '/'

#Define Logging Preferences
logging.basicConfig(format='%(levelname)s (%(asctime)s): %(message)s (line: %(lineno)d [%(filename)s])', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO, filename="photobackup.log")


def main():
    now = datetime.now()
    ext = (".gif", ".jpeg", ".jpg", ".png")
    #Make sure that required arguments were provided and that the paths exist
    input_verify(args)
    #Change Directory to the given starting path
    os.chdir(args.startpath)
    #List all files in the Starting Directory
    filelist = os.listdir()
    backupstart = None
    #Loop through the files to see if they have extensions photo extensions
    for file in filelist:
        datedict = None
        #Ensure that the directory is always changed back to the Starting directory
        os.chdir(args.startpath)
        if file.lower().endswith(ext):
            #Ensure that the "Begining Backup log is only given once and not given if nothing was done"
            if backupstart is None:
                logging.info("Begining Backup")
                backupstart = True
                #Create the directory to move the files to once copied
                create_completed()
            #Extract the Creation Date Metadata
            datedict = exifextract(file)
            #Check if the metadata was present and successfully added to the dictionary
            #If it was not pulled and added, it will set the date to the current date and month
            if(datedict):
                logging.info("Date metadata extracted for " + file)
            else:
                logging.info("No Date Metadata found for " + file + ". Proceeding with Runtime based sorting")
                year = str(now.year)
                month = str(now.month).zfill(2)
                datedict = {"year":(year),"month":(month),"file":file}
            #create the path using the month and year created above
            create_path(datedict)
            #Copy file to the provided destination using the previously created folder structure.
            transferto_destination(datedict)
            logging.info ("Moving " + file + " to the Completed Folder.")
            if os.path.exists(args.startpath + slash + "completed" + slash + file):
                os.remove(args.startpath + slash + "completed" + slash + file)
            #Move the file to the "completed folder"
            shutil.move(file, "completed")
    if backupstart is not None:
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
        #month = month.lstrip("0")
        datedict.update({"year":year,"month":month,"file":file})   
    except:TypeError

    if datedict["year"]:
        return(datedict)
    else:
        return None
    
def input_verify(args):
    if(os.path.exists(args.startpath) is False or os.path.isdir(args.startpath) is False):
        print("Starting Path Missing or invalid")
        sys.exit(1)
    if(os.path.exists(args.destinationpath) is False or os.path.isdir(args.destinationpath) is False):
        print("Destination Path Missing or invalid")
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
    os.chdir(args.destinationpath)
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
    os.chdir(args.startpath)
    year = (datedict["year"])
    month = (datedict["month"])
    file = (datedict["file"])
    destpath = args.destinationpath + slash + year + slash + month + slash + file
    if(os.path.exists(destpath)):
        logging.info(file + " already exists at destination.")
    else:
        logging.info("Copying " + file + " to destination")
        shutil.copy2(file, destpath)

       



if __name__ == "__main__":
    main()


