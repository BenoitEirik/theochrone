#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module contains the Martyrology class"""


import calendar
import collections
import fuzzywuzzy.fuzz as fuzz
import humandate
import os
import pickle

TextResult = collections.namedtuple("TextResult",("title","main","last_sentence"))
TextRatio = collections.namedtuple("TextRatio",("month","day",'ratio'))

class Martyrology:
    """The Roman Martyrology.
    This class can only contain one edition (by date)
    of the martyrology, with its different translations"""
    _first_line = {'fr':"Le {} {}",
                   'la':"Die {}. {}"
            } # a dict of the pattern for the first line
    _last_line = {
        'fr':"V. Et ailleurs, beaucoup d'autres saints martyrs, confesseurs et saintes vierges. Chœur. R. Rendons grâces à Dieu.",
        'la':"V. Et álibi aliórum plurimórum sanctórum Mártyrum et Confessórum, atque sanctárum Vírginum. Chorus. R. Deo grátias. ",
            } # a dict of the last lines

    def __init__(self,date=1962):
        """Inits the class.
        date is the edition selected.
        Loads names of files"""
        pattern = "roman_martyrology_{}.pkl".format(date)
        files_list = [file for file in os.listdir('data') if pattern in file]
        self._data = { 
                file.split('_')[0] : 'data/' + file
                for file in files_list} 

    def daytext(self,date,language):
        """date is a datetime.date like object.
        Return text for requested day and locale"""
        i = date.day
        if date.month == 2 and date.day >= 25 and calendar.isleap(date.year): # leap years : 25, 26, 27, 28 & 29 of February
            i -=1
        base = self._get_data(language)['data'][date.month-1][i-1]
        
        if date.month == 11 and ((date.day == 2 and date.isoweekday() != 7) or (date.day == 3 and date.isoweekday() == 1)):
            base = self._get_data(language)['faithful_departed'] + base
        day_formatted = humandate.main(language,date.day,'day')
        first_line = self._first_line[language].format(day_formatted,humandate.months[language][date.month])
        return TextResult(first_line,
                          base,
                self._last_line[language])

    def _get_data(self,language):
        """Loads data if necessary.
        Return self._data[language]"""
        if isinstance(self._data[language],str):
            with open(self._data[language],'br') as f:
                self._data[language] = pickle.Unpickler(f).load()
        return self._data[language] # _data = {lang:{credits:str,data:[month:[day,day...]]}}

    def credits(self,language):
        """Return appropriate credits for
        requested language"""
        return self._get_data(language)['credits']
    
    def find(self,tokens,lang,max_nb_returned=5):
        """Look into the texts and returned
        a list of the texts matching best with tokens entered. Best first.
        Items of the list are TextResult objects.
        tokens = a string with keywords
        lang = a string definining which language should be use.
        max_nb_returned = an int which specifies the max number
        of results returned"""
        results = []
        sort_function = (fuzz.partial_token_sort_ratio,fuzz.partial_ratio)[len(tokens.split()) == 1]
        for i,month in enumerate(self._get_data(lang)['data']):
            for j,day in enumerate(month):
                day = ' '.join(day)
                results.append(TextRatio(i,j,sort_function(tokens,day)))
        results.sort(key=lambda item:item.ratio,reverse=True)
        return results[:max_nb_returned] # TODO à finir : renvoyer les textes eux-mêmes

