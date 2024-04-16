I created this script because, after running Nextcloud for almost 6 years, I realized that the only feature that I really used was the media backup on my Android phone. I recently updated my home setup, and decided to not setup Nextcloud this time. To keep functionality with my home server, I decided to use Syncthing, as I was already using this for other needs. I have it set up to sync my phone's media to a folder on the server. Then, as a daily cron job, this code is run to sort it into the proper folders.

Usage: The code is expecting two arguments. The argument with the -p or --path flag should be the path to the folder you want to sort the media files from. The second command with the -dp or --destinationpath flags should be the root destination path, ignoring the year and month folders. When this code is run, it will search for all picture files, non recursively. It will then create the year and month folders in the target directory, if not yet present. Then, it will copy the files to the respective folders and move the original file to a newly created "completed" folder. The sorting is done through the exif data of the folder, and it is pulled using the Pillow module. This will need to be installed on the device prior to running. If there is no exif data for date in the picture, it will sort it by the current date, as it is assumed that this is a daily task. The log will be written and appended to in the folder that the sorting is occurring. If your path has spaces, please encapsulate them within quotes. See sample command below.

python3 ./photobackup.py --path /starting --destinationpath /destination

or

python3 ./photopbackup.py -p "/starting path" -dp "/destination path"

Future updates will include metadata sorting for video files. I currently intend to keep that as a second script, but will include that in this repo. The reason for this is simply that I use different folder for my photos and videos, and I do not want to provide four paths.