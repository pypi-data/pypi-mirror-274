"""様式1ファイルを取り扱うモジュール"""

from dataclasses import dataclass, field
from datetime import date

from .base import LineBase, DPCFile


# pylint: disable=R0902
@dataclass
class FF1(LineBase):
    """様式1ファイルを取り扱うクラス"""

    COL_SIZE = 17

    ff1_1: str = field(init=False)       # 施設コード
    ff1_2: str = field(init=False)       # データ識別番号
    ff1_3: date = field(init=False)      # 入院年月日
    ff1_4: int = field(init=False)       # 回数管理番号
    ff1_5: str = field(init=False)       # 統括診療情報番号
    code: str = field(init=False)        # コード
    version: str = field(init=False)     # バージョン
    number: int = field(init=False)      # 連番
    payload_1: date = field(init=False)  # ペイロード1
    payload_2: int = field(init=False)   # ペイロード2
    payload_3: int = field(init=False)   # ペイロード3
    payload_4: int = field(init=False)   # ペイロード4
    payload_5: int = field(init=False)   # ペイロード5
    payload_6: int = field(init=False)   # ペイロード6
    payload_7: int = field(init=False)   # ペイロード7
    payload_8: int = field(init=False)   # ペイロード8
    payload_9: int = field(init=False)   # ペイロード9

    def __post_init__(self):
        super().__post_init__()

        self.ff1_1 = self.cols[0][:9]
        self.ff1_2 = self.cols[1][:10]
        self.ff1_3 = self.to_date(self.cols[2])
        self.ff1_4 = self.to_int(self.cols[3])
        self.ff1_5 = self.cols[4]
        self.code = self.cols[5]
        self.version = self.cols[6][:8]
        self.number = self.to_int(self.cols[7])
        self.payload_1 = self.cols[8]
        self.payload_2 = self.cols[9]
        self.payload_3 = self.cols[10]
        self.payload_4 = self.cols[11]
        self.payload_5 = self.cols[12]
        self.payload_6 = self.cols[13]
        self.payload_7 = self.cols[14]
        self.payload_8 = self.cols[15]
        self.payload_9 = self.cols[16]


class FF1File(DPCFile):
    """様式1ファイルを扱うクラス"""

    line_class = FF1
