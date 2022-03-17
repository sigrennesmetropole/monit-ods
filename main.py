# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import sys
from owslib.csw import CatalogueServiceWeb
from owslib.fes import PropertyIsEqualTo, PropertyIsLike
from owslib.util import openURL
import re



CswCatalogUrl = "https://public.sig.rennesmetropole.fr/geonetwork/srv/fre/csw"
OdsUrl = "https://data.rennesmetropole.fr/explore/dataset/"


def get_all_records():
    """
    Gets all records, also managing the pagination against the remote CSW server.
    :param constraint: the constraint array to be passed to OWSLib getrecords2.
    :return: a hashmap with UUID as key, the parsed metadata as value.
    """
    startpos = 0
    max_records = 100
    mds = {}
    while True:
        csw.getrecords2(constraints=[is_dataset,ods_filter],
                        esn='full',
                        #outputschema=namespaces['gmd'],
                        startposition=startpos,
                        maxrecords=max_records)

        for uuid in csw.records:
            mds[uuid] = csw.records[uuid]
        startpos = len(mds) + 1
        # end condition
        if csw.results['nextrecord'] == 0:
            break
    return mds




# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # définition du catalogue CSW à interroger
    csw = CatalogueServiceWeb(CswCatalogUrl)

    # on filtre
    global is_dataset
    is_dataset = PropertyIsEqualTo("Type", "dataset")
    global ods_filter
    ods_filter = PropertyIsLike('dc:linkage', '%data.rennesmetropole.fr%')
    #ods_filter = PropertyIsLike('any', '%arbres%')


    print("récupération des uuid de toutes les métadonnées")
    mds = get_all_records()
    print("")
    print("fait : " + str(len(mds)) + " métadonnées trouvées")

    print("")
    print("raz du fichier de config monit")
    f = open("check_hosts_rm_ods", "w")
    f.write("\n# check host OpenDataSoft Rennes Métropole\n\n")

    print("")
    print("boucle sur toutes les md")
    print("")

    cpt = 0
    for uuid in mds:
        #print(uuid)

        MDraw = openURL("https://public.sig.rennesmetropole.fr/geonetwork/srv/fre/csw?service=CSW&version=2.0.2&request=GetRecordById&ElementSetName=full"
                        + f"&id={uuid}")
        # on transforme en texte brut
        content = str(MDraw.read())

        try:
            match = re.findall(r"(\/explore\/dataset\/)([a-z0-9_-]*)", str(content))
            # le résultat est une liste dans un tuple
            list = match[0]
            ods_id = list[1]
            #print(ods_id)

            print(f" {uuid} -> {ods_id}")

            # on écrit dans le fichier de conf pour monit
            f.write(f"""
    check host {ods_id}
      with address data.rennesmetropole.fr
      every "0 7-18 * * *"
      if failed
        port 443
        protocol https
        request /explore/dataset/{ods_id}/information/
        status = 200
      then alert
    """)

        except:
            print(f" {uuid} >>>>>> PAS DE LIEN ODS ")

        cpt += 1
        #if cpt == 3:
        #    break


    # on ferme le fichier
    f.close()

    print("")
    print("FIN")