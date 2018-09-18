from responder import RandomResponder, WhatResponder
from random import choice


class Unmo:
    """人口無能コアクラス

    property
        name : 人口無能コアの名前
        repo : 現在の応答クラスの名前
    """

    def __init__(self, name):
        """ 文字列を受け取り、コアインスタンスの名前に設定する。
        'What' Responderインスタンスを作成し、保持する。
        """
        self._responders = {
            'what': WhatResponder('What'),
            'random': RandomResponder('Random'),
        }
        self._name = name
        self._responder = self._responders['random']

    def dialogue(self, text):
        """ ユーザからの入力を受け取り、Responderに処理させた結果を返す。
        呼び出されるたびにランダムでResponderに切り替える。"""
        chosen_key = choice(list(self._responders.keys()))
        self._responder = self._responders[chosen_key]
        return self._responder.response(text)

    @property
    def name(self):
        """人口無能インスタンスの名前"""
        return self._name

    @property
    def responder_name(self):
        """　保持しているResponderの名前 """
        return self._responder.name
