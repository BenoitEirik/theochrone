#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module contains the Martyrology class"""


import calendar
import collections
import datetime
import matcher
import humandate
import os
import pickle
import phlog

logger = phlog.loggers['console']

file_path = os.path.dirname(os.path.abspath(__file__)) + '/'

TextResult = collections.namedtuple("TextResult",("title","main","last_sentence",'matching_line'))
TextRatio = collections.namedtuple("TextRatio",("month","day","matching_line",'ratio'))

class Martyrology:
    """The Roman Martyrology.
    This class can only contain one edition (by date)
    of the martyrology, with its different translations"""
    _first_line = {'fr':"Le {} {}",
                   'la':"Die {}. {}",
                   'en':"On {1} {0}",
            } # a dict of the pattern for the first line
    _last_line = {
        'fr':"V. Et ailleurs, beaucoup d'autres saints martyrs, confesseurs et saintes vierges. Chœur. R. Rendons grâces à Dieu.",
        'la':"V. Et álibi aliórum plurimórum sanctórum Mártyrum et Confessórum, atque sanctárum Vírginum. Chorus. R. Deo grátias. ",
        'en':"V. And elsewhere in divers places, many other holy martyrs, confessors, and holy virgins. R. Thanks be to God.",
            } # a dict of the last lines
    name = {
        'fr':'Martyrologe Romain',
        'la':'Romanum Martyrologium',
        'en':'Roman Martyrology',
        }

    def __init__(self,date=1962): # TEST
        """Inits the class.
        date is the edition selected.
        Loads names of files"""
        data_path = file_path + 'data/'
        pattern = "roman_martyrology_{}.pkl".format(date)
        files_list = [file for file in os.listdir(data_path) if pattern in file]
        self._data = { 
                file.split('_')[0] : data_path + file
                for file in files_list} 

    def daytext(self,date,language,matching_line=None): # TEST
        """date is a datetime.date like object.
        Return text for requested day and locale
        matching_line is needed if kw called daytext"""
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
                self._last_line[language],
                matching_line)

    def _get_data(self,language): # TEST
        """Loads data if necessary.
        Return self._data[language]"""
        if isinstance(self._data[language],str):
            with open(self._data[language],'br') as f:
                self._data[language] = pickle.Unpickler(f).load()
        return self._data[language] # _data = {lang:{credits:str,data:[month:[day,day...]]}}

    def credits(self,language): # TEST
        """Return appropriate credits for
        requested language"""
        return self._get_data(language)['credits']
    
    def _raw_kw(self,tokens,lang,max_nb_returned=-1,min_ratio=0): # TEST
        """Look into the texts and returned
        a list of indices of the texts matching best with tokens entered.
        Best first.
        tokens = a list of keywords
        lang = a string definining which language should be use.
        max_nb_returned = an int which specifies the max number
        of results returned. -1 = all
        min_ratio = an int or a float which specifies the minimum ratio
        of results returned. 0 = all
        """
        results = []
        token_matcher = matcher.Matcher(tokens,lang)
        for i, month in enumerate(self._get_data(lang)['data']):
            for j, day in enumerate(month):
                day = [line.lower() for line in day]
                day_ratio = 0
                for k,line in enumerate(day):
                    line_ratio = token_matcher.fuzzer(line)
                    if line_ratio > day_ratio:
                        day_ratio = line_ratio
                        matching_line = k
                results.append(TextRatio(i+1,j+1,matching_line,day_ratio))
        results.sort(key=lambda item:item.ratio,reverse=True)
        if token_matcher.is_score_low():
            if token_matcher.splitter():
                results = self._raw_kw(token_matcher.tokens,lang,max_nb_returned,min_ratio)
        results = [result for result in results if result.ratio >= min_ratio]
        return results if max_nb_returned == -1 else results[:max_nb_returned]
    
    def kw(self,tokens,lang,max_nb_returned = -1,min_ratio = .80,year = datetime.date.today().year):# TEST # WARNING commemoration of faithful_departed can not be find by this way
    # BUG rechercher un mot-clef le jour de la commémoration des fidèles défunts pose un problème dans le nombre de lignes... Il faut trouver un autre système.
        """Wrapper of self._raw_kw. Return a list of the texts
        Items of the list are TextResult objects including index of matching line.
        year is an int"""
        results = self._raw_kw(tokens,lang,max_nb_returned,min_ratio)
        return [ self.daytext(datetime.date(year,item.month,item.day),lang,item.matching_line) for item in results ]
        

