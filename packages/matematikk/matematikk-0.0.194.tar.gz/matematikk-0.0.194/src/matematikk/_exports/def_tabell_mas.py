# 🚀 programmering.no | 🤓 matematikk.as

import matematikk as mt

def tabell_print_kolonne_padding(txt):

    # Padder celle-breddene i tabellen med white space  (lik bredde)
    _txt = str(txt)
    for _ in range(tab_bredde - len(str(_txt))):
        _txt += " "
    return _txt

def tabell_print_rad(tab_mat, i):

    # Rader (i) og kolonner (j)
    _kolonne = ""
    for j in range(len(tab_mat)):
        _kolonne += "|" + " " + "" + tabell_print_kolonne_padding(tab_mat[j][i])
    print(_kolonne)

def tabell_print(
        tab_mat         = [[], []],
        tab_print_1_start     = 0,
        tab_print_1_slutt     = 0,
        tab_print_2_start     = 0,
        tab_print_2_slutt     = 0,
        n_periode       = int()
    ):

    # Devx-setting for rask debug
    _devx_alle_rader = 0

    # DEV > Hardkodet variabel-navn > Variabler
    _n_periode = mt.sjekk_datatype(vari_navn = "n_periode", vari = n_periode, typ = int)

    # Print header
    tabell_print_rad(tab_mat, 0)

    # Print rader
    for i in range(1, _n_periode + 1):

        # Devx > Utvalgte rader
        if _devx_alle_rader == 0:

            # Print tabell-rad (begrenset rader)
            if i >= tab_print_1_start and i <= tab_print_1_slutt: tabell_print_rad(tab_mat, i)
            if i >= tab_print_2_start and i <= tab_print_2_slutt: tabell_print_rad(tab_mat, i)

        # Devx > Alle rader
        if _devx_alle_rader == 1: tabell_print_rad(tab_mat, i)

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
        tab_mat             = [[], []],
        tab_desimal         = -1,
        tab_print           = 1,
        tab_print_1_start         = -1,
        tab_print_1_slutt         = -1,
        tab_print_2_start         = -1,
        tab_print_2_slutt         = -1,
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
    if (tab_print       == 1 and
        tab_print_1_start     == -1 and
        tab_print_1_slutt     == -1 and
        tab_print_2_start     == -1 and
        tab_print_2_slutt     == -1):
            tab_print_1_start     = 0
            tab_print_1_slutt     = n_periode

    # Resetting
    _blokk_         = 1
    _tab_mat        = tab_mat
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
                _tab_ret_mat[j]     = copy.deepcopy(mat_format[0])
                mat_format[0]       = copy.deepcopy(mat_data[j])

            if mat_data[j][0] == "År":
                _tab_ret_mat[j]     = copy.deepcopy(mat_format[1])
                mat_format[1]       = copy.deepcopy(mat_data[j])

            if mat_data[j][0] == "Innskudd":
                _tab_ret_mat[j]     = copy.deepcopy(mat_format[2])
                mat_format[2]       = copy.deepcopy(mat_data[j])

            if mat_data[j][0] == "Innskudd d":
                _tab_ret_mat[j]     = copy.deepcopy(mat_format[3])
                mat_format[3]       = copy.deepcopy(mat_data[j])

            if mat_data[j][0] == "B (start)":
                _tab_ret_mat[j]     = copy.deepcopy(mat_format[4])
                mat_format[4]       = copy.deepcopy(mat_data[j])

            if mat_data[j][0] == "B (slutt)":
                _tab_ret_mat[j]     = copy.deepcopy(mat_format[5])
                mat_format[5]       = copy.deepcopy(mat_data[j])

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
        _b_slutt = _b_start * v_mi

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
            tab_mat         = _tab_ret_mat,
            tab_print_1_start     = tab_print_1_start,
            tab_print_1_slutt     = tab_print_1_slutt,
            tab_print_2_start     = tab_print_2_start,
            tab_print_2_slutt     = tab_print_2_slutt,
            n_periode       = _n_periode
        )

    return _tab_ret_mat



# Alias > 1
tabell_okonomi_lag = tabell_økonomi_lag

# Alias > 2 > ...

