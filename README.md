# g-media-sorter
## How to use 

This script provides a g_media_sorter class that puts exported media from Google Photos into chronological order by renaming the file (see below for detailed description). If the class is not imported in another script, an instance can be created and used by following the steps below and running the commands in a Linux shell:

1) Edit the "config" dict in the script to suit your needs.
2) Run the following commands in a shell:
```
$ cd <location-of-images>
$ python3 <the-script>
```

## Class description

When photos and videos are exported from Google Photos (https://photos.google.com/) via Google Takeout (https://takeout.google.com/), a corresponding metadata file `<file-name>.<media-type>.json` is created for each media file `<file-name>.jpg`. This python class reads the creation time of a media file from this metadata and renames the media file to `<prefix>_<creation-time>'UTCp'<UTC-offset>_<running-number>.<media-type>`, where `<creation-time>` is formatted as `<year>-<month>-<day>_<hour>-<minutes>-<seconds>`. If configured, the metadata file is deleted afterwards.