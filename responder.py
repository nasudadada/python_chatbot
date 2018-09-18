from random import choice


class Responder:
    """AIの応答を制御するクラス。

    args:
        name : responderオブジェクトの名前
    """

    def __init__(self, name):
        """ 文字列を受け取り、自身のnameに設定する。 """
        self._name = name

    def response(self, *args):
        """ 文字列を受け取り、思考した結果を返す。 """
        pass

    @property
    def name(self):
        """ 応答オブジェクトの名前 """
        return self._name


class WhatResponder(Responder):
    """AIの応用を制御する思考エンジンクラス
    入力に対して疑問形で聞き返す。"""

    def response(self, text):
        """文字列textを受け取り、'{text}ってなに？'という形式で返す。"""
        return '{}ってなに？'.format(text)


class RandomResponder(Responder):
    """AIの応答を制御する思考エンジンクラス。
    登録された文字列からランダムなものを返す。

    クラス変数：
    RESPONSES：応答する文字列のリスト

    プロパティ：RandomResponderオブジェクトの名前
    """

    def __init__(self, name):
        """文字列nameを受け取りオブジェクトの名前を設定する。
        'dics/random.txt'ファイルから応答文字列のリストを読み込む。"""
        super().__init__(name)
        self._responses = []
        with open('dics/random.txt', mode='r', encoding='utf-8') as f:
            self._responses = [x for x in f.read().splitlines() if x]

    def response(self, _):
        """ユーザからの入力は受け取るが、使用せずにランダムな応答を返す。"""
        return choice(self._responses)
