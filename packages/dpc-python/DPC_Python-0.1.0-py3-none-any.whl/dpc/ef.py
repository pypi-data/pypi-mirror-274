"""入院EFファイルと外来EFファイルを取り扱うモジュール"""

from dataclasses import dataclass, field
from datetime import date

from .base import LineBase, DPCFile


# pylint: disable=R0902
@dataclass
class EF(LineBase):
    """入院EFファイルと外来EFファイルを取り扱うクラス"""

    COL_SIZE = 31

    ef_1: str = field(init=False)     # 施設コード
    ef_2: str = field(init=False)     # データ識別番号
    ef_3: date = field(init=False)    # 退院年月日（入院） | 生年月日（外来）
    ef_4: date = field(init=False)    # 入院年月日（入院） | 外来受診年月日（外来）
    ef_5: str = field(init=False)     # データ区分
    ef_6: int = field(init=False)     # 順序番号
    ef_7: int = field(init=False)     # 行為明細番号
    ef_8: str = field(init=False)     # 病院点数マスターコード
    ef_9: str = field(init=False)     # レセプト電算処理システム用コード
    ef_10: str = field(init=False)    # 解釈番号
    ef_11: str = field(init=False)    # 診療明細名称
    ef_12: float = field(init=False)  # 使用量
    ef_13: str = field(init=False)    # 基準単位
    ef_14: float = field(init=False)  # 明細点数・金額
    ef_15: bool = field(init=False)   # 円・点区分
    ef_16: int = field(init=False)    # 出来高実績点数
    ef_17: str = field(init=False)    # 行為明細区分情報
    ef_18: int = field(init=False)    # 行為点数
    ef_19: int = field(init=False)    # 行為薬剤料
    ef_20: int = field(init=False)    # 行為材料料
    ef_21: int = field(init=False)    # 行為回数
    ef_22: str = field(init=False)    # 保険者番号
    ef_23: str = field(init=False)    # レセプト種別コード
    ef_24: date = field(init=False)   # 実施年月日（入院） | 実施年月日・診療開始日（外来）
    ef_25: str = field(init=False)    # レセプト科区分
    ef_26: str = field(init=False)    # 診療科区分
    ef_27: str = field(init=False)    # 医師コード
    ef_28: str = field(init=False)    # 病棟コード
    ef_29: str = field(init=False)    # 病棟区分
    ef_30: bool = field(init=False)   # 入外区分
    ef_31: str = field(init=False)    # 施設タイプ

    def __post_init__(self):
        super().__post_init__()

        self.ef_1 = self.cols[0][:9]
        self.ef_2 = self.cols[1][:10]
        self.ef_3 = self.to_date(self.cols[2])
        self.ef_4 = self.to_date(self.cols[3])
        self.ef_5 = self.cols[4][:2]
        self.ef_6 = self.to_int(self.cols[5])
        self.ef_7 = self.to_int(self.cols[6])
        self.ef_8 = self.cols[7][:12]
        self.ef_9 = self.cols[8][:9]
        self.ef_10 = self.cols[9][:8]
        self.ef_11 = self.cols[10][:254]
        self.ef_12 = self.to_float(self.cols[11])
        self.ef_13 = self.cols[12][:3]
        self.ef_14 = self.to_float(self.cols[13])
        self.ef_15 = self.to_bool(self.cols[14])
        self.ef_16 = self.to_int(self.cols[15])
        self.ef_17 = self.cols[16][:12]
        self.ef_18 = self.to_int(self.cols[17])
        self.ef_19 = self.to_int(self.cols[18])
        self.ef_20 = self.to_int(self.cols[19])
        self.ef_21 = self.to_int(self.cols[20])
        self.ef_22 = self.cols[21][:8]
        self.ef_23 = self.cols[22][:4]
        self.ef_24 = self.to_date(self.cols[23])
        self.ef_25 = self.cols[24][:2]
        self.ef_26 = self.cols[25][:3]
        self.ef_27 = self.cols[26][:10]
        self.ef_28 = self.cols[27][:10]
        self.ef_29 = self.cols[28]
        self.ef_30 = self.to_bool(self.cols[29])
        self.ef_31 = self.cols[30][:3]

    def __str__(self):
        o = [
            self.ef_1,
            self.ef_2,
            self.yyyymmdd(self.ef_3),
            self.yyyymmdd(self.ef_4),
            self.ef_5,
            str(self.ef_6),
            str(self.ef_7),
            self.ef_8,
            self.ef_9,
            self.ef_10,
            self.ef_11,
            str(self.ef_12),
            self.ef_13,
            str(self.ef_14),
            '1' if self.ef_15 else '0',
            str(self.ef_16),
            self.ef_17,
            str(self.ef_18),
            str(self.ef_19),
            str(self.ef_20),
            str(self.ef_21),
            self.ef_22,
            self.ef_23,
            self.yyyymmdd(self.ef_24),
            self.ef_25,
            self.ef_26,
            self.ef_27,
            self.ef_28,
            self.ef_29,
            '1' if self.ef_30 else '0',
            self.ef_31,
        ]

        return '\t'.join(o)


