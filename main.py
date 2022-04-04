# -*- coding: utf-8 -*-
import string
from itertools import chain

from tabulate import tabulate

from unicodedata import normalize


def print_table(table, headers):
    print(tabulate(table, headers, tablefmt="fancy_grid"))


def prepare_alphabet_machine():
    formalize_data = [list(word) for word in words]
    return list(dict.fromkeys(list(chain.from_iterable(formalize_data))))


class Automata:
    def __init__(self, words=[]):
        self.symbol_initial = 'S'
        self.delta = '\u03B4'
        self.epsilon = '\u03B5'
        self.alphabet = string.ascii_uppercase
        self.words = words
        self.alphabet_machine = prepare_alphabet_machine()
        self.states = [[self.symbol_initial] + [''] * len(self.alphabet_machine)]
        self.last_state = 0

    def deep_index(self, w):
        return [(i, sub.index(w)) for (i, sub) in enumerate(self.states) if w in sub]

    def get_state(self, position=0, **kwargs):
        return kwargs.get('state_final', '') + list(self.alphabet)[self.last_state - position]

    def create_state(self, new=True, state='', **kwargs):
        if new:
            if state:
                self.states = self.states + [
                    [kwargs.get('state_final', '') + state] + [''] * len(self.alphabet_machine)]
            else:
                self.states = self.states + [
                    [self.get_state(state_final=kwargs.get('state_final', ''))] + [''] * len(self.alphabet_machine)]
                self.last_state += 1

    def automata_n_deteminize(self):
        for num_word, word in enumerate(words):
            len_word = len(word) - 1
            for num_letter, letter in enumerate(word):
                if num_letter == 0 and len_word:
                    if num_word == 0:
                        self.states[0][self.alphabet_machine.index(letter) + 1] += list(self.alphabet)[self.last_state]
                        self.create_state()
                    else:
                        self.states[0][self.alphabet_machine.index(letter) + 1] += list(self.alphabet)[
                            self.last_state - 1]

                else:
                    if len_word == 0:
                        self.states[self.last_state][self.alphabet_machine.index(letter) + 1] = list(self.alphabet)[
                            self.last_state - 1]
                        if not self.get_state(position=1, state_final='*') in chain(*self.states):
                            self.states[self.last_state][0] = '*' + self.states[self.last_state][0]
                        if num_letter == 0:
                            self.states[0][self.alphabet_machine.index(letter) + 1] += list(self.alphabet)[
                                self.last_state - 1]
                    else:
                        if num_letter == len_word:
                            self.states[self.last_state][self.alphabet_machine.index(letter) + 1] = list(self.alphabet)[
                                self.last_state]
                            self.create_state(state_final='*')
                            try:
                                if len(words[num_word + 1]) == 1:
                                    self.create_state(new=False)
                            except IndexError:
                                continue
                            self.create_state()
                        else:
                            self.states[self.last_state][self.alphabet_machine.index(letter) + 1] = list(self.alphabet)[
                                self.last_state]
                            self.create_state()

    def determinize_automata(self):
        for state in self.states:
            for token in state:
                if not any(token in state[0] for state in self.states) and token:
                    self.create_state(state=token)
                    indexes = self.deep_index(token)
                    # self.states[indexes[0][0]][indexes[0][1]] = f"[{self.states[indexes[0][0]][indexes[0][1]]}]"
                    self.states[indexes[0][0]][indexes[0][1]] = self.states[indexes[0][0]][indexes[0][1]]
                    for letter in token:
                        indexes_letters = self.deep_index(letter)
                        for key, valor in enumerate(self.states[indexes_letters[-1][0]]):
                            if key == 0 or not valor:
                                continue
                            self.states[indexes[1][0]][key] += valor

        for state in self.states:
            for token in state:
                if not any(token in state[0] for state in self.states) and token:
                    self.determinize_automata()


# words = ['se', 'entao', 'senao', 'a', 'e', 'i', 'o', 'u']
words = []
while True:
    command = input('Digite a palavra, para finalizar escreva "EOF": ')
    if command.lower() == 'eof':
        break
    else:
        words.append(normalize('NFKD', command).encode('ASCII', 'ignore').decode('ASCII').lower())

aut = Automata(words=words)
aut.automata_n_deteminize()
print(tabulate(['autômato não Determizado'.upper()], tablefmt="fancy_grid"))
print_table(aut.states, [aut.delta] + aut.alphabet_machine)
aut.determinize_automata()
print(tabulate(['autômato Determizado'.upper()], tablefmt="fancy_grid"))
print_table(aut.states, [aut.delta] + aut.alphabet_machine)
