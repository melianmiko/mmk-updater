import locale

from .data import L18N


def t(k: str) -> str:
    lang = locale.getlocale()[0]
    lang = "ru_RU"
    if lang in L18N:
        if k in L18N[lang]:
            return L18N[lang][k]
    return k