# pylint: disable=R0902
@dataclass
class E(LineBase):
    """入院Eファイルと外来Eファイルを取り扱うクラス"""

    COL_SIZE = 25

    e_1: str = field(init=False)    # 施設コード
    e_2: str = field(init=False)    # データ識別番号
    e_3: date = field(init=False)   # 退院年月日（入院） | 生年月日（外来）
    e_4: date = field(init=False)   # 入院年月日（入院） | 外来受診年月日（外来）
    e_5: str = field(init=False)    # データ区分
    e_6: int = field(init=False)    # 順序番号
    e_7: str = field(init=False)    # 病院点数マスターコード
    e_8: str = field(init=False)    # レセプト電算処理システム用コード
    e_9: str = field(init=False)    # 解釈番号
    e_10: str = field(init=False)   # 診療行為名称
    e_11: int = field(init=False)   # 行為点数
    e_12: int = field(init=False)   # 行為薬剤料
    e_13: int = field(init=False)   # 行為材料料
    e_14: bool = field(init=False)  # 円・点区分
    e_15: int = field(init=False)   # 行為回数
    e_16: str = field(init=False)   # 保険者番号
    e_17: str = field(init=False)   # レセプト種別コード
    e_18: date = field(init=False)  # 実施年月日（入院） | 実施年月日・診療開始日（外来）
    e_19: str = field(init=False)   # レセプト科区分
    e_20: str = field(init=False)   # 診療科区分
    e_21: str = field(init=False)   # 医師コード
    e_22: str = field(init=False)   # 病棟コード
    e_23: str = field(init=False)   # 病棟区分
    e_24: bool = field(init=False)  # 入外区分
    e_25: str = field(init=False)   # 施設タイプ

    def __post_init__(self):
        super().__post_init__()

        self.e_1 = self.cols[0][:9]
        self.e_2 = self.cols[1][:10]
        self.e_3 = self.to_date(self.cols[2])
        self.e_4 = self.to_date(self.cols[3])
        self.e_5 = self.cols[4][:2]
        self.e_6 = self.to_int(self.cols[5])
        self.e_7 = self.cols[6][:12]
        self.e_8 = self.cols[7][:9]
        self.e_9 = self.cols[8][:8]
        self.e_10 = self.cols[9][:254]
        self.e_11 = self.to_int(self.cols[10])
        self.e_12 = self.to_int(self.cols[11])
        self.e_13 = self.to_int(self.cols[12])
        self.e_14 = self.to_bool(self.cols[13])
        self.e_15 = self.to_int(self.cols[14])
        self.e_16 = self.cols[15][:8]
        self.e_17 = self.cols[16][:4]
        self.e_18 = self.to_date(self.cols[17])
        self.e_19 = self.cols[18][:2]
        self.e_20 = self.cols[19][:3]
        self.e_21 = self.cols[20][:10]
        self.e_22 = self.cols[21][:10]
        self.e_23 = self.cols[22][:1]
        self.e_24 = self.to_bool(self.cols[23])
        self.e_25 = self.cols[24][:3]


