#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import collections
import re

DAY_SUFFIX = (
    ("pierws", "szy"),
    ("pierws", "szego"),
    ("dru", "gi"),
    ("dru", "giego"),
    ("trzeci", "trzeci"),
    ("trzeci", "ego"),
    ("czwar", "rty"),
    ("czwar", "tego"),
    ("pią", "ąty"),
    ("pią", "tego"),
    ("szó", "óty"),
    ("szó", "tego"),
    ("siódm", "my"),
    ("siódm", "ego"),
    ("ó", "smy"),
    ("ó", "smego"),
    ("dziewią", "ąty"),
    ("dziewią", "tego"),
    ("dziesia", "ąty"),
    ("dziesia", "tego"),
    ("jedenas", "sty"),
    ("jedenas", "tego"),
)


MONTH_NAMES = ("stycz", "lut", "mar", "kwie", "maj", "czerw",
               "lip", "sierp", "wrze", "paździer", "listop", "grud")

HOUR_SUFFIX = (
    ("połud", "dnie"),
    ("połud", "dnia"),
    ("połud", "dniu"),
    ("połud", "dniem"),
    ("pierws", "sza"),
    ("pierws", "szej"),
    ("pierws", "szą"),
    ("dru", "ga"),
    ("dru", "giej"),  # było zduplikowane
    ("dru", "gą"),  # było: ("dru", "gią"), - zrobić jeszcze unittest
    ("trzeci", "trzecia"),
    ("trzeci", "trzeciej"),
    ("trzeci", "trzecią"),
    ("czwar", "rta"),
    ("czwar", "rtej"),
    ("czwar", "rtą"),
    ("pią", "ąta"),
    ("pią", "ątej"),
    ("pią", "ątą"),
    ("szó", "sta"),
    ("szó", "stej"),
    ("szó", "stą"),
    ("siódm", "dma"),
    ("siódm", "dmej"),
    ("siódm", "dmą"),
    ("ó", "sma"),
    ("ó", "smej"),
    ("ó", "smą"),
    ("dziewią", "ąta"),
    ("dziewią", "tej"),
    ("dziewią", "ątą"),  # było: ("dziewią", "ąta") - zrobić unittest
    ("dziesią", "ąta"),  # było: ("dziesia", "ąta") - zrobić unittest
    ("dziesią", "tej"),  # było: ("dziesia", "ąta") - zrobić unittest
    ("dziesią", "ątą"),  # było: ("dziesia", "ąta") - zrobić unittest
    ("jedenas", "sta"),  # było: ("jedenas", "ąta") - zrobić unittest
    ("jedenas", "tej"),
    ("jedenas", "stą"),  # było: ("jedenas", "ąta") - zrobić unittest
)

# "w pół" jest niegramatyczne
HALF_HOUR_WORDS = ("o wpół do", "o pół do", "o wpół", "o pół", "wpół do",
                   "w pół do", "pół do", "w pół", "wpół", "pół")

TEN_MULIPLE_WORDS = (
    'dziesięć', 'dziesiątego', 'dzieścia', 'dzieści', 'dziesty', 'dziestego',
    'dziesta', 'dziestej', 'dziesiąt', 'dziesiąty', 'dziesiątego', 'dziesiąta',
    'dziesiątej'
)

MINUTE_SUFFIX = (
    ("kwadrans", "drans"),
    ("kwadrans", "drana"),
    ("kwadrans", "dranse"),
    ("kwadrans", "dransów"),
    ("minuta", "minuta"),  #
    ("minutę", "minutę"),  #
    ("jed", "en"),
    ("jed", "nego"),
    ("dw", "dwa"),
    ("dw", "wie"),
    ("tr", "rzy"),
    ("czt", "tery"),
    ("pię", "ć"),
    ("sześ", "ć"),
    ("sied", "em"),
    ("o", "siem"),
    ("dziewię", "ć"),
    ("jedena", "ście"),
    ("dw", "adzieścia"),
    ("dw", "adzieścia"),
    ("trzydzie", "ści"),
    ("czterdzie", "ści"),
    ("pięćdziesi", "ąt"),
    ("sześćdziesi", "ąt"),
)

