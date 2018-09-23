import re
from janome.tokenizer import Tokenizer


class Dictionary:
    """思考エンジンの辞書クラス。

    クラス変数：
    DICT_RANDOM -- ランダム辞書のファイル名
    DICT_PATTERN -- パターン辞書のファイル名

    プロパティ：
    random -- ランダム辞書
    pattern -- パターン辞書
    """

    DICT_RANDOM = 'dics/random.txt'
    DICT_PATTERN = 'dics/pattern.txt'

    TOKENIZER = Tokenizer()

    def __init__(self):
        """ファイルから辞書の読み込みを行う。"""
        with open(Dictionary.DICT_RANDOM, encoding='utf-8') as f:
            self._random = [x for x in f.read().splitlines() if x]

        self._pattern = []
        with open(Dictionary.DICT_PATTERN, encoding='utf-8') as f:
            self._pattern = [Dictionary.make_pattern(l) for l in f.read().splitlines() if f]

    @staticmethod
    def make_pattern(line):
        """文字列lineを\tで分割し、｛'pattern': [0], 'phrases': [1]｝の形式で返す。
        [1]は、さらに'|'で分割し、文字列のリストする。"""
        pattern, phrases = line.split('\t')
        if pattern and phrases:
            return {'pattern': pattern, 'phrases': phrases.split('|')}

    def study(self, text):
        """ランダム辞書、パターン辞書をメモリに保存する。"""
        self.study_random(text)
        self.study_pattern(text, Dictionary.analyze(text))

    def study_random(self, text):
        """ユーザーの発言textをメモリに保存する。
        すでに同じ発言があった場合は何もしない。"""
        if not text in self._random:
            self._random.append(text)

    def study_pattern(self, text, parts):
        """ユーザーの発言textを、形態素partsに基づいてパターン辞書に保存する。"""
        for word, part in parts:
            if self.is_keyword(part):
                duplicated = next((p for p in self._pattern if p['pattern'] == word), None)
                if duplicated:
                    if not text in duplicated['phrases']:
                        duplicated['phrases'].append(text)
                else:
                    self._pattern.append({'pattern': word, 'phrases': [text]})

    @staticmethod
    def analyze(text):
        """文字列textを形態素解析し、[(surface, parts)]の形にして返す。"""
        return [(t.surface, t.part_of_speech) for t in Dictionary.TOKENIZER.tokenize(text)]

    @staticmethod
    def pattern_to_line(pattern):
        """パターンのハッシュを文字列に変換する。"""
        return '{}\t{}'.format(pattern['pattern'], '|'.join(pattern['phrases']))

    @staticmethod
    def is_keyword(part):
        """品詞partが学習すべきーワードであるかどうかを真偽値で返す。"""
        return bool(re.match(r'名詞,(一般|代名詞|固有名詞|サ変接続|形容動詞語幹)', part))

    def save(self):
        """メモリ上の辞書をファイルに保存する。"""
        with open(Dictionary.DICT_RANDOM, mode='w') as f:
            f.write('\n'.join(self.random))

    @property
    def random(self):
        """ランダム辞書"""
        return self._random

    @property
    def pattern(self):
        return self._pattern
