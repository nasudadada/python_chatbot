import os.path
from collections import defaultdict

import morph


class Dictionary:
    """思考エンジンの辞書クラス。

    クラス変数：
    DICT --

    プロパティ：
    random -- ランダム辞書
    pattern -- パターン辞書
    template -- テンプレート辞書
    """

    DICT = {'random': 'dics/random.txt',
            'pattern': 'dics/pattern.txt',
            'template': 'dics/template.txt',
            }

    def __init__(self):
        """ファイルから辞書の読み込みを行う。"""
        Dictionary.touch_dics()
        with open(Dictionary.DICT['random'], encoding='utf-8') as f:
            self._random = [x for x in f.read().splitlines() if x]

        with open(Dictionary.DICT['pattern'], encoding='utf-8') as f:
            self._pattern = [Dictionary.make_pattern(l) for l in f.read().splitlines() if f]

        with open(Dictionary.DICT['template'], encoding='utf-8') as f:
            self._template = defaultdict(lambda: [], {})
            for line in f:
                count, template = line.strip().split('\t')
                if count and template:
                    count = int(count)
                    self._template[count].append(template)

    @staticmethod
    def touch_dics():
        """辞書ファイルがなければ空のファイルを作成し、あれば何もしない。"""
        for dic in Dictionary.DICT.values():
            if not os.path.exists(dic):
                open(dic, 'w').close()

    @staticmethod
    def make_pattern(line):
        """文字列lineを\tで分割し、｛'pattern': [0], 'phrases': [1]｝の形式で返す。
        [1]は、さらに'|'で分割し、文字列のリストする。"""
        pattern, phrases = line.split('\t')
        if pattern and phrases:
            return {'pattern': pattern, 'phrases': phrases.split('|')}

    def study(self, text, parts):
        """ランダム辞書、パターン辞書をメモリに保存する。"""
        self.study_random(text)
        self.study_pattern(text, morph.analyze(text))
        self.study_template(parts)

    def study_random(self, text):
        """ユーザーの発言textをメモリに保存する。
        すでに同じ発言があった場合は何もしない。"""
        if not text in self._random:
            self._random.append(text)

    def study_pattern(self, text, parts):
        """ユーザーの発言textを、形態素partsに基づいてパターン辞書に保存する。"""
        for word, part in parts:
            if morph.is_keyword(part):
                duplicated = next((p for p in self._pattern if p['pattern'] == word), None)
                if duplicated:
                    if not text in duplicated['phrases']:
                        duplicated['phrases'].append(text)
                else:
                    self._pattern.append({'pattern': word, 'phrases': [text]})

    def study_template(self, parts):
        template = ''
        count = 0
        for word, part in parts:
            if morph.is_keyword(part):
                word = '%noun%'
                count += 1
            template += word

            if count > 0 and template not in self._template[count]:
                self._template[count].append(template)

    @staticmethod
    def pattern_to_line(pattern):
        """パターンのハッシュを文字列に変換する。"""
        return '{}\t{}'.format(pattern['pattern'], '|'.join(pattern['phrases']))

    def save(self):
        """メモリ上の辞書をファイルに保存する。"""
        with open(Dictionary.DICT['random'], mode='w') as f:
            f.write('\n'.join(self.random))

        with open(Dictionary.DICT['pattern'], mode='w', encoding='utf-8') as f:
            f.write('\n'.join([Dictionary.pattern_to_line(p) for p in self._pattern]))

        with open(Dictionary.DICT['template'], mode='w', encoding='utf-8') as f:
            for count, templates in self._template.items():
                for template in templates:
                    f.write('{}\t{}\n'.format(count, template))

    @property
    def random(self):
        """ランダム辞書"""
        return self._random

    @property
    def pattern(self):
        return self._pattern

    @property
    def template(self):
        """ テンプレート辞書"""
        return self._template
