I created these scripts because, after running Nextcloud for almost 6 years, I realized that the only feature that I really used was the media backup on my Android phone. I recently updated my home setup, and decided to not setup Nextcloud this time. To keep functionality with my home server, I decided to use Syncthing, as I was already using this for other needs. I have it set up to sync my phone's media to a folder on the server. Then, as a daily cron job, this code is run to sort it into the proper folders.

Usage: The code is expecting two arguments. The argument with the -p or --path flag should be the path to the folder you want to sort the media files from. The second command with the -dp or --destinationpath flags should be the root destination path, ignoring the year and month folders. When this code is run, it will search for all picture files, non recursively. It will then create the year and month folders in the target directory, if not yet present. Then, it will copy the files to the respective folders and move the original file to a newly created "completed" folder. The sorting is done through the exif data of the image, and it is pulled using the Pillow module. Conversely, for video, it is pulled using ffmpeg through the ffmpeg-python module. If there is no exif data for date in the picture, it will sort it by the current date, as it is assumed that this is a daily task. The log will be written and appended to in the folder that the sorting is occurring. If your path has spaces, please encapsulate them within quotes. See sample command below.

python3 ./photobackup.py --path /starting --destinationpath /destination

or

python3 ./videopbackup.py -p "/starting path" -dp "/destination path"

Testing so far has only been on Linux systems, though I have some provisions on path type for Windows devices. I intend to test this in the future. Further, I have only had the chance to test with MP4 files. I am in the process of testing with other video formats that are already listed in the tuple within the code to sort by.

Required: FFMPEG installed on the local system and a pip install of the requirements.txt file.