# 🚀 programmering.no | 🤓 matematikk.as

import matematikk as mt

def okonomi(variabel = mt.Symbol(""),
            uttrykk  = mt.Symbol(""),
            desimal  = None,
            debug    = -1):

    # overskudd_max() er en undergruppe av ekstremalpunkt_max()
    variabel_max = mt.ekstremalpunkt_max(variabel = variabel,
                                         uttrykk  = uttrykk,
                                         rund     = desimal,
                                         debug    = debug)

    return variabel_max

# Alias > 1 > ...

# Alias > 2 > ...

