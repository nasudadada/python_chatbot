from random import choice, randrange
from responder import RandomResponder, WhatResponder, PatternResponder
from dictionary import Dictionary


class Unmo:
    """人口無能コアクラス

    property
        name : 人口無能コアの名前
        repo : 現在の応答クラスの名前
    """

    def __init__(self, name):
        """ 文字列を受け取り、コアインスタンスの名前に設定する。
        'What' Responderインスタンスを作成し、保持する。
        Dictionaryインスタンスを作成し、保持する。
        """
        self._dictionary = Dictionary()

        self._responders = {
            'what': WhatResponder('What', self._dictionary),
            'random': RandomResponder('Random', self._dictionary),
            'pattern': PatternResponder('Pattern', self._dictionary)
        }
        self._name = name
        self._responder = self._responders['pattern']

    def dialogue(self, text):
        """ ユーザからの入力を受け取り、Responderに処理させた結果を返す。
        呼び出されるたびにランダムでResponderを切り替える。
        入力をDictionaryに学習させる。"""
        chance = randrange(0, 100)
        if chance in range(0, 59):
            self._responder = self._responders['pattern']
        elif chance in range(60, 89):
            self._responder = self._responders['random']
        else:
            self._responder = self._responders['what']

        response = self._responder.response(text)
        self._dictionary.study(text)
        return response

    def save(self):
        """Dictionaryへの保存を行う。"""
        self._dictionary.save()

    @property
    def name(self):
        """人口無能インスタンスの名前"""
        return self._name

    @property
    def responder_name(self):
        """保持しているResponderの名前 """
        return self._responder.name
