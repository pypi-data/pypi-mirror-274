"""DPCデータを取り扱うためのライブラリ"""

from csv import reader
from dataclasses import dataclass, field
from datetime import date
from os.path import basename


@dataclass
class LineBase:
    """各DPCデータの基底クラス"""

    COL_SIZE = 0

    cols: tuple = field(repr=False)

    def __post_init__(self):
        if len(self.cols) != self.COL_SIZE:
            raise TypeError(f'{self.__class__.__name__} requires '
                            f'{self.COL_SIZE} columns, '
                            f'but received {len(self.cols)} columns')

        self.cols = [col.strip() if isinstance(col, str) else col for col in self.cols]

    @staticmethod
    def to_float(x):
        """値を実数に変換する"""
        if x == 0:
            return 0.0

        if x:
            return float(x)

        return None

    @staticmethod
    def to_int(x):
        """値を整数に変換する"""
        if x == 0:
            return 0

        if x:
            return int(LineBase.to_float(x))

        return None

    @staticmethod
    def to_bool(x):
        """値を真偽値に変換する"""
        if x is False:
            return False

        if x:
            return bool(LineBase.to_int(x))

        return None

    @staticmethod
    def to_date(x):
        """値をDate型に変換する"""
        if not x:
            return None

        if isinstance(x, date):
            return x

        x = ''.join(x.split('-')) if x.count('-') else x
        x = x[:x.index('.')] if x.count('.') else x

        if len(x) != 8:
            return None

        if x in ('00000000', '99999999'):
            return None

        y, m, d = int(x[0:4]), int(x[4:6]), int(x[6:8])

        if y == 0 or m == 0:
            return None

        if d == 0:
            d = 1

        return date(y, m, d)

    @staticmethod
    def yyyymmdd(x):
        """Dateを8桁の文字列で返す"""
        if x:
            return f'{x.year:04d}{x.month:02d}{x.day:02d}'
        else:
            return '00000000'


class DPCFile:
    """DPCファイルの基底クラス"""

    line_class = LineBase

    def __init__(self, path=None, encoding='cp932'):
        self.encoding = encoding
        self.has_header = False
        self.file_name = ''
        self.lines = []

        if path:
            self.read(path)

    def read(self, path):
        """CSVファイルを開いて読み込み各ファイルが対象とするデータクラスのオブジェクトを格納する"""
        if not path:
            raise ValueError('No file path is passed')

        self.file_name = basename(path)

        with open(path, mode='r', encoding=self.encoding) as f:
            first_line = True

            for cols in reader(f, delimiter='\t'):
                if first_line:
                    first_line = False
                    if not cols[0].isdigit():
                        self.has_header = True
                        continue

                try:
                    o = self.line_class(cols)
                except TypeError as err:
                    msg = f'Error has occurerd to create {self.line_class.__name__}'
                    raise ValueError(msg) from err
                else:
                    self.lines.append(o)
