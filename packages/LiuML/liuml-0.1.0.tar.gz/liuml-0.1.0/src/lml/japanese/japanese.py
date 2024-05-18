#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
from enum import Enum

from sudachipy.dictionary import Dictionary

SUDACHI_DICT = Dictionary().create()


class RE_JAPANESE:  # noqa
    KATAKANA = re.compile("^[ァ-ヾ]+$")
    HIRAGANA = re.compile("^[ぁ-ゞ]+$")
    HALF_KATAKANA = re.compile("^[ｦ-ﾟ]+$")
    KANJI = re.compile(r"^[\u4E00-\u9FA5]+$")
    KANA_AND_KANJI = re.compile(r"^[\u30A0-\u30FF\u3040-\u309F\u4E00-\u9FA5]+$")


# Defination

HIRAGANA = 'ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろわをんーゎゐゑゕゖゔゝゞ・「」。、'
KATAKANA = 'ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロワヲンーヮヰヱヵヶヴヽヾ・「」。、'

SEION_KATAKANA = 'カキクケコサシスセソタチツテトハヒフヘホ'
DAKUON_KATAKANA = 'ガギグゲゴザジズゼゾダヂヅデドバビブベボ'
SEION_HIRAGANA = 'かきくけこさしすせそたちつてとはひふへほ'
DAKUON_HIRAGANA = 'がぎぐげござじずぜぞだぢづでどばびぶべぼ'

SEION = SEION_HIRAGANA + SEION_KATAKANA
DAKUON = DAKUON_HIRAGANA + DAKUON_KATAKANA

SMALL_HIRAGANA = 'ぁぃぅぇぉゃゅょっ'
NORMALIZED_HIRAGANA = 'あいうえおやゆよつ'
SMALL_HALF_KATAKANA = 'ｧｨｩｪｫｬｭｮｯｰ'
NORMALIZED_HALF_KATAKANA = 'ｱｲｳｴｵﾔﾕﾖﾂｰ'
SMALL_KATAKANA = 'ァィゥェォヵヶャュョッ'
NORMALIZED_KATAKANA = 'アイウエオカケヤユヨツ'

SMALL_KANA = SMALL_HIRAGANA + SMALL_HALF_KATAKANA + SMALL_KATAKANA
NORMALIZED_KANA = NORMALIZED_HIRAGANA + NORMALIZED_HALF_KATAKANA + NORMALIZED_KATAKANA

ODORIZI = 'ゝゞヽヾ々'
ONBIKI = 'ｰ'
UNNORMAL_ONBIKI = '―‐˗֊‐‑‒–⁃⁻₋−-'

# Mapping
SEION_TO_DAKUON = str.maketrans(SEION, DAKUON)
DAKUON_TO_SEION = str.maketrans(DAKUON, SEION)

SMALL_TO_NORMALIZED = str.maketrans(SMALL_KANA, NORMALIZED_KANA)
NORMALIZED_TO_SMALL = str.maketrans(NORMALIZED_KANA, SMALL_KANA)

HIRA_TO_KATA = str.maketrans(HIRAGANA, KATAKANA)
KATA_TO_HIRA = str.maketrans(KATAKANA, HIRAGANA)

ONBIKI_TO_NORMALIZED = str.maketrans(UNNORMAL_ONBIKI, ONBIKI * len(UNNORMAL_ONBIKI))


# Function

# 踊り字の処理
def odorizi(origin: str) -> str:
    """
    处理日语中的叠字符号

    :param origin: 待处理文字
    :return: 返回文字
    """
    remapping = ''
    try:
        for char in origin:
            match char:
                case 'ゝ' | 'ヽ':
                    remapping += remapping[-1] if remapping[-1] in SEION else remapping[-1].translate(DAKUON_TO_SEION)
                case 'ゞ' | 'ヾ':
                    remapping += remapping[-1] if remapping[-1] in DAKUON else remapping[-1].translate(SEION_TO_DAKUON)
                case '々':
                    remapping += remapping[-1]
                case _:
                    remapping += char
    except Exception as e:
        print(e)
        remapping = origin
    return remapping


def to_katakana(origin: str) -> str:
    """

    :param origin:
    :return:
    """
    return ''.join(
        [item.reading_form() if RE_JAPANESE.KANA_AND_KANJI.match(item.surface()) else item.surface() for item in
         SUDACHI_DICT.tokenize(origin)])
