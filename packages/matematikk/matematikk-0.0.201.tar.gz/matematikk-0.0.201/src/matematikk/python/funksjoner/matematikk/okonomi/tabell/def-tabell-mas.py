# 🚀 programmering.no | 🤓 matematikk.as

import matematikk as mt

def tabell_print_effekt(n_perioder = 10, mat_fx = []):

    # Effekt
    _typ = str()
    if mat_fx != []: _typ = mat_fx[0]   # Hvilken effekt (foreløpig kun "matrix")
    if mat_fx == []: _typ = "matrix"    # Default

    # Matrix effekt
    if _typ == "matrix":

        # Perioder
        _n_perioder = n_perioder

        # Resett mat
        _mat_fx = []

        # Default settings
        if mat_fx == []:
                _mat_fx.append([                # Liste med japanske symbol (jp-sym) som hentes frem tilfeldig (alleer dobbelt så lange som vanlige char)
                    "グ", "ケ", "ゲ", "コ", "ゴ", "サ", "ザ", "シ", "ジ", "ス", "ズ", "セ", "ゼ", "ソ", "ゾ", "タ"
                ])
                _mat_fx.append(["0", "1"])      # Liste med 0 og 1 som blandes med jp-sym
                _mat_fx.append([                # Filter-parametre som gir en tilfeldig, dynamisk blanding mellom to lister (se nedenfor): 3 i dette scopet og 4 som argumenter inn i tabell
                    1.00, 0.10, 0.60, 0.80, 0.99, 0.10, 0.99
                ])
                _mat_fx.append(700000 / 10)     # Gjør at flere el kommer etter hverandre (startet med 692 852 som er ca. 700 000 / 140 = 5000 el etter hverandre)
                _mat_fx.append(692852)

        # Egne argumenter: Kun alle 4 elementene eller ingen (default)
        if mat_fx != []:
                _mat_fx.append(mat_fx[1])
                _mat_fx.append(mat_fx[2])
                _mat_fx.append(mat_fx[3])
                _mat_fx.append(mat_fx[4])

        # Argumenter
        matrix_jp_ls        = _mat_fx[0]
        matrix_null_en_ls   = _mat_fx[1]
        matrix_f_ls         = _mat_fx[2]
        matrix_cut_off      = _mat_fx[3]

        # Nullstill matrix-lister
        _matrix_jp_mix_ls   = []
        _matrix_null_ls     = []
        _matrix_jp_null_ls  = []

        # Filter > Sekvens med like js-sym etter hverandre blandet med tilfeldige
        j = 0
        k = 1 # Enten 1 (i intervall med like etter hverandre)
        m = 0
        for i in range(_n_perioder):

            # Sekvens med f.eks. 5000 jp-sym etter hverandre
            if k == 1:
                _r                                      = mt.random.randint(len(matrix_jp_ls)) # Sekvensen blandes med noen tilfeldige jp-sym
                if mt.random.random() > matrix_f_ls[0]:    _matrix_jp_mix_ls.append(f"{matrix_jp_ls[m]}") # m plukker samme jp-sym for 2 sekvenser
                else:                                   _matrix_jp_mix_ls.append(f"{matrix_jp_ls[_r]}")

            # Sekvens med f.eks. 5000 white space
            if k == 2:                                  _matrix_jp_mix_ls.append("  ") # Dobbel-space pga. jp-sym tar 2 plasser

            if j > 0    and j <= matrix_cut_off:                k = 1 # k er 1 så lenge j er i den 1. sekvensen
            if j > matrix_cut_off and j < matrix_cut_off * 2:   k = 2 # k blir 2 når j går over i den 2. sekvensen
            if j == matrix_cut_off * 2:
                j                                       = 0 # j nullstilles når den når 3. sekvens
                m                                       = mt.random.randint(len(matrix_jp_ls)) # m blir en ny tilfeldig index for et nytt jp-sym
            j                                           += 1    # j øker alltid med 1 og nullstilles for hver 3. sekvens

        # Filter > 0 blandet med 1
        for i in range(_n_perioder):
            if mt.random.random() > matrix_f_ls[1]:    _matrix_null_ls.append(f" {matrix_null_en_ls[0]}") # Dobbel-space pga. jp-sym tar 2 plasser
            else:                                   _matrix_null_ls.append(f" {matrix_null_en_ls[1]}") # -"-

        # Filter > jp blandet med 0 og 1
        for i in range(_n_perioder):
            if mt.random.random() > matrix_f_ls[2]:    _matrix_jp_null_ls.append(_matrix_jp_mix_ls[i])
            else:                                   _matrix_jp_null_ls.append(_matrix_null_ls[i])

        # Videre som argument inn i tabell
        _mat_matrix = ["matrix", _matrix_jp_null_ls, [0], matrix_f_ls] # (*) Trenger kun ett [0] som øker med belop_start_ink_he

    return _mat_matrix

