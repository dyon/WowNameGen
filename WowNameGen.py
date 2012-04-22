#
# WowNameGen
# Author: Dyon
# This tool generates random World of Warcraft character names.

import ConfigParser
import sys
import csv
from random import choice


class WowNameGen:

    __race_names = []
    __races = {}
    __file = 'names.csv'
    __delimiter = ','

    def __init__(self):
        if not self.read_config():
            sys.exit()

    def read_config(self):
        try:
            config = ConfigParser.RawConfigParser()

            config.read('config.cfg')

            # Get race names and key-value pairs
            for race in config.items('Races'):
                self.__race_names.append([race[1], race[0]])
                self.__races[race[1]] = race[0]

            # Get source file name
            self.__file = config.get('General', 'NamesFile')

            # Get csv delimiter
            self.__delimiter = self.get_delimiter_char(config.get('General', 'Delimiter'))

            return True
        except:
            print 'Error while trying to read the configuration file.'

        return False

    def get_delimiter_char(self, delimiter_name):
        delimiter_chars = {
            'comma': ',',
            'tab': '\t',
            'space': ' '
        }

        if delimiter_name in delimiter_chars:
            return delimiter_chars[delimiter_name]
        else:
            print 'Invalid delimiter name supplied, using the default (comma).'

            return ','

    def get_race_name(self, index):
        if index < len(self.__race_names):
            return self.__race_names[index][1].title()
        else:
            return None

    def get_race_name_by_id(self, race_id):
        if str(race_id) in self.__races:
            return self.__races[str(race_id)].title()
        else:
            return None

    def get_race_id_from_index(self, index):
        if index < len(self.__race_names):
            return self.__race_names[index][0].title()
        else:
            return None

    def get_gender_name_by_id(self, gender_id):
        genders = ['Male', 'Female']

        if self.gender_index_is_valid(gender_id):
            return genders[gender_id]
        else:
            return 'Unknown'

    def race_index_is_valid(self, index):
        if index >= 0 and index < len(self.__race_names):
            return True
        else:
            return False

    def gender_index_is_valid(self, index):
        if index >= 0 and index <= 1:
            return True
        else:
            return False

    def load_names(self, race_id, gender_id):
        names = []

        with open(self.__file, 'rb') as file:
            reader = csv.reader(file, delimiter=self.__delimiter)

            for row in reader:
                # Filter by race id and gender id
                if row[2] == str(race_id) and row[3] == str(gender_id):
                    names.append(row)

        return names

    def pick_random_name(self, race_id, gender_id):
        return choice(self.load_names(race_id, gender_id))[1]

    def display_race_list_by_index(self):
        index = 1

        for race in self.__race_names:
            print '    ' + str(index) + '. ' + race[1].title()

            index += 1

    def generate_random_name(self):
        race = 0
        gender = 0

        print 'World of Warcraft random character name generator.'
        print
        print 'Pick a race:'
        self.display_race_list_by_index()

        while True:
            race = raw_input('--> ')

            if race.isdigit() and self.race_index_is_valid(int(race) - 1):
                race = int(race) - 1
                break

        print 'Pick a gender:'
        print '    1. Male'
        print '    2. Female'

        while True:
            gender = raw_input('--> ')

            if gender.isdigit() and self.gender_index_is_valid(int(gender) - 1):
                gender = int(gender) - 1
                break

        print 'Your generated name for a ' + self.get_race_name(race) + ' ' + self.get_gender_name_by_id(gender) + ': ' + self.pick_random_name(self.get_race_id_from_index(race), gender)


wng = WowNameGen()

wng.generate_random_name()
