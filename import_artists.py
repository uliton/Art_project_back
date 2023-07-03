import pandas as pd
from pip._vendor import chardet

from gallery_app.models import Artist


def import_artists_from_csv(file_path):
    with open(file_path, 'rb') as csv_file:
        result = chardet.detect(csv_file.read())
        encoding = result['encoding']

    df = pd.read_csv(file_path, encoding=encoding)

    for _, row in df.iterrows():
        artist = Artist(
            fullname=row['fullname'],
            location=row['location'],
            bio=row['bio'],
            categories=row['categories'],
            phone=row['phone']
        )
        image = row['image']
        artist.image.save(image.split('/')[-1], open(image, 'rb'), save=True)
        artist.save()
