def vekstfaktor(fortegn = str(),
                p       = float(),
                desimal = -1,
                rund    = -1):

    # Gjør argument-alias om til samme variabel
    _desimal = -1
    if rund     != -1: _desimal = rund
    if desimal  != -1: _desimal = desimal
 
    # Vekstfaktor er definert som V = 1 ± p / 100, p: prosentvis vekst [%]
    v = float()
    if fortegn == "+": v = 1 + p / 100 # "+": Øker
    if fortegn == "-": v = 1 - p / 100 # "-": Minker

    # Runder av svaret
    if _desimal != -1: v = round(v, _desimal)

    return v
