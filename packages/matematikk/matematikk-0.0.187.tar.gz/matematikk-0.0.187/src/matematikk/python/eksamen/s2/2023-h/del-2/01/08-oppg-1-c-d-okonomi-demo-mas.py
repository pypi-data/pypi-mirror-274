# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Høst (Matematikk AS)
# Oppgave 1 c) og d) Alle svar - økonmi - DEMO
# - Løser oppgaven med CAS i Python
# - Kopier denne kommandoen i terminalen for å importere matematikk:
#   $ pip install matematikk

import matematikk as mt
x = mt.Symbol("x")
alle_svar = mt.økonomi(
    p = 79 - 12.2 * mt.ln(x)
)