def tabell_print_farge(txt = str(), tab_farge_typ = str()):

    # Farge
    if tab_farge_typ == "blå":          return f"{mt.Fore.BLUE}      {txt}{mt.Style.RESET_ALL}"
    if tab_farge_typ == "grønn":        return f"{mt.Fore.GREEN}     {txt}{mt.Style.RESET_ALL}"
    if tab_farge_typ == "magentea":     return f"{mt.Fore.MAGENTA}   {txt}{mt.Style.RESET_ALL}"
    if tab_farge_typ == "rød":          return f"{mt.Fore.RED}       {txt}{mt.Style.RESET_ALL}"
    if tab_farge_typ == "gul":          return f"{mt.Fore.YELLOW}    {txt}{mt.Style.RESET_ALL}"

    # Ingen farge (bypass) 
    return txt

def tabell_print_kolonne_padding(txt = str(), tab_bredde = int(), tab_fx = []):

    # Effekt
    if tab_fx != []:

        # Matrix-effekt: Foreløpig ingen advarsler default hvis ukjent effekt
        if tab_fx[0] == "matrix":

            # Padder celle-breddene i tabellen med white space (lik bredde)
            _txt                                        = str(txt)
            _bredde_diff                                = tab_bredde - len(str(_txt))
            for _ in range(_bredde_diff):               _txt += " "

            # Varierer posisjonen hvor matrix-sym skrives mellom 9 og 10
            _posisjon = int()
            if mt.random.random() > tab_fx[3][3]:      _posisjon = 10
            else:                                       _posisjon = 9

            # "Pulserende treshhold"-verdi som demper og forsterker (mer statisk uten)
            if mt.random.random() > tab_fx[3][4]:      _tresh = tab_fx[3][5]
            else:                                       _tresh = tab_fx[3][6]

            if mt.random.random() > _tresh: # _tresh:
                _ran_1 = mt.random.randint(4, 6)           # (4, 7) er mer bredde-variasjon for matrix-sym, men blir mer intens
                if _bredde_diff > _posisjon:
                    _txt = _txt[:_ran_1] + str(tab_fx[1][0]) + _txt[_ran_1 + 2:]
                _k      = tab_fx[2][0]              # (*) Det økende elementet fra while-løkken
                _el     = tab_fx[1][_k]             # Henter frem neste matrix-sym i matrisen
                _txt    = _txt.replace("      ", f"    {_el}", 1) # Bytter ut tomrom med matrix-sym

            return _txt

    # Ingen effekt
    if tab_fx == []:

        # Padder celle-breddene i tabellen med white space  (lik bredde)
        _txt    = str(txt)
        _rang   = tab_bredde - len(str(_txt))
        for _ in range(_rang): _txt += " "

        return _txt

def tabell_print_rad(tab_mat = [], i = int(), tab_bredde = int(), tab_is_farge = -1, tab_farge_typ = str(), tab_fx = []):

    # Rader (i) og kolonner (j)
    _kolonne = ""
    for j in range(len(tab_mat)):
        _kolonne += "|" + " " + "" + tabell_print_kolonne_padding(txt = tab_mat[j][i], tab_bredde = tab_bredde, tab_fx = tab_fx)

    # Farge
    if tab_is_farge == 1: _kolonne = tabell_print_farge(txt = _kolonne, tab_farge_typ = tab_farge_typ)

    # Print
    print(_kolonne)

