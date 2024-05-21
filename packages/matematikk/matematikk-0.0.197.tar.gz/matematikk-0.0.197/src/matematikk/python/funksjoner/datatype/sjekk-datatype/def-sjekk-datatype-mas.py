
# yooo
def sjekk_datatype(vari_navn = str(), vari = None, typ = None):

    # None er default-argument pga. forskjellige datatyper

    # Riktig type
    if type(vari) == typ:

        return vari

    # Feil type
    if type(vari) != typ:

        # Advarsel
        _typ = type(vari)

        # int: Type caster feil type -> riktig type
        if typ == int: _vari = int(vari)

        print(f"Advarsel ({vari_navn}): Type caster {vari} ({_typ.__name__}) til {_vari} ({typ.__name__})")

        return _vari

# Alias > 1 > ...

# Alias > 2 > ... 
datatype_sjekk                        = sjekk_datatype
