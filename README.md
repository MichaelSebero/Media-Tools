<p align="center">
	<img src="https://i.postimg.cc/Hns6LNCz/document-tools.png" />

## How to Install

```
pip install matplotlib librosa audioread pydub futures mutagen pillow eyed3 tinytag moviepy

git clone https://github.com/MichaelSebero/Media-Tools

sh /home/$USER/Media-Tools/media-tools
```

## Compare Audio
This script compares two audio files using a spectrogram during the first 8 minutes or less.

<p align="left">
    <img src="https://i.postimg.cc/4dgNCq02/comparison.png" style="width:50%; height:auto;" />
</p>

## Convert to Opus
This script converts all audio files in a given directory to `.opus` in a seperate folder.

## Mass Crop Images
This script mass crops images to an output folder.

## Mass Thumbnail
This script adds thumbnails of the user's choice to `.mp3` and `.flac` files in a given directory.

## Sort by Album
This script organizes songs within a specified directory by creating folders named after their album metadata.

## Sort by Artist
This script organizes songs within a specified directory by creating folders named after their artist and album metadata, `sort-by-artist-r` does this recursively.

## Sort by Genre
This script organizes songs by their genre, artist and albums associated with the artist.

## View Metadata
The script `view-metadata` displays metadata associated with a specific media file and `view-metadata-all` shows all metadata of media files in a given directory.
