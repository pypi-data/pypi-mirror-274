"""Hファイルを取り扱うモジュール"""

from dataclasses import dataclass, field
from datetime import date

from .base import LineBase, DPCFile


# pylint: disable=R0902
@dataclass
class Hn(LineBase):
    """Hファイルを取り扱うクラス"""

    COL_SIZE = 29

    h_1: str = field(init=False)         # 施設コード
    h_2: str = field(init=False)         # 病棟コード
    h_3: str = field(init=False)         # データ識別番号
    h_4: date = field(init=False)        # 退院年月日
    h_5: date = field(init=False)        # 入院年月日
    h_6: date = field(init=False)        # 実施年月日
    code: str = field(init=False)        # コード
    version: str = field(init=False)     # バージョン
    number: int = field(init=False)      # 連番
    payload_1: int = field(init=False)   # ペイロード1
    payload_2: int = field(init=False)   # ペイロード2
    payload_3: int = field(init=False)   # ペイロード3
    payload_4: int = field(init=False)   # ペイロード4
    payload_5: int = field(init=False)   # ペイロード5
    payload_6: int = field(init=False)   # ペイロード6
    payload_7: int = field(init=False)   # ペイロード7
    payload_8: int = field(init=False)   # ペイロード8
    payload_9: int = field(init=False)   # ペイロード9
    payload_10: int = field(init=False)  # ペイロード10
    payload_11: int = field(init=False)  # ペイロード11
    payload_12: int = field(init=False)  # ペイロード12
    payload_13: int = field(init=False)  # ペイロード13
    payload_14: int = field(init=False)  # ペイロード14
    payload_15: int = field(init=False)  # ペイロード15
    payload_16: int = field(init=False)  # ペイロード16
    payload_17: int = field(init=False)  # ペイロード17
    payload_18: int = field(init=False)  # ペイロード18
    payload_19: int = field(init=False)  # ペイロード19
    payload_20: int = field(init=False)  # ペイロード20

    def __post_init__(self):
        super().__post_init__()

        self.h_1 = self.cols[0][:9]
        self.h_2 = self.cols[1][:10]
        self.h_3 = self.cols[2][:10]
        self.h_4 = self.to_date(self.cols[3])
        self.h_5 = self.to_date(self.cols[4])
        self.h_6 = self.to_date(self.cols[5])
        self.code = self.cols[6]
        self.version = self.cols[7][:8]
        self.number = self.to_int(self.cols[8])
        self.payload_1 = self.cols[9]
        self.payload_2 = self.cols[10]
        self.payload_3 = self.cols[11]
        self.payload_4 = self.cols[12]
        self.payload_5 = self.cols[13]
        self.payload_6 = self.cols[14]
        self.payload_7 = self.cols[15]
        self.payload_8 = self.cols[16]
        self.payload_9 = self.cols[17]
        self.payload_10 = self.cols[18]
        self.payload_11 = self.cols[19]
        self.payload_12 = self.cols[20]
        self.payload_13 = self.cols[21]
        self.payload_14 = self.cols[22]
        self.payload_15 = self.cols[23]
        self.payload_16 = self.cols[24]
        self.payload_17 = self.cols[25]
        self.payload_18 = self.cols[26]
        self.payload_19 = self.cols[27]
        self.payload_20 = self.cols[28]


class HnFile(DPCFile):
    """Hnファイルを扱うクラス"""

    line_class = Hn
