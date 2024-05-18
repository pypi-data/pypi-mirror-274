#from _defs.def_bld import (
#    bld
#)
#from _defs.def_col import (
#    col_
#)
#from _konst.prim_col0 import Col0
#_col0 = Col0()

import matematikk as mt
from colorama import Fore, Style

def økonomi(
    oppg_typ                        = "",
    I_uttrykk                       = mt.Symbol(""),
    pris_uttrykk_hs_desimal         = -1,
    pris_uttrykk_hs_rund            = -1,
    pris_uttrykk_hs                 = mt.Symbol(""),
    pris_desimal                    = -1,
    pris_rund                       = -1,
    pris                            = mt.Symbol(""),
    p_desimal                       = -1,
    p_rund                          = -1,
    p                               = mt.Symbol(""),
    ):

    # Oppg
    _oppg_typ   = ""
    _tit        = ""

    # Økonomi
    if oppg_typ                     == "":

        _oppg_typ   = "Økonomi"
        _tit        = "Økonomi"

    # Eksamen
    if oppg_typ                     != "":

        _oppg_typ   = "Eksamen" # oppg_typ
        _tit        = "Eksamen" # oppg_typ

    # Pris
    _p = mt.Symbol("")
    if p                            != mt.Symbol(""): _p = p
    if pris                         != mt.Symbol(""): _p = p
    if pris_uttrykk_hs              != mt.Symbol(""): _p = p

    # Pris avrunding
    _p_desimal = 0
    if pris_uttrykk_hs_desimal      != -1: _p_desimal = pris_uttrykk_hs_desimal
    if pris_uttrykk_hs_rund         != -1: _p_desimal = pris_uttrykk_hs_desimal
    if pris_desimal                 != -1: _p_desimal = pris_desimal
    if pris_rund                    != -1: _p_desimal = pris_rund
    if p_desimal                    != -1: _p_desimal = p_desimal
    if p_rund                       != -1: _p_desimal = p_rund

    # Inntekts-funksjon
    _I = mt.Symbol("")
    if I_uttrykk                    != mt.Symbol(""): _I = I_uttrykk
    if I_uttrykk                    == mt.Symbol(""): _I = _p * x

    # Variabler
    _pr_ls                          = list()
    _p_fn                           = "-"
    _I_fn                           = "-"
    _inntekt_max_enheter            = "-"
    _inntekt_max_pris               = "-"

    # Pris-funksjon
    if _p == mt.Symbol(""): pass
    if _p != mt.Symbol(""):

        _p_fn = f"p(x) = {_p}"

        # Antall enheter (etterspørsel) og pris per enhet når inntekten er størst
        enhet_og_pris_ls = mt.enhet_og_pris_fra_inntekt_max(pris_uttrykk_hs = p,
                                                            pris_desimal    = _p_desimal,
                                                            enhet_vari      = mt.Symbol("x"),
                                                            enhet_desimal   = None,
                                                            enhet_debug     = -1)

    # Inntekst-funksjon
    if _I == mt.Symbol(""): _I = _p * x
    if _I_fn == "-":

        _I_fn = "I(x)" + " " + "=" + " " + str(_I)

    # Størst inntekt > Antall enheter
    if _p_fn == "-": pass
    if _p_fn != "-":

        _inntekt_max_enheter = "x = " f"{enhet_og_pris_ls[0]}"

    # Størst inntekt
    if _p_fn == "-": pass
    if _p_fn != "-":

        _inntekt_max_pris_val = round(float(enhet_og_pris_ls[1]), 2)
        _inntekt_max_pris = "p(x) = " + f"{_inntekt_max_pris_val}" + " " + "kr"

    _colors = 1
    _is_colors = 0
    # 1: Light bvit
    # 2: Blå
    # 3: Rød
    _col_tit        = 1
    _col_ramme      = 3
    _col_uttrykk    = 2
    #def cc(txt, typ = 0):
    #    if _colors == 0: return txt
    #    if _colors == 1:
    #        if typ == 0: return col_(txt, _col0._green)
    #        if typ == 1: return col_(txt, _col0._green)
    #        if typ == 2: return col_(txt, _col0._magenta)
    #        if typ == 3: return col_(txt, _col0._red)
    #        if typ == 4: return col_(txt, _col0._blue)

    if _oppg_typ == "Økonomi":

        _pr_ls.append(f"╔══════════════════════════════════════") # ┌
        _pr_ls.append(f"║ {_tit}                            ") # │
        _pr_ls.append(f"╠───┬──────────────────────────────────")
        _pr_ls.append(f"║   │ Pris-funksjon                    ") # │
        _pr_ls.append(f"║   └───┬─────────┬────────────────────")
        _pr_ls.append(f"║       │ Uttrykk │ {_p_fn} ")
        _pr_ls.append(f"║   ┌───┴─────────┴────────────────────")
        _pr_ls.append(f"║   │ Inntekt-funksjon                 ")
        _pr_ls.append(f"║   └───┬─────────┬────────────────────")
        _pr_ls.append(f"║       │ Uttrykk │ {_I_fn} ")
        _pr_ls.append(f"║       ├─────────┴──────┬─────────┬")
        _pr_ls.append(f"║       │ Størst inntekt │ Enheter │ {_inntekt_max_enheter} ")
        _pr_ls.append(f"║       └────────────────┼─────────┼")
        _pr_ls.append(f"║                        │ Pris    │ {_inntekt_max_pris} ")
        _pr_ls.append(f"╚════════════════════════╩═════════╩") #  └ ╩ ┴ ┴

    # Eksamen
    if _oppg_typ == "Eksamen":

        _pr_ls.append(f"╔══════════════════════════════════════") # ┌
        _pr_ls.append(f"║ {_tit}                            ") # │
        _pr_ls.append(f"╠───┬──────────────────────────────────") # ├
        _pr_ls.append(f"║   │ Økonomi                    ") # │
        _pr_ls.append(f"║   └───┬─────────────────────────────")
        _pr_ls.append(f"║       │ Pris-funksjon                    ") # │
        _pr_ls.append(f"║       └───┬─────────┬────────────────────")
        _pr_ls.append(f"║           │ Uttrykk │ {_p_fn} ")
        _pr_ls.append(f"║       ┌───┴─────────┴────────────────────")
        _pr_ls.append(f"║       │ Inntekt-funksjon                 ")
        _pr_ls.append(f"║       └───┬─────────┬────────────────────")
        _pr_ls.append(f"║           │ Uttrykk │ {_I_fn} ")
        _pr_ls.append(f"║           ├─────────┴──────┬─────────┬")
        _pr_ls.append(f"║           │ Størst inntekt │ Enheter │ {_inntekt_max_enheter} ")
        _pr_ls.append(f"║           └────────────────┼─────────┼")
        _pr_ls.append(f"║                            │ Pris    │ {_inntekt_max_pris} ")
        _pr_ls.append(f"╚════════════════════════════╩═════════╩") #  └ ╩ ┴ ┴


    _cnt    = 0
    _i_max  = list()

    # Finn lengste lengde
    for i in range(len(_pr_ls)):
        if len(_pr_ls[i]) > _cnt: _cnt = len(_pr_ls[i])

    # Lagre index med max lengde
    for i in range(len(_pr_ls)):
        if len(_pr_ls[i]) == _cnt: _i_max.append(i)

    # Lag streker / space
    for i in range(len(_pr_ls)):

        if len(_pr_ls[i]) < _cnt:
            _diff = _cnt - len(_pr_ls[i])
            _strek = ""
            _STREK = ""
            _space = ""
            for _ in range(_diff):
                _strek += r"─"
                _STREK += r"═"
                _space += f" "

        # Max lengde
        if i in _i_max: _pr_ls[i] = _pr_ls[i] + "║" # + "│"

        # Vanlig lengde
        else:

            if _oppg_typ == "Økonomi":

                if i == 0:      _pr_ls[i] = _pr_ls[i] + _STREK + "╗" # + "┐"
                if i == 1:      _pr_ls[i] = _pr_ls[i] + _space + "║" # + "│"
                if i == 2:      _pr_ls[i] = _pr_ls[i] + _strek + "╣" # + "┤"
                if i == 3:      _pr_ls[i] = _pr_ls[i] + _space + "║" # + "│"
                if i == 4:      _pr_ls[i] = _pr_ls[i] + _strek + "╣" # + "┤"
                if i == 5:      _pr_ls[i] = _pr_ls[i] + _space + "║" # + "│"
                if i == 6:      _pr_ls[i] = _pr_ls[i] + _strek + "╣" # + "┤"
                if i == 7:      _pr_ls[i] = _pr_ls[i] + _space + "║" # + "│"
                if i == 8:      _pr_ls[i] = _pr_ls[i] + _strek + "╣" # + "┤"
                if i == 9:      _pr_ls[i] = _pr_ls[i] + _space + "║" # + "│"
                if i == 10:     _pr_ls[i] = _pr_ls[i] + _strek + "╣" # + "┤"
                if i == 11:     _pr_ls[i] = _pr_ls[i] + _space + "║" # + "│"
                if i == 12:     _pr_ls[i] = _pr_ls[i] + _strek + "╣" # + "┤"
                if i == 13:     _pr_ls[i] = _pr_ls[i] + _strek + "╣" # + "┤"
                if i == 14:     _pr_ls[i] = _pr_ls[i] + _STREK + "╝" # + "┘" # Siste linje

            if _oppg_typ == "Eksamen":

                if i == 0:      _pr_ls[i] = _pr_ls[i] + _STREK + "╗" # + "┐"
                if i == 1:      _pr_ls[i] = _pr_ls[i] + _space + "║" # + "│"
                if i == 2:      _pr_ls[i] = _pr_ls[i] + _strek + "╣" # + "┤"
                if i == 3:      _pr_ls[i] = _pr_ls[i] + _space + "║" # + "│"
                if i == 4:      _pr_ls[i] = _pr_ls[i] + _strek + "╣" # + "┤"
                if i == 5:      _pr_ls[i] = _pr_ls[i] + _space + "║" # + "│"
                if i == 6:      _pr_ls[i] = _pr_ls[i] + _strek + "╣" # + "┤"
                if i == 7:      _pr_ls[i] = _pr_ls[i] + _space + "║" # + "│"
                if i == 8:      _pr_ls[i] = _pr_ls[i] + _strek + "╣" # + "┤"
                if i == 9:      _pr_ls[i] = _pr_ls[i] + _space + "║" # + "│"
                if i == 10:     _pr_ls[i] = _pr_ls[i] + _strek + "╣" # + "┤"
                if i == 11:     _pr_ls[i] = _pr_ls[i] + _space + "║" # + "│"
                if i == 12:     _pr_ls[i] = _pr_ls[i] + _strek + "╣" # + "┤"
                if i == 13:     _pr_ls[i] = _pr_ls[i] + _space + "║" # + "┤"
                if i == 14:     _pr_ls[i] = _pr_ls[i] + _strek + "╣" # + "┘"
                if i == 15:     _pr_ls[i] = _pr_ls[i] + _strek + "║" # + "┘"
                if i == 16:     _pr_ls[i] = _pr_ls[i] + _STREK + "╝" # + "┘" # Siste linje

    _debug_col = 3
    if _debug_col == 0:
        for pr in _pr_ls: print(pr)
    if _debug_col == 1:
        for pr in _pr_ls: print(f"{pr} {len(pr)}")

    _col_ls = list()
    if _debug_col == 3:
        for i in range(len(_pr_ls)):

            from colorama import Fore, Style

            if _is_colors == 0: _col_ls.append(f"{_pr_ls[i]}")
            if _is_colors == 1: _col_ls.append(f"{Fore.RED}{_pr_ls[i]}")

            def colo(typ):

                if _is_colors == 0: return ""

                if _is_colors == 1:

                    if typ == "r":

                        if _col_ramme   == 2: return Fore.BLUE
                        if _col_ramme   == 3: return Fore.RED

                    if typ == "t":

                        if _col_tit     == 1: return Fore.LIGHTWHITE_EX

                    if typ == "u":

                        if _col_uttrykk == 2: return Fore.BLUE

            # Ramme > Single
            _col_ls[i] = str(_col_ls[i]).replace('─', f'{colo("r")}─{colo("u")}')
            _col_ls[i] = str(_col_ls[i]).replace('┌', f'{colo("r")}┌{colo("u")}')
            _col_ls[i] = str(_col_ls[i]).replace('│', f'{colo("r")}│{colo("u")}')
            _col_ls[i] = str(_col_ls[i]).replace('┬', f'{colo("r")}┬{colo("u")}')
            _col_ls[i] = str(_col_ls[i]).replace('└', f'{colo("r")}└{colo("u")}')
            _col_ls[i] = str(_col_ls[i]).replace('┴', f'{colo("r")}┴{colo("u")}')
            _col_ls[i] = str(_col_ls[i]).replace('┤', f'{colo("r")}┤{colo("u")}')
            _col_ls[i] = str(_col_ls[i]).replace('┐', f'{colo("r")}┐{colo("u")}')
            _col_ls[i] = str(_col_ls[i]).replace('├', f'{colo("r")}├{colo("u")}')
            _col_ls[i] = str(_col_ls[i]).replace('┼', f'{colo("r")}┼{colo("u")}')
            _col_ls[i] = str(_col_ls[i]).replace('┘', f'{colo("r")}┘{colo("u")}')

            # Ramme > Dobbel
            _col_ls[i] = str(_col_ls[i]).replace('═', f'{colo("r")}═{colo("u")}')
            _col_ls[i] = str(_col_ls[i]).replace('╩', f'{colo("r")}╩{colo("u")}')
            _col_ls[i] = str(_col_ls[i]).replace('╗', f'{colo("r")}╗{colo("u")}')
            _col_ls[i] = str(_col_ls[i]).replace('║', f'{colo("r")}║{colo("u")}')
            _col_ls[i] = str(_col_ls[i]).replace('╣', f'{colo("r")}╣{colo("u")}')
            _col_ls[i] = str(_col_ls[i]).replace('╝', f'{colo("r")}╝{colo("u")}')

            # Tittel
            _col_ls[i] = str(_col_ls[i]).replace("Eksamen",             f'{colo("t")}Eksamen')
            _col_ls[i] = str(_col_ls[i]).replace("Alle svar",           f'{colo("t")}Alle svar')
            _col_ls[i] = str(_col_ls[i]).replace("Økonomi",             f'{colo("t")}Økonomi')
            _col_ls[i] = str(_col_ls[i]).replace("Pris-funksjon",       f'{colo("t")}Pris-funksjon')
            _col_ls[i] = str(_col_ls[i]).replace("Uttrykk",             f'{colo("t")}Uttrykk')
            _col_ls[i] = str(_col_ls[i]).replace("Inntekt-funksjon",    f'{colo("t")}Inntekt-funksjon')
            _col_ls[i] = str(_col_ls[i]).replace("Størst inntekt",      f'{colo("t")}Størst inntekt')
            _col_ls[i] = str(_col_ls[i]).replace("Enheter",             f'{colo("t")}Enheter')
            _col_ls[i] = str(_col_ls[i]).replace("Pris",                f'{colo("t")}Pris')

    # bld(cmd="clear") # Sjekk Mac / Kanskje lin
    for pr in _col_ls: print(pr)

# Exe
x = mt.Symbol("x")
_exe_okonomi = 0
if _exe_okonomi == 1:

    alle_svar = økonomi(
        p = 79 - 12.2 * mt.ln(x)
    )

_exe_eksamen = 0
if _exe_eksamen == 1:

    def eksamen(p, oppg_typ = "eksamen"):
        def _økonomi(p, oppg_typ):
            alle_svar = økonomi(
                p = 79 - 12.2 * mt.ln(x),
                oppg_typ = oppg_typ
            )
        _økonomi(p = p, oppg_typ = oppg_typ)

    alle_svar = eksamen(
        p = 79 - 12.2 * mt.ln(x)
    )



# Alias > 1
#derivert                        = diff
#momentan_vekst                  = diff
#momentan_vekstfart              = diff

# Alias > 2 > ...
