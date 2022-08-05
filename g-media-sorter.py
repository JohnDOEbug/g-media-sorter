#!/bin/python3

logo = '\
  _____ __  __          _ _        _____            _             \n\
 / ____|  \/  |        | (_)      / ____|          | |            \n\
| |  __| \  / | ___  __| |_  __ _| (___   ___  _ __| |_ ___ _ __  \n\
| | |_ | |\/| |/ _ \/ _` | |/ _` |\___ \ / _ \| `__| __/ _ \ `__| \n\
| |__| | |  | |  __/ (_| | | (_| |____) | (_) | |  | ||  __/ |    \n\
 \_____|_|  |_|\___|\__,_|_|\__,_|_____/ \___/|_|   \__\___|_|    '

"""How to use this Script:

This script provides a g_media_sorter class that puts exported media from
Google Photos into chronological order by renaming the file (see below for
detailed description). If the class is not imported in another script, an
instance can be created and used by following the steps below and running
the commands in a Linux shell:

1) Edit the "config" dict below to suit your needs.
2) Run the following commands in a shell:
   $ cd <location-of-images>
   $ python3 <the-script>
"""

import os
import glob
import json
from datetime import datetime
from pytz import timezone

class g_media_sorter:
    """Python class for the sorting exported Media from Google Photos.

    When photos and videos are exported from Google Photos
    (https://photos.google.com/) via Google Takeout
    (https://takeout.google.com/), a corresponding metadata file
    <file-name>.<media-type>.json is created for each media file
    <file-name>.jpg. This python class reads the creation time of a media file
    from this metadata and renames the media file to
    <prefix>_<creation-time>'UTCp'<UTC-offset>_<running-number>.<media-type>,
    where <creation-time> is formatted as
    <year>-<month>-<day>_<hour>-<minutes>-<seconds>. If configured, the
    metadata file is deleted afterwards.
    """

    def __init__(self, config):
        """ Create instance of g_media_sorter.

        Parameters
        ----------
        config : dictionary
            Configuration for g_media_sorter.

            time_zone : string
                Local time zone.
                    get a list of valid strings:
                    for tz in pytz.all_timezones : print(tz)

            delete_json : boolean
                Delete the metadata file after processing.

            name_prefix : string
                Prefix of the new file name.
        """

        self.config = config

        print(logo)
        print(' ')
        print('Instance of g_media_sorter created. By github.com/JohnDOEbug')
        print(' ')
        print(' ')

    def process(self, dir):
        """Read metadata and rename media file.

        Parameters
        ----------
        dir : string
            Directory of the exported media files.
        """

        def time_formatter(time, time_zone):
            """Format a time.

            Parameters
            ----------
            time : date object
                A date.
            
            time_zone : string
                A Timezone.
                    get a list of valid strings:
                    for tz in pytz.all_timezones : print(tz)

            Returns
            -------
            string
                Formatted time.
            """
            time = time.astimezone(timezone(time_zone))
            time_format = time.strftime('%Y-%m-%d_%H-%M-%S') \
                + 'UTCp' + str(time.utcoffset().seconds // 3600)
            return time_format

        # All files
        for subdirs, dirs, files in os.walk(dir):
            for file in files:
                file_name = os.path.splitext(file)
                
                # Get all metadata files
                if file_name[1] == '.json':
                    metadata_file = os.path.join(subdirs, file)

                    renamed = False

                    # Read and convert Google metadata
                    creation_time = 'undef'
                    try:
                        with open(metadata_file, 'r') as meta_file:
                            metadata = json.load(meta_file)
                        creation_time = time_formatter(datetime.fromtimestamp(
                            int(metadata['photoTakenTime']['timestamp'])), \
                            self.config['time_zone'])
                        media_file_name = os.path.splitext(metadata['title'])
                    except:
                        pass

                    # Get all corresponding media files
                    media_files = glob.glob(
                        os.path.join(subdirs, media_file_name[0] + '*' + \
                        media_file_name[1])
                    )

                    for media_file in media_files: 

                        # Rename file
                        i = 0
                        new_file = os.path.join(subdirs, \
                            self.config['name_prefix'] + creation_time + '_' \
                            + str(i).zfill(3) + media_file_name[1])
                        while os.path.exists(new_file):
                            new_file = os.path.join(subdirs, \
                                self.config['name_prefix'] + creation_time \
                                + '_' + str(i).zfill(3) + media_file_name[1])
                            i += 1

                        if not creation_time == 'undef':
                            os.rename(media_file, new_file)
                            renamed = True
                            print(' Renaming: ' + media_file)
                            print('       to: ' + new_file)
                            print(' ')
                        else:
                            print('Excluding: ' + media_file)
                            print(' ')

                    # Delete metadata file if configured
                    if self.config['delete_json'] \
                    and not creation_time == 'undef' \
                    and renamed:
                        os.remove(metadata_file)
                        print(' Deleting: ' + metadata_file)
                        print(' ')

        print('Finished ...')

if __name__ == '__main__':
    config = {
        'time_zone': 'Europe/Berlin',
        'delete_json': True, 
        'name_prefix': 'Picture_'
    }
    dir=os.getcwd()

    sorter = g_media_sorter(config)
    sorter.process(dir)