import os
import mimetypes
import eyed3
from mutagen import File as MutagenFile
from mutagen.flac import Picture as FlacPicture

def add_thumbnail_to_songs(directory_path, thumbnail_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if is_audio_file(file):
                song_path = os.path.join(root, file)
                add_thumbnail(song_path, thumbnail_path)

def is_audio_file(file):
    mime, _ = mimetypes.guess_type(file)
    return mime and mime.startswith('audio')

def select_thumbnail():
    thumbnail_path = input("Enter the path of the thumbnail image: ")
    while not os.path.isfile(thumbnail_path) or not thumbnail_path.lower().endswith(('.jpg', '.jpeg', '.png')):
        print("Invalid file. Please enter a valid path to a JPEG or PNG image.")
        thumbnail_path = input("Enter the path of the thumbnail image: ")
    return thumbnail_path

def add_thumbnail(song_path, thumbnail_path):
    if song_path.lower().endswith('.mp3') or song_path.lower().endswith('.m4a'):
        add_mp3_m4a_thumbnail(song_path, thumbnail_path)
    elif song_path.lower().endswith('.flac'):
        add_flac_thumbnail(song_path, thumbnail_path)

def add_mp3_m4a_thumbnail(song_path, thumbnail_path):
    audiofile = eyed3.load(song_path)

    if audiofile is not None:
        if audiofile.tag is None:
            audiofile.initTag()

        audiofile.tag.images.set(3, open(thumbnail_path, 'rb').read(), 'image/jpeg')
        audiofile.tag.save()

def add_flac_thumbnail(song_path, thumbnail_path):
    audiofile = MutagenFile(song_path)

    if audiofile is not None:
        if 'APIC:' in audiofile.tags:
            del audiofile.tags['APIC:']

        image_data = open(thumbnail_path, 'rb').read()
        picture = FlacPicture()
        picture.type = 3  # Cover (front) image
        picture.mime = 'image/jpeg'
        picture.desc = u'Cover'
        picture.data = image_data

        audiofile.add_picture(picture)
        audiofile.save()

if __name__ == "__main__":
    songs_directory = input("Enter the directory containing audio files: ")
    thumbnail_path = select_thumbnail()

    add_thumbnail_to_songs(songs_directory, thumbnail_path)
    print("Thumbnails added to audio files successfully.")
