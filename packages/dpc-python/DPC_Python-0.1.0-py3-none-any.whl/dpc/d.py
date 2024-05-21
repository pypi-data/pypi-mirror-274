"""Dファイルを取り扱うモジュール"""

from dataclasses import dataclass, field
from datetime import date

from .base import LineBase, DPCFile


# pylint: disable=R0902
@dataclass
class Dn(LineBase):
    """Dファイルを取り扱うクラス"""

    COL_SIZE = 30

    d_1: str = field(init=False)     # 施設コード
    d_2: str = field(init=False)     # データ識別番号
    d_3: date = field(init=False)    # 退院年月日
    d_4: date = field(init=False)    # 入院年月日
    d_5: str = field(init=False)     # データ区分
    d_6: int = field(init=False)     # 順序番号
    d_7: str = field(init=False)     # 病院点数マスターコード
    d_8: str = field(init=False)     # レセプト電算処理システム用コード
    d_9: str = field(init=False)     # 解釈番号
    d_10: str = field(init=False)    # 診療行為名称
    d_11: int = field(init=False)    # 行為点数
    d_12: int = field(init=False)    # 行為薬剤料
    d_13: int = field(init=False)    # 行為材料料
    d_14: bool = field(init=False)   # 円・点区分
    d_15: int = field(init=False)    # 行為回数
    d_16: str = field(init=False)    # レセ電算保険者番号
    d_17: str = field(init=False)    # レセプト種別コード
    d_18: date = field(init=False)   # 実施年月日
    d_19: str = field(init=False)    # レセプト科区分
    d_20: str = field(init=False)    # 診療科区分
    d_21: str = field(init=False)    # 医師コード
    d_22: str = field(init=False)    # 病棟コード
    d_23: str = field(init=False)    # 病棟区分
    d_24: bool = field(init=False)   # 入外区分
    d_25: str = field(init=False)    # 施設タイプ
    d_26: date = field(init=False)   # 算定開始日
    d_27: date = field(init=False)   # 算定終了日
    d_28: date = field(init=False)   # 算定起算日
    d_29: str = field(init=False)    # 診断群分類番号
    d_30: float = field(init=False)  # 医療機関別係数

    def __post_init__(self):
        super().__post_init__()
        self.d_1 = self.cols[0][:9]
        self.d_2 = self.cols[1][:10]
        self.d_3 = self.to_date(self.cols[2])
        self.d_4 = self.to_date(self.cols[3])
        self.d_5 = self.cols[4][:2]
        self.d_6 = self.to_int(self.cols[5])
        self.d_7 = self.cols[6][:12]
        self.d_8 = self.cols[7][:9]
        self.d_9 = self.cols[8][:8]
        self.d_10 = self.cols[9][:254]
        self.d_11 = self.to_int(self.cols[10])
        self.d_12 = self.to_int(self.cols[11])
        self.d_13 = self.to_int(self.cols[12])
        self.d_14 = self.to_bool(self.cols[13])
        self.d_15 = self.to_int(self.cols[14])
        self.d_16 = self.cols[15][:8]
        self.d_17 = self.cols[16][:4]
        self.d_18 = self.to_date(self.cols[17])
        self.d_19 = self.cols[18][:2]
        self.d_20 = self.cols[19][:3]
        self.d_21 = self.cols[20][:10]
        self.d_22 = self.cols[21][:10]
        self.d_23 = self.cols[22][:1]
        self.d_24 = self.to_bool(self.cols[23])
        self.d_25 = self.cols[24][:3]
        self.d_26 = self.to_date(self.cols[25])
        self.d_27 = self.to_date(self.cols[26])
        self.d_28 = self.to_date(self.cols[27])
        self.d_29 = self.cols[28][:14]
        self.d_30 = self.to_float(self.cols[29])


class DnFile(DPCFile):
    """Dnファイルを扱うクラス"""

    line_class = Dn