# REGEX
DAY = "|".join([r"\b[\wĄąÓó]*{0}\b".format(ds1) for ds0, ds1 in DAY_SUFFIX])
MONTH = "|".join([r"\b{0}[\wŚś]*\b".format(m) for m in MONTH_NAMES])
HOUR = "|".join([r"\b[\wĄĆĘŁŃÓŚŻŹąćęłńóśżź]*{0}\b".format(hs1) for hs0, hs1 in HOUR_SUFFIX])
HALF_HOUR = "|".join([r"\b{0}\b".format(hh) for hh in HALF_HOUR_WORDS])
MINUTES = "|".join([r"\b[\wĄĆĘŁŃÓŚŻŹąćęłńóśżź]*{0}\b(\skwadrans\w*)*".format(ms1) for ms0, ms1 in MINUTE_SUFFIX])
PRE_MODIF = "|".join([r"\b{0}\b".format(prem) for prem in ("do", "przed")])
POST_MODIF = "|".join([r"\b{0}\b".format(postm) for postm in ("za", )])
ON_HOUR = r"\bna\b"
TEN_MULIPLE = "(" + "|".join([r"{0}".format(m10) for m10 in TEN_MULIPLE_WORDS]) + ")"

# Zasady ekstrakcji danych z tekstu; wykorzystują powyższe wyrażenia regularne
PARSE_SPEC = [
    ('DAY', DAY),
    ('MONTH', MONTH),
    ('HOUR', HOUR),
    ('HALF_HOUR', HALF_HOUR),
    ('MINUTES', MINUTES),
    ('PRE_MODIF', PRE_MODIF),
    ('POST_MODIF', POST_MODIF),
    ('ON_HOUR', ON_HOUR),
]

TO_NUM_SPEC = [
    ('NUM_1', r'^(jed|pierw|minuta|minutę)'),
    ('NUM_2', r'^(dw|dru)'),
    ('NUM_3', r'^(trze|trzy)'),
    ('NUM_4', r'^(czt|czwar)'),
    ('NUM_5', r'^(pię|pią)'),
    ('NUM_6', r'^(sześ|szó|szes|sze)'),
    ('NUM_7', r'^(sied|siódm)'),
    ('NUM_8', r'^(osie|ósm)'),
    ('NUM_9', r'^(dziewię|dziewią)'),
    ('MULT_10', TEN_MULIPLE),
    ('PLUS_10', r'(naście|nasty|nasta|nastego|nastej)'),
    ('MONTH_0', MONTH),
    ('QUATER_15', r'kwadra'),
    ('MID_12', r'^południ'),
]


def tokenize(s, spec):
    """Dzieli teksty na tokeny, na podstawie zadanego kryterium.
    -- s - tekst wejściowy <type: str>
    -- spec - kryterium tokenizacji <type: list[tuple[str, regex]]
    """
    Token = collections.namedtuple('Token', ['typeof', 'text', 'pos'])
    token_regex = '|'.join('(?P<%s>%s)' % pair for pair in spec)
    for mo in re.finditer(token_regex, s, flags=re.IGNORECASE):
        typeof = mo.lastgroup
        text = mo.group()
        pos = mo.span()
        # print(Token(typeof, text, pos))
        yield Token(typeof, text, pos)