def tabell_print(
        tab_mat                 = [[], []],
        tab_print_1_start       = 0,
        tab_print_1_slutt       = 0,
        tab_print_2_start       = 0,
        tab_print_2_slutt       = 0,
        tab_bredde              = int(),
        tab_is_farge            = -1,
        tab_farge_typ           = str(),
        tab_fx              = [],
        n_periode               = int()
    ):

    # Devx-setting for rask debug
    _devx_alle_rader = 0

    # DEV > Hardkodet variabel-navn > Variabler
    _n_periode = mt.sjekk_datatype(vari_navn = "n_periode", vari = n_periode, typ = int)

    # Print header
    tabell_print_rad(tab_mat = tab_mat, i = 0, tab_bredde = tab_bredde, tab_is_farge = tab_is_farge, tab_farge_typ = tab_farge_typ, tab_fx = [])

    # Print rader
    for i in range(1, _n_periode + 1):

        # Devx > Utvalgte rader
        if _devx_alle_rader == 0:

            # Print tabell-rad (begrenset rader) > Matrix
            if i >= tab_print_1_start and i <= tab_print_1_slutt:
                tabell_print_rad(tab_mat = tab_mat, i = i, tab_bredde = tab_bredde, tab_is_farge = tab_is_farge, tab_farge_typ = tab_farge_typ, tab_fx = tab_fx)
            if i >= tab_print_2_start and i <= tab_print_2_slutt:
                tabell_print_rad(tab_mat = tab_mat, i = i, tab_bredde = tab_bredde, tab_is_farge = tab_is_farge, tab_farge_typ = tab_farge_typ)

        # Devx > Alle rader
        if _devx_alle_rader == 1: tabell_print_rad(tab_mat = tab_mat, i = i, tab_bredde = tab_bredde, tab_is_farge = tab_is_farge, tab_farge_typ = tab_farge_typ)

def tabell_finn_el(tab_mat, i_pos, j_pos_header):

    # Sjekk datatype
    _i_pos = mt.sjekk_datatype(vari_navn = "i_pos", vari = i_pos, typ = int)

    # Finn elementet
    for j in range(len(tab_mat)):
        if tab_mat[j][0] == j_pos_header:
            return tab_mat[j][_i_pos]

    # Hvis ikke finner elementet
    return None

