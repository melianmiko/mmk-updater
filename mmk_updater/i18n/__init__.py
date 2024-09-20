import locale

from .data import L18N


def t(k):
    lang = locale.getlocale()[0]
    if lang in L18N:
        if k in L18N[lang]:
            return L18N[lang][k]
    return k