# pylint: disable=R0902
@dataclass
class F(LineBase):
    """入院Fファイルと外来Fファイルを取り扱うクラス"""

    COL_SIZE = 19

    f_1: str = field(init=False)     # 施設コード
    f_2: str = field(init=False)     # データ識別番号
    f_3: date = field(init=False)    # 退院年月日（入院） | 生年月日（外来）
    f_4: date = field(init=False)    # 入院年月日（入院） | 外来受診年月日（外来）
    f_5: str = field(init=False)     # データ区分
    f_6: int = field(init=False)     # 順序番号
    f_7: int = field(init=False)     # 行為明細判号
    f_8: str = field(init=False)     # 病院点数マスターコード
    f_9: str = field(init=False)     # レセプト電算処理システム用コード
    f_10: str = field(init=False)    # 解釈番号
    f_11: str = field(init=False)    # 診療明細名称
    f_12: float = field(init=False)  # 使用量
    f_13: str = field(init=False)    # 基準単位
    f_14: int = field(init=False)    # 行為明細点数
    f_15: int = field(init=False)    # 行為明細薬剤料
    f_16: int = field(init=False)    # 行為明細材料料
    f_17: bool = field(init=False)   # 円・点区分
    f_18: int = field(init=False)    # 出来高実績点数
    f_19: str = field(init=False)    # 行為明細区分情報

    def __post_init__(self):
        super().__post_init__()

        self.f_1 = self.cols[0][:9]
        self.f_2 = self.cols[1][:10]
        self.f_3 = self.to_date(self.cols[2])
        self.f_4 = self.to_date(self.cols[3])
        self.f_5 = self.cols[4][:2]
        self.f_6 = self.to_int(self.cols[5])
        self.f_7 = self.to_int(self.cols[6])
        self.f_8 = self.cols[7][:12]
        self.f_9 = self.cols[8][:9]
        self.f_10 = self.cols[9][:8]
        self.f_11 = self.cols[10][:254]
        self.f_12 = self.to_float(self.cols[11])
        self.f_13 = self.cols[12][:3]
        self.f_14 = self.to_int(self.cols[13])
        self.f_15 = self.to_int(self.cols[14])
        self.f_16 = self.to_int(self.cols[15])
        self.f_17 = self.to_bool(self.cols[16])
        self.f_18 = self.to_int(self.cols[17])
        self.f_19 = self.cols[18][:12]


class EFFile(DPCFile):
    """EFファイルを扱うクラス"""

    line_class = EF


class EFile(DPCFile):
    """Eファイルを扱うクラス"""

    line_class = E


class FFile(DPCFile):
    """Fファイルを扱うクラス"""

    line_class = F


def generate_ef_lines(e_lines, f_lines):
    """Eファイルの内容とFファイルの内容からEFファイルの内容を生成する関数"""
    m = {}
    lines = []

    for e_line in e_lines:
        k = (e_line.e_1, e_line.e_2, e_line.e_3,
             e_line.e_4, e_line.e_5, e_line.e_6)
        m[k] = e_line

        ef_line = EF((
            e_line.e_1,
            e_line.e_2,
            e_line.e_3,
            e_line.e_4,
            e_line.e_5,
            e_line.e_6,
            0,
            e_line.e_7,
            e_line.e_8,
            e_line.e_9,
            e_line.e_10,
            0.0,
            '',
            0,
            e_line.e_14,
            0,
            '',
            e_line.e_11,
            e_line.e_12,
            e_line.e_13,
            e_line.e_15,
            e_line.e_16,
            e_line.e_17,
            e_line.e_18,
            e_line.e_19,
            e_line.e_20,
            e_line.e_21,
            e_line.e_22,
            e_line.e_23,
            e_line.e_24,
            e_line.e_25,
        ))

        lines.append(ef_line)

    for f_line in f_lines:
        k = (f_line.f_1, f_line.f_2, f_line.f_3,
             f_line.f_4, f_line.f_5, f_line.f_6)

        e_line = m[k]

        ef_14 = 0
        if f_line.f_14:
            ef_14 = f_line.f_14
        elif f_line.f_15:
            ef_14 = f_line.f_15
        elif f_line.f_16:
            ef_14 = f_line.f_16

        ef_line = EF((
            f_line.f_1,
            f_line.f_2,
            f_line.f_3,
            f_line.f_4,
            f_line.f_5,
            f_line.f_6,
            f_line.f_7,
            f_line.f_8,
            f_line.f_9,
            f_line.f_10,
            f_line.f_11,
            f_line.f_12,
            f_line.f_13,
            ef_14,
            f_line.f_17,
            f_line.f_18,
            f_line.f_19,
            e_line.e_11,
            e_line.e_12,
            e_line.e_13,
            e_line.e_15,
            e_line.e_16,
            e_line.e_17,
            e_line.e_18,
            e_line.e_19,
            e_line.e_20,
            e_line.e_21,
            e_line.e_22,
            e_line.e_23,
            e_line.e_24,
            e_line.e_25,
        ))

        lines.append(ef_line)

    return lines
