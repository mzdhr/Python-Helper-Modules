import json
import sqlite3
import ast
from peewee import *

db = SqliteDatabase('ksacountries.db')
cities_list_raw = []


class Cities(Model):
    city_id = CharField(unique=True)
    country = CharField()
    city_name = CharField()
    translated_city_name = CharField()
    lat = CharField()
    lon = CharField()

    class Meta:
        database = db


def open_file_and_loop(file):
    #i = 0
    with open(file, 'r') as t:
        for line in t:
            dict_data = ast.literal_eval(line)
            cities_list_raw.append(dict_data)


def add_city_to_database():
    for city in cities_list_raw:
        try:
            Cities.create(city_id=city['_id'],
                          country=city['country'],
                          city_name=city['name'],
                          translated_city_name='',
                          lat=city['coord']['lat'],
                          lon=city['coord']['lon'])
        except IntegrityError:
            city_data = Cities.save()


if __name__ == '__main__':
    db.connect()
    json_file = 'KSACountries.json'

    open_file_and_loop(json_file)
    print(cities_list_raw)
    db.create_tables([Cities], safe=True)
    add_city_to_database()
