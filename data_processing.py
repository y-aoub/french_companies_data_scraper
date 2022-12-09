import re
import pandas as pd

# to save df into csv format
def final_data_csv(df, PATH):
    df.to_csv(PATH, sep=";", header=True)


# " " to %20
def replace_space(companies):
    for i in range(len(companies)):
        companies[i] = companies[i].replace(" ", "%20")
    return companies


# %20 to " "
def recover_space(companies):
    for i in range(len(companies)):
        companies[i] = companies[i].replace("%20", " ")
    return companies


# " " to +
def replace_space_duckduckgo(companies):
    for i in range(len(companies)):
        companies[i] = companies[i].replace(" ", "+")
    return companies


# + to " "
def recover_space_duckduckgo(companies):
    for i in range(len(companies)):
        companies[i] = companies[i].replace("+", " ")
    return companies


# abbreviate header
def abbrev_Header(header):
    header = header.replace("Adresse", "adresse")
    header = header.replace("Activité", "activite")
    header = header.replace("Effectif", "effectif")
    header = header.replace("Création", "creation")
    header = header.replace("Dirigeants", "dirigeants")
    header = header.replace("Dirigeant", "dirigeants")
    return header


# abbreviate InfosJuridiques
def abbrev_InfosJuridiques(infos_jurid):
    infos_jurid = infos_jurid.replace("SIRET (siège)", "SIRET")
    infos_jurid = infos_jurid.replace("Forme juridique", "forme_jurid")
    infos_jurid = infos_jurid.replace("TVA intracommunautaire", "TVA_intracommu")
    infos_jurid = infos_jurid.replace("Numéro RCS", "num_RCS")
    infos_jurid = infos_jurid.replace("Capital social", "capital_soc")
    infos_jurid = infos_jurid.replace(
        "Date de clôture d'exercice comptable", "date_cloture_ex_compta"
    )
    infos_jurid = infos_jurid.replace("Inscription au RCS", "inscrip_RCS")
    return infos_jurid


# abbreviate TabFianances
def abbrev_TabFinances(table):
    table = table.replace("Performance", "annee")
    table = table.replace("Chiffre d'affaires (€)", "CA(€)")
    table = table.replace("Marge brute (€)", "marge_brute(€)")
    table = table.replace("EBITDA - EBE (€)", "EBITDA_EBE(€)")
    table = table.replace("Résultat d'exploitation (€)", "res_exploitation(€)")
    table = table.replace("Résultat net (€)", "res_net(€)")
    table = table.replace("Croissance", "croiss")
    table = table.replace("Taux de croissance du CA (%)", "taux_croiss_CA(%)")
    table = table.replace("Taux de marge brute (%)", "taux_marge_brute(%)")
    table = table.replace("Taux de marge d'EBITDA (%)", "taux_marge_EBITA(%)")
    table = table.replace("Taux de marge opérationnelle (%)", "taux_marge_oper(%)")
    table = table.replace("Gestion BFR", "gest_BFR")
    table = table.replace("BFR (€)", "BFR(€)")
    table = table.replace("BFR exploitation (€)", "BFR_exploitation(€)")
    table = table.replace("BFR exploitation (j de CA)", "BFR_exploitation_j_de_CA")
    table = table.replace("BFR hors exploitation (€)", "BFR_hors_exploitation(€)")
    table = table.replace("BFR (j de CA)", "BFR_j_de_CA")
    table = table.replace(
        "BFR hors exploitation (j de CA)", "BFR_hors_exploitation_j_de_CA"
    )
    table = table.replace("Délai de paiement clients (j)", "delai_paie_client_j")
    table = table.replace("Délai de paiement fournisseurs (j)", "delai_paie_fourn_j")
    table = table.replace("Ratio des stocks / CA (j)", "ratio_stocks/CA_j")
    table = table.replace("Autonomie financière (%)", "autonomie_fin(%)")
    table = table.replace("Autonomie financière", "autonomie_fin")
    table = table.replace("Capacité d'autofinancement (€)", "capacite_autofin(€)")
    table = table.replace(
        "Capacité d'autofinancement / CA (%)", "capacite_autofin/CA(%)"
    )
    table = table.replace(
        "Fonds de roulement net global (€)", "fond_roulement_net_glob(€)"
    )
    table = table.replace("Couverture du BFR", "couverture_BFR")
    table = table.replace("Trésorerie (€)", "tresor(€)")
    table = table.replace("Dettes financières (€)", "dettes_fin(€)")
    table = table.replace("Capacité de remboursement", "capacite_remb")
    table = table.replace("Ratio d'endettement (Gearing)", "ratio_endet")
    table = table.replace("Taux de levier (DFN/EBITDA)", "taux_levier")
    table = table.replace("Solvabilité", "solvab")
    table = table.replace(
        "Etat des dettes à un an au plus (€)", "etat_dettes_1an_au_plus(€)"
    )
    table = table.replace("Liquidité générale", "liq_generale")
    table = table.replace("Couverture des dettes", "couv_dettes")
    table = table.replace("Rentabilité sur fonds propres (%)", "rentab_fonds_prop(%)")
    table = table.replace("Rentabilité économique (%)", "rentab_eco(%)")
    table = table.replace("Rentabilité", "rentab")
    table = table.replace("Marge nette (%)", "marge_nette(%)")
    table = table.replace("Valeur ajoutée (€)", "val_ajoutee")
    table = table.replace("Valeur ajoutée / CA (%)", "val_ajoutee/CA(%)")
    table = table.replace("Structure d'activité", "struc_activite")
    table = table.replace(
        "Salaires et charges sociales (€)", "salaires_et_charges_soc(€)"
    )
    table = table.replace("Salaires / CA (%)", "salaires/CA(%)")
    table = table.replace("Impôts et taxes (€)", "impo_taxes(€)")
    return table


