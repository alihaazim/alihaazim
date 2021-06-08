import json
import os
import sys

from PyQt5.QtCore import QDir, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QTreeWidgetItem, QButtonGroup, \
    QAbstractItemView

from moduleAcquisition.data_acquisition import *
from moduleAcquisition.file_downloader import *
from ui.base import Ui_MainWindow
from modeles.communiques import CommuniqueSchema, Communiques


class MainWindow(QMainWindow, Ui_MainWindow):
    checked_item_row = []
    unchecked_item_row = []
    official_checked_row = []
    json_file_content = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model1 = QFileSystemModel()
        self.model2 = QFileSystemModel()
        self.model3 = QFileSystemModel()
        self.ui = Ui_MainWindow()  # represente la fenetre principale
        self.ui.setupUi(self)

        # Module Acquisition
        self.ui.pushButton_5.clicked.connect(self.convert_json)
        self.ui.pushButton_4.clicked.connect(self.download_commnunique)

        # Module Loader
        self.ui.treeView.doubleClicked.connect(self.on_double_click)  # signal sur une ligne du tableau affichant
        # l'ensemble des fichiers json
        self.ui.treeView.setAlternatingRowColors(True)
        self.ui.treeView.setHeaderHidden(True)
        self_radio_group = QButtonGroup(self.ui.groupBox)
        self_radio_group.addButton(self.ui.radioButton)
        self_radio_group.addButton(self.ui.radioButton_2)
        self.ui.radioButton.clicked.connect(self.on_trx_radio)
        self.ui.radioButton_2.clicked.connect(self.on_ac_radio)
        selmodel = self.ui.treeWidget.selectionModel()
        selmodel.selectionChanged.connect(self.check_box_clicked)
        self.ui.pushButton_3.clicked.connect(self.validation)

    # Module Acquisition
    def populate_doc_table(self):
        self.model1.setRootPath(QDir.currentPath())  # definition de chemin d'acces des fichiers json a afficher
        self.ui.treeView_2.setModel(self.model2)  #
        self.ui.treeView_2.setRootIndex(self.model2.index('../files/pdf'))
        self.ui.treeView_2.hideColumn(1)
        self.ui.treeView_2.hideColumn(3)
        self.ui.treeView.setColumnWidth(0, 300)

    def populate_json_table(self):
        self.model3.setRootPath(QDir.currentPath())  # definition de chemin d'acces des fichiers json a afficher
        self.ui.treeView_3.setModel(self.model3)  #
        self.ui.treeView_3.setRootIndex(self.model3.index('../files/jsons'))

    def convert_json(self):
        run_convert_code()

    def download_commnunique(self):
        run_acq_code()

    # Module Loader code
    def populate_communique_table(self):
        self.model2.setRootPath(QDir.currentPath())  # definition de chemin d'acces des fichiers json a afficher
        self.ui.treeView.setModel(self.model2)  #
        self.ui.treeView.setRootIndex(self.model2.index('../files/jsons'))
        self.ui.treeView.hideColumn(1)
        self.ui.treeView.hideColumn(3)
        self.ui.treeView.setColumnWidth(0, 300)

    def on_double_click(self, index):
        # premet d'obtenir le chemin d'acces du fichier selectionne lors d'un double clique
        file_path = self.model2.filePath(index)

        # recuperation du nom du fichier selectionne los d'un double clique
        index_ = self.ui.treeView.selectedIndexes()  # on recupere l'ensemble des indexes
        first_index = index_[0].data()  # on recupere la premiere indexe qui correspond a la colonne name du tableau

        # appelle la fonction display_preview en lui donnant le chemin et le nom du fichier
        self.display_preview(file_path, first_index)

    # affiche le contenu d'un fichier sur le panneau a droite
    def display_preview(self, file_path, first_index):
        with open(file_path) as f:
            self.json_file_content = json.load(f)

        list_communique = self.json_file_content
        view = self.ui.treeWidget
        view.clear()
        view.setSelectionMode(QAbstractItemView.MultiSelection)
        view.setHeaderHidden(True)

        for i in range(len(list_communique)):

            child_item = QTreeWidgetItem(view.invisibleRootItem())
            child_item.setText(0, list_communique[i]['date'])
            child_item.setCheckState(0, Qt.Unchecked)
            child_item.setExpanded(True)
            sub_child1 = QTreeWidgetItem()
            sub_child2 = QTreeWidgetItem()
            sub_child3 = QTreeWidgetItem()
            sub_child31 = QTreeWidgetItem()
            sub_child32 = QTreeWidgetItem()
            sub_child4 = QTreeWidgetItem()
            sub_child5 = QTreeWidgetItem()
            sub_child6 = QTreeWidgetItem()
            sub_child7 = QTreeWidgetItem()
            sub_child8 = QTreeWidgetItem()
            sub_child9 = QTreeWidgetItem()
            sub_child1.setText(0, "Nombre de Test: " + str(list_communique[i]['test_realise']))
            sub_child2.setText(0, "Nombre de nouveaux Cas: " + str(list_communique[i]['nouveaux_cas']))
            sub_child31.setText(0, "Nombre de cas importes: " + str(list_communique[i]['cas_importes']))
            sub_child3.setText(0, "Nombre cas contact: " + str(list_communique[i]['cas_contacts']))
            sub_child32.setText(0, "Nombre de personnes sous traitement: " + str(
                list_communique[i]['personne_sous_traitement']))
            sub_child4.setText(0, "Nombre cas communautaire: " + str(list_communique[i]['cas_communautaires']))
            sub_child5.setText(0, "Nombre gueris: " + str(list_communique[i]['nombre_gueris']))
            sub_child6.setText(0, "Nombre deces: " + str(list_communique[i]['nombre_deces']))
            sub_child7.setText(0, "Nom du fichier source: " + list_communique[i]['nom_fichier_source'])
            sub_child8.setText(0, "Date et heure d'extraction: " + list_communique[i]['date_heure_extraction'])
            sub_child9.setText(0, "Nombre de cas dans chaque region")
            sub_child9.setExpanded(True)

            for j in list_communique[i]['localites']:
                localite = QTreeWidgetItem()
                localite.setText(0, j + " : " + str(list_communique[i]['localites'][j]))
                sub_child9.addChild(localite)

            child_item.addChild(sub_child1)
            child_item.addChild(sub_child2)
            child_item.addChild(sub_child3)
            child_item.addChild(sub_child31)
            child_item.addChild(sub_child32)
            child_item.addChild(sub_child4)
            child_item.addChild(sub_child5)
            child_item.addChild(sub_child6)
            child_item.addChild(sub_child7)
            child_item.addChild(sub_child8)
            child_item.addChild(sub_child9)
            view.addTopLevelItem(child_item)

    def check_box_clicked(self, selected, deselected):

        for index in selected.indexes():
            self.checked_item_row.append(index.row())
        for index in deselected.indexes():
            self.unchecked_item_row.append(index.row())

    def validation(self):
        schema = CommuniqueSchema()
        json_string = "["
        if len(self.unchecked_item_row) > 0:
            for it in self.unchecked_item_row:
                self.checked_item_row.remove(it)
        for i in range(len(self.checked_item_row) - 1):
            json_string += str(self.json_file_content[i]) + ","
        json_string += str(self.json_file_content[len(self.checked_item_row)]) + "]"
        json_string = json_string.replace("\'", "\"")

        try:
            communique = None
            json_object = schema.loads(json_string, many=True)
            for i in json_object:
                communique = Communiques(i.date, i.test_realise, i.nouveaux_cas, i.cas_contacts, i.cas_communautaires,
                                         i.cas_importes, i.personne_sous_traitement,
                                         i.nombre_gueris, i.nombre_deces, i.nom_fichier_source, i.date_heure_extraction,
                                         i.localites)
                communique.init_DB()
        except Exception as e:
            print(e)

    def on_trx_radio(self):
        self.ui.pushButton.setEnabled(True)
        self.ui.pushButton_2.setEnabled(True)

    def on_ac_radio(self):
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_2.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mW = MainWindow()
    mW.populate_communique_table()
    mW.populate_doc_table()
    mW.populate_json_table()
    mW.show()
    app.exec_()
