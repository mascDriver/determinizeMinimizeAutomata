# -*- coding: utf-8 -*-
import re
import string
from itertools import chain
from unicodedata import normalize

from tabulate import tabulate


def print_table(table, headers, title=None):
    if title:
        print(tabulate([title.upper()], tablefmt="fancy_grid"))
    print(tabulate(table, headers, tablefmt="fancy_grid"))


def prepare_alphabet_machine():
    formalize_data = [list(word) for word in words]
    return list(dict.fromkeys(list(chain.from_iterable(formalize_data))))


def formalize_data(file_name):
    ref_arquivo = open(file_name, "r")
    pattern = "<(?:\"[^\"]*\"['\"]*|'[^']*'['\"]*|[^'\">])+>"
    for linha in ref_arquivo:
        valores = normalize('NFKD', linha.strip()).encode('ASCII', 'ignore').decode('ASCII').lower()
        if valores.startswith('<s>'):
            tokens = valores.replace('::=', '').split('|')
            for token in tokens:
                words.append(re.sub(pattern, '', token).strip())
            continue
        elif valores.startswith('<'):
            continue
        words.append(valores)
    ref_arquivo.close()


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

    def deep_index(self, word):
        """
            Function return index list of list (0, 0) S[0][0]
        """

        return [(i, sub.index(word)) for (i, sub) in enumerate(self.states) if word in sub]

    def get_state(self, position=0, **kwargs):
        """
            Function return actual state by autoincrement 
        """
        return kwargs.get('state_final', '') + list(self.alphabet)[self.last_state - position]

    def create_state(self, new=True, state='', **kwargs):
        """
            Function thats create the state
            state: pre-defined(in case when determize) the new state
             is the state parameter passed in function,
            state_final: passed in kwargs, generally is the '*'
        """
        if new:
            if state:
                self.states = self.states + [
                    [kwargs.get('state_final', '') + state] + [''] * len(self.alphabet_machine)]
            else:
                self.states = self.states + [
                    [self.get_state(state_final=kwargs.get('state_final', ''))] + [''] * len(self.alphabet_machine)]
                self.last_state += 1

    def automata_n_deteminize(self):
        """
            Function get the data and generate the automata finite
        """
        for num_word, word in enumerate(words):
            len_word = len(word) - 1  # decrement 1 for compare in enumerate for
            for num_token, token in enumerate(word):
                if num_token == 0 and len_word:
                    # here is the first token in word or alphabet not in S
                    if num_word == 0:
                        # add in S the first token and create new state
                        self.states[0][self.alphabet_machine.index(token) + 1] += list(self.alphabet)[self.last_state]
                        self.create_state()
                    else:
                        # only add in S the token
                        self.states[0][self.alphabet_machine.index(token) + 1] += list(self.alphabet)[
                            self.last_state - 1]

                else:
                    if len_word == 0:
                        # alphabet in S
                        self.states[self.last_state][self.alphabet_machine.index(token) + 1] = list(self.alphabet)[
                            self.last_state - 1]
                        if not self.get_state(position=1, state_final='*') in chain(*self.states):
                            # if the state not be finally, change the finally
                            self.states[self.last_state][0] = '*' + self.states[self.last_state][0]
                        if num_token == 0:
                            # Add in S finally state for alphabetic in S
                            self.states[0][self.alphabet_machine.index(token) + 1] += list(self.alphabet)[
                                self.last_state - 1]
                    else:
                        if num_token == len_word:
                            # here the motive for -1, when be final token in word add state and create new state
                            self.states[self.last_state][self.alphabet_machine.index(token) + 1] = list(self.alphabet)[
                                self.last_state]
                            self.create_state(state_final='*')
                            try:
                                if len(words[num_word + 1]) == 1:
                                    self.create_state(new=False)
                            except IndexError:
                                continue
                            self.create_state()
                        else:
                            # the normal process, add state and create new state
                            self.states[self.last_state][self.alphabet_machine.index(token) + 1] = list(self.alphabet)[
                                self.last_state]
                            self.create_state()

    def determinize_automata(self):
        """
            Function thats determize automata
        """
        for state in self.states:
            for token in state:
                if not any(token in state[0] for state in self.states) and token:
                    state_final = False
                    # verify the token not have state, if not create the state but passed the name of state, btw the token
                    for token_new_state in token:
                        if any('*' + token_new_state in state[0] for state in self.states) and \
                                not any('*' + token in state[0] for state in self.states):
                            state_final = True
                    if state_final:
                        self.create_state(state=token, state_final='*')
                    else:
                        self.create_state(state=token)
                    indexes = self.deep_index(token)
                    # self.states[indexes[0][0]][indexes[0][1]] = f"[{self.states[indexes[0][0]][indexes[0][1]]}]"
                    self.states[indexes[0][0]][indexes[0][1]] = self.states[indexes[0][0]][indexes[0][1]]
                    for new_token in token:
                        # add states for new state
                        indexes_tokens = self.deep_index(new_token)
                        for key, valor in enumerate(self.states[indexes_tokens[-1][0]]):
                            if key == 0 or not valor:
                                # not subscribe the name of state
                                continue
                            self.states[-1][key] += valor

        for state in self.states:
            for token in state:
                # its ugly but here to be recursivity that function
                if not any(token in state[0] for state in self.states) and token:
                    self.determinize_automata()

    def create_state_error(self):
        """
            Maping blanks states and subscribe for state
        """
        self.create_state(state='<e>', state_final='*')
        for key_state, state in enumerate(self.states):
            for key_token, token in enumerate(state):
                if not token:
                    self.states[key_state][key_token] = '<e>'

    def compile(self):
        self.automata_n_deteminize()
        print_table(aut.states, [aut.delta] + aut.alphabet_machine, 'autômato não determinizado')
        self.determinize_automata()
        print_table(aut.states, [aut.delta] + aut.alphabet_machine, 'autômato determinizado')
        self.create_state_error()
        print_table(aut.states, [aut.delta] + aut.alphabet_machine, 'autômato com estado de erro')


# words = ['se', 'entao', 'senao', 'a', 'e', 'i', 'o', 'u']
words = []
while True:
    choice = input('Como você deseja adicionar gramaticas?\n1 - Manual\n2 - Arquivo\n')
    if choice == '1':
        command = input('Digite a palavra, para finalizar escreva "EOF": ')
        if command.lower() == 'eof':
            break
        else:
            words.append(normalize('NFKD', command).encode('ASCII', 'ignore').decode('ASCII').lower())
    elif choice == '2':
        file = input('Digite o nome do arquivo com a extensão: ')
        try:
            open(file, 'r')
            formalize_data(file)
            break
        except FileNotFoundError:
            print('Arquivo não encontrado, verifique o nome do arquivo\n')

aut = Automata(words=words)
aut.compile()