# divide text into lines and add all lines to a list
def txt_to_list(infos):
    infos = infos.split("\n")
    infos = [infos[i].strip() for i in range(len(infos))]
    return infos

# to delete redundants in TabFinances
def del_redundants(table, TabFinances):
    redundants = [
        "croiss",
        "gest_BFR",
        "autonomie_fin",
        "solvab",
        "rentab",
        "struc_activite",
    ]
    for elem in TabFinances:
        L = elem.split(" ")
        if L[0] in redundants:
            TabFinances.remove(elem)
    return table


# formatting the extracted data and add missing columns in the webdriver (example: CA_2016 missing for some companies)
def infos_to_df(table, InfosHeader, InfosJuridiques, TabFinances, NomEntreprise):
    if table == InfosHeader:
        dic_infos_header = {
            elem.split(" : ")[0]: elem.split(" : ")[1:] for elem in table
        }
        data_infos_header = pd.DataFrame.from_dict(dic_infos_header, orient="index")
        data_infos_header = data_infos_header.transpose()
        data_infos_header.insert(0, "nom_entreprise", NomEntreprise, True)
        return data_infos_header

    elif table == InfosJuridiques:
        dic_infos_jurid = {
            elem.split(" : ")[0]: elem.split(" : ")[1:] for elem in table
        }
        data_infos_jurid = pd.DataFrame.from_dict(dic_infos_jurid, orient="index")
        data_infos_jurid = data_infos_jurid.transpose()
        return data_infos_jurid

    elif table == TabFinances:
        dic_tab_fin = {elem.split(" ")[0]: elem.split(" ")[1:] for elem in table}
        data_tab_fin = pd.DataFrame.from_dict(dic_tab_fin, orient="index")
        data_tab_fin = data_tab_fin.transpose()
        data_tab_fin = data_tab_fin.set_index(data_tab_fin.columns[0])
        reorderlist = ["2021", "2020", "2019", "2018", "2017", "2016"]
        data_tab_fin = data_tab_fin.reindex(reorderlist)

        len_row = len(data_tab_fin.index)
        len_column = len(data_tab_fin.columns)
        dico = {
            data_tab_fin.columns[j]
            + "_"
            + data_tab_fin.index[i]: data_tab_fin.loc[
                data_tab_fin.index[i], data_tab_fin.columns[j]
            ]
            for i in range(len_row)
            for j in range(len_column)
        }
        new_data_tab_fin = pd.DataFrame.from_dict(dico, orient="index")
        new_data_tab_fin = new_data_tab_fin.transpose().sort_index(
            axis=1, ascending=False
        )
        new_data_tab_fin
        return new_data_tab_fin


# to concatenate infos_header_data, data_infos_jurid, data_tab_fin
def concat_data_entreprise(data_infos_header, data_infos_jurid, data_tab_fin):
    data_entrep = pd.concat([data_infos_header, data_infos_jurid, data_tab_fin], axis=1)
    data_entrep = data_entrep.set_index(data_entrep.columns[0])
    return data_entrep


# delete hiden profils (LinkedIn Member)
def del_linkedin_member(data):
    for i in data.index:
        if "LinkedIn" in data.loc[i, "nom"]:
            data = data.drop(index=[i])
    return data