def tabell_økonomi_lag(
        tab_bredde          = int(),
        tab_mat             = [[], []],
        tab_desimal         = -1,
        tab_print           = 1,
        tab_print_1_start   = -1,
        tab_print_1_slutt   = -1,
        tab_print_2_start   = -1,
        tab_print_2_slutt   = -1,
        tab_is_farge        = -1,
        tab_farge_typ       = -1,
        tab_fx          = [],
        vf                  = float(),
        n_periode           = int(),
        aar_start           = int(),
        innskudd            = float(),
        innskudd_desimal    = -1,
        innskudd_d          = float(),
        innskudd_d_desimal  = -1,
        b_start_desimal     = -1,
        b_slutt_desimal     = -1
    ):

    # Print
    if (tab_print               == 1 and
        tab_print_1_start       == -1 and
        tab_print_1_slutt       == -1 and
        tab_print_2_start       == -1 and
        tab_print_2_slutt       == -1):
            tab_print_1_start     = 0
            tab_print_1_slutt     = n_periode

    # Resetting
    _blokk_         = 1
    _tab_mat        = tab_mat
    _vf             = vf
    _n_periode      = mt.sjekk_datatype(vari_navn = "n_periode", vari = n_periode, typ = int)
    _aar            = mt.sjekk_datatype(vari_navn = "aar", vari = aar_start, typ = int)
    _innskudd       = innskudd
    _innskudd_d     = innskudd_d
    _b_start        = _innskudd

    # Format
    _debug_mat      = 0
    _tab_size       = 6
    _tab_f_mat      = []
    _tab_ret_mat    = []
    for i in range(_tab_size):
        _tab_f_mat.append([])
        _tab_ret_mat.append([])

    # Lager midlertidig formatert matrise av matrise med data
    def mat_ops(typ, mat_data, mat_format):

        # _tab_ret_mat må være øverst for siste format
        for j in range(len(mat_data)):
            if mat_data[j][0] == "Periode":
                _tab_ret_mat[j]     = mt.deepcopy(mat_format[0])
                mat_format[0]       = mt.deepcopy(mat_data[j])

            if mat_data[j][0] == "År":
                _tab_ret_mat[j]     = mt.deepcopy(mat_format[1])
                mat_format[1]       = mt.deepcopy(mat_data[j])

            if mat_data[j][0] == "Innskudd":
                _tab_ret_mat[j]     = mt.deepcopy(mat_format[2])
                mat_format[2]       = mt.deepcopy(mat_data[j])

            if mat_data[j][0] == "Innskudd d":
                _tab_ret_mat[j]     = mt.deepcopy(mat_format[3])
                mat_format[3]       = mt.deepcopy(mat_data[j])

            if mat_data[j][0] == "B (start)":
                _tab_ret_mat[j]     = mt.deepcopy(mat_format[4])
                mat_format[4]       = mt.deepcopy(mat_data[j])

            if mat_data[j][0] == "B (slutt)":
                _tab_ret_mat[j]     = mt.deepcopy(mat_format[5])
                mat_format[5]       = mt.deepcopy(mat_data[j])

        if typ == 1: return mat_format
        if typ == 2: return _tab_ret_mat

    _tab_f_mat = mat_ops(1, _tab_mat, _tab_f_mat)

    # Debug
    if _debug_mat == 1:
        print(""); print("debug > format - header ::")
        for j in range(len(_tab_f_mat)): print(_tab_f_mat[j])

    # For-løkke som regner ut tabell-verdiene
    for i in range(1, _n_periode + 1):

        # Regner ut slutt-beløpet med vekstfaktor (avrundet)
        _b_slutt = _b_start * _vf

        # Periode (n)
        if _blokk_ == 1:

            # Tabell > Legg verdier i matrisen
            _tab_f_mat[0].append(i)

        # År
        if _blokk_ == 1:

            _tab_f_mat[1].append(_aar)

        # Innskudd
        if _blokk_ == 1:

            # Avrunding
            if innskudd_desimal != -1: _innskudd = round(_innskudd, innskudd_desimal)

            # Legger verdien i matrisen
            _tab_f_mat[2].append(_innskudd)

        # Innskudd d
        if _blokk_ == 1:

            # Avrunding
            if innskudd_d_desimal != -1: _innskudd_d = round(_innskudd_d, innskudd_d_desimal)

            # Legger verdien i matrisen
            _tab_f_mat[3].append(_innskudd_d)

        # Beløp (start)
        if _blokk_ == 1:

            # Avrunding
            if b_start_desimal != -1: _b_start = round(_b_start, b_start_desimal)

            # Legger verdien i matrisen
            _tab_f_mat[4].append(_b_start)

        # Beløp (slutt)
        if _blokk_ == 1:

            # Avrunding
            if b_slutt_desimal != -1: _b_slutt = round(_b_slutt, b_slutt_desimal)

            # Legger verdien i matrisen
            _tab_f_mat[5].append(_b_slutt)

        # Inkrement variabler
        _aar            += 1
        _innskudd       += _innskudd_d
        _b_start        = _b_slutt + _innskudd

    # Avrunding > Hele tabellen
    if tab_desimal != -1:
        for j in range(len(_tab_f_mat)):
            for i in range(len(_tab_f_mat[j])):
                if i > 0: _tab_f_mat[j][i] = round(_tab_f_mat[j][i], tab_desimal)

    # Debug
    if _debug_mat == 1:
        print(""); print("debug > format ::")
        for j in range(len(_tab_f_mat)): print(_tab_f_mat[j])

    # Lag return-mat som innkommende data-mat
    _tab_ret_mat = mat_ops(2, _tab_mat, _tab_f_mat)

    # Fjern tomme kolonner
    for j in range(len(_tab_ret_mat)):
        if _tab_ret_mat[j] == []: _tab_ret_mat.pop(j)

    # Debug
    if _debug_mat == 1:
        print(""); print("debug > ret ::")
        for j in range(len(_tab_ret_mat)): print(_tab_ret_mat[j])

    # Print tabell
    if tab_print == 1:
        tabell_print(
            tab_mat                 = _tab_ret_mat,
            tab_print_1_start       = tab_print_1_start,
            tab_print_1_slutt       = tab_print_1_slutt,
            tab_print_2_start       = tab_print_2_start,
            tab_print_2_slutt       = tab_print_2_slutt,
            tab_bredde              = tab_bredde,
            tab_fx              = tab_fx,
            tab_is_farge            = tab_is_farge,
            tab_farge_typ           = tab_farge_typ,
            n_periode               = _n_periode,
        )

    return _tab_ret_mat


# Alias > 1
tabell_okonomi_lag = tabell_økonomi_lag

# Alias > 2 > ...

