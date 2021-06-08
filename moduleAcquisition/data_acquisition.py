import glob
import json
import os
import shutil
from datetime import datetime

import pytesseract
from pdf2image import convert_from_path

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1
from pytesseract import Output
import re


def run_convert_code():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    textJson = []
    entries = os.listdir('../files/pdf')
    source_file = ''
    text = ''
    date = ''

    # recuperation du chemin de chaque doc pdf dans le dossier
    for pdf_path in entries:
        source_file = pdf_path
        try:
            images = convert_from_path('../files/pdf/' + pdf_path, poppler_path=r'C:\poppler-21.03.0\Library\bin')
            list_images = images[0]
            ocr_dict = pytesseract.image_to_data(list_images, lang='eng', output_type=Output.DICT)
            text1 = " ".join(ocr_dict['text'])

            file = open('../files/pdf/' + pdf_path, 'rb')
            parser = PDFParser(file)
            document = PDFDocument(parser)
            if resolve1(document.catalog['Pages'])['Count'] > 1:
                pil_im1 = images[1]
                ocr_dict1 = pytesseract.image_to_data(pil_im1, lang='eng', output_type=Output.DICT)
                text2 = " ".join(ocr_dict1['text'])
            else:
                text2 = ''
            text = text1 + text2

            jour = re.search("(lundi|mardi|Mercredi|mércredi|jeudi|vendredi|samedi|dimanche)", text, re.IGNORECASE)

            pat = r"\W*([\w]+)"
            n = 3
            groups = re.search(r'{}\W*{}{}'.format(pat * n, str(jour.group(0)), pat * n), text, re.IGNORECASE).groups()
            date_input = str(groups[n:][0]) + '-' + str(groups[n:][1]).lower() + '-' + str(groups[n:][2])
            if len(str(groups[n:][0])) < 2:
                journ = '0' + str(groups[n:][0])
            else:
                journ = str(groups[n:][0])
            if str(groups[n:][1]).lower() == 'janvier':
                mois = '01'
            if str(groups[n:][1]).lower() == 'février':
                mois = '02'
            if str(groups[n:][1]).lower() == 'mars':
                mois = '03'
            if str(groups[n:][1]).lower() == 'avril':
                mois = '04'
            if str(groups[n:][1]).lower() == 'mai':
                mois = '05'
            if str(groups[n:][1]).lower() == 'juin':
                mois = '06'
            if str(groups[n:][1]).lower() == 'juillet':
                mois = '07'
            if str(groups[n:][1]).lower() == 'août':
                mois = '08'
            if str(groups[n:][1]).lower() == 'septembre':
                mois = '09'
            if str(groups[n:][1]).lower() == 'octobre':
                mois = '10'
            if str(groups[n:][1]).lower() == 'novembre':
                mois = '11'
            if str(groups[n:][1]).lower() == 'décembre':
                mois = '12'
            date = journ + '/' + mois + '/' + str(groups[n:][2])

        except Exception as e:
            print('petit probleme')

        cas_positifs = re.search(r'(\w+\s+){0,3}sont revenus positifs(\w+\s+){0,3}', text, re.IGNORECASE)
        if cas_positifs:
            pos_num = str(cas_positifs.group(0))
            cas_positifs_nums = [int(s) for s in pos_num.split() if s.isdigit()]
            if not cas_positifs_nums:
                cas_positifs_nums = [0]
        else:
            cas_positifs_nums = [0]

        cas_importes = re.search(r'(\w+\s+){0,3}cas importés(\w+\s+){0,3}', text, re.IGNORECASE)
        if cas_importes:
            imp_num = str(cas_importes.group(0))
            cas_importes_nums = [int(s) for s in imp_num.split() if s.isdigit()]
            if not cas_importes_nums:
                cas_importes_nums = [0]
        else:
            cas_importes_nums = [0]

        cas_contacts = re.search(r'(\w+\s+){0,3}cas contacts(\w+\s+){0,3}', text, re.IGNORECASE)
        if cas_contacts:
            cont_num = str(cas_contacts.group(0))
            cas_contacts_nums = [int(s) for s in cont_num.split() if s.isdigit()]
            if not cas_contacts_nums:
                cas_contacts_nums = [0]
        else:
            cas_contacts_nums = [0]

        tests_realises = re.search(r'(\w+\s+){0,3}tests réalisés(\w+\s+){0,3}', text, re.IGNORECASE)
        if tests_realises:
            test_num = str(tests_realises.group(0))
            if tests_realises.group(0) is not None:
                cas_test_nums = [int(s) for s in test_num.split() if s.isdigit()]
                if not cas_test_nums:
                    cas_test_nums = [0]
        else:
            cas_test_nums = [0]

        sous_traitement = re.search(r'(\w+\s+){0,3}sous traitement(\w+\s+){0,3}', text, re.IGNORECASE)
        if sous_traitement:
            trait_num = str(sous_traitement.group(0))
            cas_sous_traitement_nums = [int(s) for s in trait_num.split() if s.isdigit()]
            if not cas_sous_traitement_nums:
                cas_sous_traitement_nums = [0]
        else:
            cas_sous_traitement_nums = [0]

        contacts_suivis = re.search(r'(\w+\s+){0,3}contacts suivis(\w+\s+){0,3}', text, re.IGNORECASE)
        if contacts_suivis:
            suivi_num = str(contacts_suivis.group(0))
            cas_contacts_suivis_nums = [int(s) for s in suivi_num.split() if s.isdigit()]
            if not cas_contacts_suivis_nums:
                cas_ccontacts_suivis_nums = [0]
        else:
            cas_contacts_suivis_nums = [0]

        cas_communautaires = re.search(r'(\w+\s+){0,12} communautaire(\w+\s+){0,3}', text, re.IGNORECASE)
        if cas_communautaires:
            comm_num = str(cas_communautaires.group(0))
            cas_communautaires_nums = [int(s) for s in comm_num.split() if s.isdigit()]
            if not cas_communautaires_nums:
                cas_communautaires_nums = [0]
        else:
            cas_communautaires_nums = [0]

        cas_gueris = re.search(r'(\w+\s+){0,6}négatifs et déclarés guéris(\w+\s+){0,3}', text, re.IGNORECASE)
        if cas_gueris:
            gueris_num = str(cas_gueris.group(0))
            cas_gueris_nums = [int(s) for s in gueris_num.split() if s.isdigit()]
        else:
            cas_gueris_nums = [0]

        cas_deces = re.search(r'(\w+\s+){0,10}décès(\w+\s+){0,10}', text, re.IGNORECASE)
        if cas_deces:
            deces_num = str(cas_deces.group(0))
            cas_deces_nums = [int(s) for s in deces_num.split() if s.isdigit()]
            if not cas_deces_nums:
                cas_deces_nums = [0]
        else:
            cas_deces_nums = [0]

        # different regions du senegal
        reg1 = r"(?i)(?:\bDakar\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Dakar)"
        reg2 = r"(?i)(?:\bThiès\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Thiès)"
        reg3 = r"(?i)(?:\bLouga\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Louga)"
        reg4 = r"(?i)(?:\bDiourbel\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Diourbel)"
        reg5 = r"(?i)(?:\bFatick\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Fatick)"
        reg6 = r"(?i)(?:\bKaolack\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Kaolack)"
        reg7 = r"(?i)(?:\bKaffrine\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Kaffrine)"
        reg8 = r"(?i)(?:\bKolda\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Kolda)"
        reg9 = r"(?i)(?:\bTamba\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Tamba)"
        reg10 = r"(?i)(?:\bZiguinchor\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Ziguinchor)"
        reg11 = r"(?i)(?:\bSaint-Louis\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Saint-Louis)"
        reg12 = r"(?i)(?:\bMatam\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Matam)"
        reg13 = r"(?i)(?:\bSédhiou\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Sédhiou)"
        reg14 = r"(?i)(?:\bKédougou\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Kédougou)"

        nb_cas_dkr = re.findall(reg1, text)
        if not nb_cas_dkr:
            nb_cas_dakar = [0]
        else:
            dkr_str = str(nb_cas_dkr)
            nb_cas_dakar = re.findall(r'\d+', dkr_str)

        nbCasTh = re.findall(reg2, text)
        if not nbCasTh:
            nb_cas_thies = [0]
        else:
            th_str = str(nbCasTh)
            nb_cas_thies == re.findall(r'\d+', th_str)

        nbCasLg = re.findall(reg3, text)
        if not nbCasLg:
            nb_cas_louga = [0]
        else:
            lg_str = str(nbCasLg)
            nb_cas_louga = re.findall(r'\d+', lg_str)

        nbCasDbl = re.findall(reg4, text)
        if not nbCasDbl:
            nb_cas_diourbel = [0]
        else:
            dbl_str = str(nbCasDbl)
            nb_cas_diourbel = re.findall(r'\d+', dbl_str)

        nbCasFtk = re.findall(reg5, text)
        if not nbCasFtk:
            nb_cas_fatick = [0]
        else:
            ftk_str = str(nbCasFtk)
            nb_cas_fatick = re.findall(r'\d+', ftk_str)

        nbCasKlk = re.findall(reg6, text)
        if not nbCasKlk:
            nb_cas_kaolack = [0]
        else:
            klk_str = str(nbCasKlk)
            nb_cas_kaolack = re.findall(r'\d+', klk_str)

        nbCasKfr = re.findall(reg7, text)
        if not nbCasKfr:
            nb_cas_kaffrine = [0]
        else:
            kfr_str = str(nbCasKfr)
            nb_cas_kaffrine = re.findall(r'\d+', kfr_str)

        nbCasKld = re.findall(reg8, text)
        if not nbCasKld:
            nb_cas_kolda = [0]
        else:
            kld_str = str(nbCasKld)
            nb_cas_kolda = re.findall(r'\d+', kld_str)

        nbCasTmb = re.findall(reg9, text)
        if not nbCasTmb:
            nb_cas_tamba = [0]
        else:
            tmb_str = str(nbCasTmb)
            nb_cas_tamba = re.findall(r'\d+', tmb_str)

        nbCasZig = re.findall(reg10, text)
        if not nbCasZig:
            nb_cas_ziguinchor = [0]
        else:
            zig_str = str(nbCasZig)
            nb_cas_ziguinchor = re.findall(r'\d+', zig_str)

        nbCasSl = re.findall(reg11, text)
        if not nbCasSl:
            nb_cas_saintl = [0]
        else:
            sl_str = str(nbCasSl)
            nb_cas_saintl = re.findall(r'\d+', sl_str)

        nbCasMtm = re.findall(reg12, text)
        if not nbCasMtm:
            nb_cas_matam = [0]
        else:
            mtm_str = str(nbCasMtm)
            nb_cas_matam = re.findall(r'\d+', mtm_str)

        nbCasSdh = re.findall(reg13, text)
        if not nbCasSdh:
            nb_cas_sedhiou = [0]
        else:
            sdh_str = str(nbCasSdh)
            nb_cas_sedhiou = re.findall(r'\d+', sdh_str)

        nbCasKdg = re.findall(reg14, text)
        if not nbCasKdg:
            nb_cas_kedougou = [0]
        else:
            kdg_str = str(nbCasKdg)
            nb_cas_kedougou = re.findall(r'\d+', kdg_str)
        annee_mois = ''
        json_data = {
            pdf_path: {
                'date': date,
                'nouveaux_cas': cas_positifs_nums[0],
                'cas_importes': cas_importes_nums[0],
                'cas_contacts': cas_contacts_nums[0],
                'test_realise': cas_test_nums[0],
                'personne_sous_traitement': cas_sous_traitement_nums[0],
                'cas_communautaires': cas_communautaires_nums[0],
                'nombre_gueris': cas_gueris_nums[0],
                'nombre_deces': cas_deces_nums[0],
                'date_heure_extraction': str(datetime.now()),
                'nom_fichier_source': source_file,
                'localites': {
                    'Dakar': int(nb_cas_dakar[0]),
                    'Thies': int(nb_cas_thies[0]),
                    'Diourbel': int(nb_cas_diourbel[0]),
                    'Fatick': int(nb_cas_fatick[0]),
                    'Kaolack': int(nb_cas_kaolack[0]),
                    'Kaffrine': int(nb_cas_kaffrine[0]),
                    'Louga': int(nb_cas_louga[0]),
                    'Kolda': int(nb_cas_kolda[0]),
                    'Tambacounda': int(nb_cas_tamba[0]),
                    'Ziguinchor': int(nb_cas_ziguinchor[0]),
                    'Saint-Louis': int(nb_cas_saintl[0]),
                    'Matam': int(nb_cas_matam[0]),
                    'Sedhiou': int(nb_cas_sedhiou[0]),
                    'Kedougou': int(nb_cas_kedougou[0])
                }
            }}
        textJson.append(json_data[pdf_path])

    valeurs = set(map(lambda x: x['date'][3:12], textJson))
    new_list = [[y for y in textJson if y['date'][3:12] == x] for x in valeurs]

    for i in new_list:
        doc_name = i[0]['date'][3:12]
        txtFile = doc_name.replace('/', '-')
        annee_mois = doc_name
        if txtFile:
            with open(str(txtFile) + '.json', 'w', encoding='utf-8') as f:
                json.dump(i, f, ensure_ascii=False, indent=4)
            f.close()
    for f in glob.glob('*.json'):
        shutil.move(f, '../files/jsons')
