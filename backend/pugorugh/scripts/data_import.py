import json
from os import environ
from os import path
import sys

import django


BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

PROJ_DIR = path.dirname(BASE_DIR)

sys.path.insert(0, PROJ_DIR)


def load_data():
    try:
        from pugorugh.serializers import DogSerializer
    except ImportError:
        raise ImportError(
            'serializers.py must contain a properly '
            'implemented DogSerializer class for this import to work.'
        )

    filepath = path.join(PROJ_DIR, 'pugorugh', 'static', 'dog_details.json')

    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
        itera = 1
        for item in data:
            try:
                print(str(itera) + ': ' + item['breed'])
            except KeyError:
                item['breed'] = 'Unknown Mix'
                print(str(itera) + ': ' + item['breed'])
            itera += 1

        serializer = DogSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            print('load_data done.')
        else:
            print(serializer.errors)
            print('load_data unsuccessful.')


if __name__ == '__main__':
    # sys.path.append(PROJ_DIR) ##### MIGHT HAVE TO KEEP THIS FOR DJANGO 2+
    environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    django.setup()
    load_data()
