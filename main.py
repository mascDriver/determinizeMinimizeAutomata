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
        self.state = [[self.symbol_initial] + [''] * len(self.alphabet_machine)]
        self.last_state = 0

    def get_state(self, position=0, **kwargs):
        return kwargs.get('state_final', '') + list(self.alphabet)[self.last_state - position]

    def create_state(self, new=True, **kwargs):
        if new:
            self.state = self.state + [[self.get_state(state_final=kwargs.get('state_final', ''))] + [''] * len(self.alphabet_machine)]
            self.last_state += 1

    def automata_n_deteminize(self):
        for num_word, word in enumerate(words):
            len_word = len(word) - 1
            for num_letter, letter in enumerate(word):
                if num_letter == 0 and len_word:
                    if num_word == 0:
                        self.state[0][self.alphabet_machine.index(letter) + 1] += list(self.alphabet)[self.last_state]
                        self.create_state()
                    else:
                        self.state[0][self.alphabet_machine.index(letter) + 1] += list(self.alphabet)[self.last_state-1]

                else:
                    if len_word == 0:
                        self.state[self.last_state][self.alphabet_machine.index(letter) + 1] = list(self.alphabet)[
                            self.last_state - 1]
                        if not self.get_state(position=1, state_final='*') in chain(*self.state):
                            self.state[self.last_state][0] = '*' + self.state[self.last_state][0]
                        if num_letter == 0:
                            self.state[0][self.alphabet_machine.index(letter) + 1] += list(self.alphabet)[
                                self.last_state - 1]
                    else:
                        if num_letter == len_word:
                            self.state[self.last_state][self.alphabet_machine.index(letter) + 1] = list(self.alphabet)[
                                self.last_state]
                            self.create_state(state_final='*')
                            try:
                                if len(words[num_word + 1]) == 1:
                                    self.create_state(new=False)
                            except IndexError:
                                continue
                            self.create_state()
                        else:
                            self.state[self.last_state][self.alphabet_machine.index(letter) + 1] = list(self.alphabet)[
                                self.last_state]
                            self.create_state()


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
print_table(aut.state, [aut.delta] + aut.alphabet_machine)
