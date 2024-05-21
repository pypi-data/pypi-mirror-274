#!/usr/bin/env python
# -*- coding: latin-1 -*-
# Copyright (c) 2006 Bermi Ferrer Martinez
# Copyright (c) 2006 Carles Sadurn� Anguita
#
# bermi a - t bermilabs - com
#
# See the end of this file for the free software, open source license (BSD - style).

import re
from .base import Base

class Spanish(Base):
    '''
    Inflector for pluralize and singularize Spanish nouns.
    '''

    def pluralize(self, word):
        '''Pluralizes Spanish nouns.'''
        rules = [
            [r'(?i)([aeiou])x$', r'\1x'],  # This could fail if the word is oxytone.
            [r'(?i)([�����])([ns])$', r'|1\2es'],
            [r'(?i)(^[bcdfghjklmn�pqrstvwxyz]*)an$', r'\1anes'],  # clan - >clanes
            [r'(?i)([�����])s$', r'|1ses'],
            [r'(?i)(^[bcdfghjklmn�pqrstvwxyz]*)([aeiou])([ns])$', r'\1\2\3es'],  # tren - >trenes
            [r'(?i)([aeiou���])$', r'\1s'],  # casa - >casas, padre - >padres, pap� - >pap�s
            [r'(?i)([aeiou])s$', r'\1s'],  # atlas - >atlas, virus - >virus, etc.
            [r'(?i)([��])(s)$', r'|1\2es'],  # ingl�s - >ingleses
            [r'(?i)z$', 'ces'],  # luz - >luces
            [r'(?i)([��])$', r'\1es'],  # ceut� - >ceut�es, tab� - >tab�es
            [r'(?i)(ng|[wckgtp])$', r'\1s'],  # Anglicismos como puenting, frac, crack, show (En que casos podr�a fallar esto?)
            [r'(?i)$', 'es']	 # ELSE +es (v.g. �rbol - >�rboles)
        ]

        uncountable_words = ['tijeras', 'gafas', 'vacaciones', 'v�veres', 'd�ficit']
        ''' In fact these words have no singular form: you cannot say neither
        "una gafa" nor "un v�vere". So we should change the variable name to
        onlyplural or something alike.'''

        irregular_words = {
            'pa�s': 'pa�ses',
            'champ�': 'champ�s',
            'jersey': 'jers�is',
            'car�cter': 'caracteres',
            'esp�cimen': 'espec�menes',
            'men�': 'men�s',
            'r�gimen': 'reg�menes',
            'curriculum': 'curr�culos',
            'ultim�tum': 'ultimatos',
            'memor�ndum': 'memorandos',
            'refer�ndum': 'referendos'
        }

        lower_cased_word = word.lower()

        for uncountable_word in uncountable_words:
            if lower_cased_word[- 1 * len(uncountable_word):] == uncountable_word:
                return word

        for irregular in irregular_words.keys():
            match = re.search('(?i)(' + irregular + ')$', word, re.IGNORECASE)
            if match:
                return re.sub('(?i)' + irregular + '$', match.expand('\\1')[0] + irregular_words[irregular][1:], word)

        for rule in range(len(rules)):
            match = re.search(rules[rule][0], word, re.IGNORECASE)

            if match:
                groups = match.groups()
                replacement = rules[rule][1]
                if re.match('\|', replacement):
                    for k in range(1, len(groups)):
                        replacement = replacement.replace('|' + str(k), self.string_replace(groups[k - 1], '����������', 'AEIOUaeiou'))

                result = re.sub(rules[rule][0], replacement, word)
                # Esto acentua los sustantivos que al pluralizarse se convierten en esdr�julos como esm�quines, j�venes...
                match = re.search('(?i)([aeiou]).{1, 3}([aeiou])nes$', result)

                if match and len(match.groups()) > 1 and not re.search('(?i)[�����]', word):
                    result = result.replace(match.group(0), self.string_replace(match.group(1), 'AEIOUaeiou', '����������') + match.group(0)[1:])

                return result

        return word

    def singularize(self, word):
        '''Singularizes Spanish nouns.'''

        rules = [
            ['(?i)^([bcdfghjklmn�pqrstvwxyz]*)([aeiou])([ns])es$', '\\1\\2\\3'],
            ['(?i)([aeiou])([ns])es$',  '~1\\2'],
            ['(?i)oides$',  'oide'],  # androides - >androide
            ['(?i)(ces)$/i', 'z'],
            ['(?i)(sis|tis|xis) + $',  '\\1'],  # crisis, apendicitis, praxis
            ['(?i)(�)s$',  '\\1'],  # beb�s - >beb�
            ['(?i)([^e])s$',  '\\1'],  # casas - >casa
            ['(?i)([bcdfghjklmn�prstvwxyz]{2, }e)s$', '\\1'],  # cofres - >cofre
            ['(?i)([gh�pv]e)s$', '\\1'],  # 24 - 01 llaves - >llave
            ['(?i)es$', '']  # ELSE remove _es_  monitores - >monitor
        ]

        uncountable_words = ['paraguas', 'tijeras', 'gafas', 'vacaciones', 'v�veres', 'lunes', 'martes', 'mi�rcoles', 'jueves', 'viernes', 'cumplea�os', 'virus', 'atlas', 'sms']

        irregular_words = {
            'jersey': 'jers�is',
            'esp�cimen': 'espec�menes',
            'car�cter': 'caracteres',
            'r�gimen': 'reg�menes',
            'men�': 'men�s',
            'r�gimen': 'reg�menes',
            'curriculum': 'curr�culos',
            'ultim�tum': 'ultimatos',
            'memor�ndum': 'memorandos',
            'refer�ndum': 'referendos',
            's�ndwich': 's�ndwiches'
        }

        lower_cased_word = word.lower()

        for uncountable_word in uncountable_words:
            if lower_cased_word[-1 * len(uncountable_word):] == uncountable_word:
                return word

        for irregular in irregular_words.keys():
            match = re.search('(' + irregular + ')$', word, re.IGNORECASE)
            if match:
                return re.sub('(?i)' + irregular + '$', match.expand('\\1')[0] + irregular_words[irregular][1:], word)

        for rule in range(len(rules)):
            match = re.search(rules[rule][0], word, re.IGNORECASE)
            if match:
                groups = match.groups()
                replacement = rules[rule][1]
                if re.match('~', replacement):
                    for k in range(1, len(groups)):
                        replacement = replacement.replace('~' + str(k), self.string_replace(groups[k - 1], 'AEIOUaeiou', '����������'))

                result = re.sub(rules[rule][0], replacement, word)
                # Esta es una posible soluci�n para el problema de dobles acentos. Un poco guarrillo pero funciona
                match = re.search('(?i)([�����]).*([�����])', result)

                if match and len(match.groups()) > 1 and not re.search('(?i)[�����]', word):
                    result = self.string_replace(result, '����������', 'AEIOUaeiou')

                return result

        return word


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
