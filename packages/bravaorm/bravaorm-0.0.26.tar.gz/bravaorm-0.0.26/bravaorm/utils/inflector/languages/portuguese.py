#!/usr/bin/env python

# Copyright (c) 2006 Bermi Ferrer Martinez
# bermi a-t bermilabs - com
#
# See the end of this file for the free software, open source license (BSD-style).

import re
from .base import Base

class Portuguese(Base):
    """
    Inflector for pluralize and singularize English nouns.

    This is the default Inflector for the Inflector obj
    """

    def pluralize(self, word) :
        '''Pluralizes English nouns.'''

        rules = [
            ['(?i)r$', 'res'],
            ['(?i)m$', 'ns'],
            ['(?i)il$', 'is'],
            ['(?i)l$', 'is'],
            ['(?i)(ao)$', 'oes'],
            ['(?i)([aeiou])$', '\\1s']
        ]


        uncountable_words = [
            'lapis',
            'onibus',
            'virus',
            'caridade',
            'bondade',
            'fe',
            'ouro',
            'prata',
            'bronze',
            'brisa',
            'oxigenio',
            'fome',
            'sede',
            'po',
            'plebe',
            'neve',
            'lenha',
            'cristianismo',
            'nazismo',
            'sinceridade',
            'lealdade',
            'status'
        ]

        irregular_words = {
            'bookmark': 'bookmarks',
            'direct': 'directs',
            'inbox': 'inboxes',
            'session': 'sessions',
            'fan': 'fans',
            'feed': 'feeds',
            'app':'apps',
            'server': 'servers',
            'mediaserver': 'mediaservers',
            'streamer': 'streamers',
            'mal': 'males',
            'consul': 'consules',
            'mel': 'meis',
            'cal': 'cais',
            'aval': 'avais',
            'mol': 'mois',
            'til': 'tis',
            'projetil': 'projeteis',
            'facil': 'faceis',
            'dificil': 'dificeis',
            'fossil': 'fosseis',
            'cep': 'ceps',
            'log': 'logs',
            'banner': 'banners',
            'faq': 'faqs',
            'newsletter': 'newsletters',
            'vip': 'vips',
            'deploy': 'deploys'
        }

        lower_cased_word = word.lower();

        for uncountable_word in uncountable_words:
            if lower_cased_word[-1*len(uncountable_word):] == uncountable_word :
                return word

        for irregular in irregular_words.keys():
            match = re.search('('+irregular+')$',word, re.IGNORECASE)
            if match:
                return re.sub('(?i)'+irregular+'$', match.expand('\\1')[0]+irregular_words[irregular][1:], word)

        for rule in range(len(rules)):
            match = re.search(rules[rule][0], word, re.IGNORECASE)
            if match :
                groups = match.groups()
                for k in range(0,len(groups)) :
                    if groups[k] == None :
                        rules[rule][1] = rules[rule][1].replace('\\'+str(k+1), '')

                return re.sub(rules[rule][0], rules[rule][1], word)

        return word


    def singularize_word(self, word) :
        '''Singularizes English nouns.'''

        rules = [
            ['((?i)ns)$', 'm'],
            ['((?i)[e][i]s)$', 'el'],
            ['(?i)(ais)$', 'al'],
            ['(?i)([i]s)$', 'il'],
            ['(?i)(oe)s$', 'ao'],
            ['(?i)(c)oes$', '\\1ao'],
            ['(?i)(r)es$', '\\1'],
            ['(?i)(z)es$', '\\1'],
            ['(?i)(s)es$', '\\1'],
            ['(?i)(le)ns$', '\\1n'],
            ['(?i)(de)ns$', '\\1n'],
            ['(?i)([aeou])is$', 'il'],
            ['(?i)([aeiou])s$', '\\1'],
            ['(?i)ns$', 'm'],
        ];

        uncountable_words = [
            'lapis',
            'onibus',
            'virus',
            'caridade',
            'bondade',
            'fe',
            'ouro',
            'prata',
            'bronze',
            'brisa',
            'oxigenio',
            'fome',
            'sede',
            'po',
            'plebe',
            'neve',
            'lenha',
            'cristianismo',
            'nazismo',
            'sinceridade',
            'lealdade',
            'status'
        ]

        irregular_words = {
            'bookmarks': 'bookmark',
            'directs': 'direct',
            'inboxes': 'inbox',
            'sessions': 'session',
            'fans': 'fan',
            'feeds': 'feed',
            'apps':'app',
            'servers': 'server',
            'mediaservers': 'mediaserver',
            'streamers': 'streamer',
            'males': 'mal',
            'consules': 'consul',
            'meis': 'mel',
            'cais': 'cal',
            'avais': 'aval',
            'mois': 'mol',
            'tis': 'til',
            'projeteis': 'projetil',
            'faceis': 'facil',
            'dificeis': 'dificil',
            'fosseis': 'fossil',
            'ceps': 'cep',
            'logs': 'log',
            'banners': 'banner',
            'faqs': 'faq',
            'newsletters': 'newsletter',
            'vips': 'vip',
            'deploys': 'deploy',
        }


        lower_cased_word = word.lower();

        for uncountable_word in uncountable_words:
            if lower_cased_word[-1*len(uncountable_word):] == uncountable_word :
                return word

        for irregular in irregular_words.keys():
            match = re.search('('+irregular+')$',word, re.IGNORECASE)
            if match:
                return re.sub('(?i)'+irregular+'$', match.expand('\\1')[0]+irregular_words[irregular][1:], word)


        for rule in range(len(rules)):
            match = re.search(rules[rule][0], word, re.IGNORECASE)
            if match :
                groups = match.groups()
                for k in range(0,len(groups)) :
                    if groups[k] == None :
                        rules[rule][1] = rules[rule][1].replace('\\'+str(k+1), '')

                return re.sub(rules[rule][0], rules[rule][1], word)

        return word

    def singularize(self, word):
        '''Singularizes each word'''
        words = word.split('_')
        words_done = []
        for word in words:
            words_done.append(self.singularize_word(word))
        return '_'.join(words_done)



# Copyright (c) 2006 Bermi Ferrer Martinez
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software to deal in this software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of this software, and to permit
# persons to whom this software is furnished to do so, subject to the following
# condition:
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THIS SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THIS SOFTWARE.