def to_num(textnum):
    """Konwertuje tekst na liczbę."""
    calcfunc = {'MULT': lambda n: n * 10,
                'PLUS': lambda n: n + 10,
                'UNIT': lambda n: n,
                'MONTH': lambda n: [m for m, word in enumerate(MONTH_NAMES) if n.startswith(word)][0] + 1,
                'QUATER': lambda n: n * 15,
                }
    # calcfunc bezpieczniejsze niż exec()!
    calculation = None
    d = 1
    for n in tokenize(textnum, TO_NUM_SPEC):
        base, num = n.typeof.split('_')
        if base == 'NUM':
            d = int(num)
            calculation = 'UNIT'
        elif base == 'MULT':
            calculation = 'MULT'
        elif base == 'PLUS':
            calculation = 'PLUS'
        elif base == 'MONTH':
            d = n.text
            calculation = 'MONTH'
        elif base == 'QUATER':
            calculation = 'QUATER'
        elif base == 'MID':
            d = 12
            calculation = 'UNIT'
    try:
        return calcfunc[calculation](d)
    except KeyError:
        print("Nie rozpoznano")
        return 0


def calc_month(monthlist, reminder):
    """Oblicza miesiąc. Przyjmuje resztę z obliczania dnia zwracaną przez
    funkcję calc_day.

    -- monthlist - lista miesięcy <type List[int]>
    -- reminder - naddatek z obliczania dnia <type int>, może być 0
    """
    if reminder != 0:
        monthlist.append(reminder)
    if len(monthlist) == 0:
        return 1
    else:
        return sum(monthlist)


def calc_day(daylist):
    """Oblicza dzień. Funkcja sprawdza, czy tokenizer błędnie nie uznał
    okreslenia miesiąca za dzień. Jeśli tak, zwraca tę wartość. Ale daylist może
    być dłuża niż 1 i może być to poprawne - np. dwudziesty czwarty. Funkcja
    też to sprawdza.

    -- daylist - lista dni <type List[int]>
    """
    if len(daylist) < 2:
        return sum(daylist), 0
    elif len(daylist) == 2:
        if daylist[0] > 19 and daylist[1] < 10:
            return sum(daylist), 0
        else:
            return tuple(daylist)


def calc_time(hours, minutes):
    """Oblicza godzinę w formacie 24-godzinnym i minuty."""
    hour, minute = divmod(hours * 60 + minutes, 60)
    return hour % 24, minute


def recognize(s):
    """Głowna funkcja skryptu. Przyjmuje tekst, wywołuje pozostałe funkcje
    i zwraca słownik.

    -- s - tekst wejściowy <type str>
    """
    if not isinstance(s, str):
        print("Skrypt wymaga danych typu <str>")
        return
    parse_gen = tokenize(s, PARSE_SPEC)
    day = []
    month = []
    hour = 0
    minute = []
    modif = 1
    while s:
        try:
            token = next(parse_gen)
        except StopIteration:
            break
        if token.typeof == "DAY":
            day.append(to_num(token.text))
        elif token.typeof == "MONTH":
            month.append(to_num(token.text))
        elif token.typeof == "HOUR":
            hour += to_num(token.text)
        elif token.typeof == "HALF_HOUR":
            h = -30
            minute.append(h)
        elif token.typeof == "POST_MODIF":  # "za", np. za dwadzieścia pięć
            modif = -modif if modif > 0 else modif
        elif token.typeof == "PRE_MODIF":  # "do", "przed", np. dwadzieścia pięć minut do ósmej, kwadrans przed siódmą
            minute = [-m for m in minute]
        elif token.typeof == "ON_HOUR":  # "na", np. kwadrans na piątą == 4:15
            minute = [m - 60 for m in minute]
        elif token.typeof == "MINUTES":
            m = to_num(token.text) * modif
            minute.append(m)
    try:
        day, reminder = calc_day(day)
    except TypeError:
        reminder = 0
        print("Nie rozpoznano:", s)
    month = calc_month(month, reminder)
    hour, minute = calc_time(hour, sum(minute))
    datedict = {"day": day, "month": month, "hour": hour, "minute": minute}
    return datedict


def main():
    return 0


if __name__ == "__main__":
    main()
