from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLineEdit, QApplication,QInputDialog, QLabel, QPushButton, QVBoxLayout,QWidget,QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


import sys 
import json

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.resize(1000,800)
window.setWindowTitle('oum')
window.setWindowIcon(QtGui.QIcon("C:\\Users\\Setup Game\\Downloads\\data_oum\\oum.png"))


#media party
background = QtWidgets.QLabel(window)
photo = QPixmap('C:\\Users\\adamc\Desktop\\data_oum\\img\\background.jpg').scaled(1000,800)
background.setPixmap(photo)
icon1=QPixmap('C:\\Users\\adamc\\Desktop\\data_oum\\img\\id.png')
icon2=QPixmap('C:\\Users\\adamc\\Desktop\\data_oum\\img\\search.png')
icon3=QPixmap('C:\\Users\\adamc\\Desktop\\data_oum\\img\\search.png')



# Charge les données depuis le fichier JSON
with open('data.json', 'r+') as file:
    data = json.load(file)

# Création d'un widget QLabel pour afficher les messages
message_label = QLabel(window)      
message_label.setGeometry(165, 150, 600,650)  # Définir la géométrie de la zone de texte
message_label.setStyleSheet(' font-weight:bold ;font-size:16px;padding:10px; margin:10px; color:blacks')

def search_by_id():
    user_input2, ok = QInputDialog.getInt(window, "Chercher par ID", "Veuillez entrer l'ID:")
    if ok:
        id = int(user_input2)
        found = False
        message = ""  # Variable pour stocker le message à afficher
        for item in data:
            if item['id'] == id      :
                message += f"ID associé : {item['id']}\n"
                message += f"IG associé : {item['IG']}\n"
                message += f"Crop associé : {item['Crop']}\n"
                message += f"DOI associé : {item['DOI']}\n"
                message += f"Origin associé : {item['Origin']}\n"
                message += f"Taxon associé : {item['Taxon']}\n"
                message += f"Premières gousses associé : {item['Premieres gousses']}\n"
                message += f"Jours a la maturite associé : {item['Jours a la maturite']}\n"
                message += f"Couleur de la fleur (petales) associé : {item['Couleur de la fleur (petales)']}\n"
                message += f"Intensite des stries florales (streaks) associé : {item['Intensite des stries florales (streaks)']}\n"
                message += "Couleur de l'aile florale associée : {}\n".format(item["Couleur de l'aile florale"])
                message += f"Nombre de fleur/ inflorescence associé : {item['Nombre de fleur/ inflorescence']}\n"
                message += f"Nombre de branches associé : {item['Nombre de branches']}\n"
                message += f"Ramification terminale associé : {item['Ramification terminale']}\n"
                message += f"Hauteur (maturite) associé : {item['Hauteur (maturite)']}\n"
                message += f"Vigueur de la plante associé : {item['Vigueur de la plante']}\n"
                message += f"Reflectance de la surface de la gousse associé : {item['Reflectance de la surface de la gousse']}\n"
                message += f"Inclinaison de la gousse associé : {item['Inclinaison de la gousse']}\n"
                message += f"Nombre de gousses par plante associé : {item['Nombre de gousses par plante']}\n"
                message += f"Nombre de graines viables par gousse associé : {item['Nombre de graines viables par gousse']}\n"
                message += f"Nombre moyen des graines par gousse associé : {item['Nombre moyen des graines par gousse']}\n"
                message += f"Longueur des gousses (cm) associé : {item['Longueur des gousses (cm)']}\n"
                message += f"Couleur des graines associé : {item['Couleur des graines']}\n"
                message += f"Couleur du hile associé : {item['Couleur du hile']}\n"
                message += f"Nombre de graines par plante individuelle associé : {item['Nombre de graines par plante individuelle']}\n"
                message += f"Poids 1000 grains associé : {item['Poids 1000 grains']}\n"
                message += f"Hauteur (maturite) associé : {item['Hauteur (maturite)']}\n"
                message += f"Etat phytosanitaire associé : {item['Etat phytosanitaire']}\n"
                message += f"Rendement par plante individuelle associé : {item['Rendement par plante individuelle']}\n"
                message += f"Rendement q/ha associé : {item['Rendement q/ha']}\n"
                found = True
                break
        

        if not found:
            message = "L'ID n'existe pas dans les données."

        # Afficher le message dans le widget QLabel
        message_label.setText(message)

def search_by_ig():
    ig, ok = QInputDialog.getInt(window, "Chercher par IG", "Veuillez entrer l'IG:")
    if ok:
        
        i = int(ig)
        found = False
        message = ""
        for item in data:
            if item['IG'] == i:
                message += f"IG associé : {item['IG']}\n"
                message += f"ID associé : {item['id']}\n"
                message += f"Crop associé : {item['Crop']}\n"
                message += f"DOI associé : {item['DOI']}\n"
                message += f"Origin associé : {item['Origin']}\n"
                message += f"Taxon associé : {item['Taxon']}\n"
                message += f"Premières gousses associé : {item['Premieres gousses']}\n"
                message += f"Jours a la maturite associé : {item['Jours a la maturite']}\n"
                message += f"Couleur de la fleur (petales) associé : {item['Couleur de la fleur (petales)']}\n"
                message += f"Intensite des stries florales (streaks) associé : {item['Intensite des stries florales (streaks)']}\n"
                message += "Couleur de l'aile florale associée : {}\n".format(item["Couleur de l'aile florale"])
                message += f"Nombre de fleur/ inflorescence associé : {item['Nombre de fleur/ inflorescence']}\n"
                message += f"Nombre de branches associé : {item['Nombre de branches']}\n"
                message += f"Ramification terminale associé : {item['Ramification terminale']}\n"
                message += f"Hauteur (maturite) associé : {item['Hauteur (maturite)']}\n"
                message += f"Vigueur de la plante associé : {item['Vigueur de la plante']}\n"
                message += f"Reflectance de la surface de la gousse associé : {item['Reflectance de la surface de la gousse']}\n"
                message += f"Inclinaison de la gousse associé : {item['Inclinaison de la gousse']}\n"
                message += f"Nombre de gousses par plante associé : {item['Nombre de gousses par plante']}\n"
                message += f"Nombre de graines viables par gousse associé : {item['Nombre de graines viables par gousse']}\n"
                message += f"Nombre moyen des graines par gousse associé : {item['Nombre moyen des graines par gousse']}\n"
                message += f"Longueur des gousses (cm) associé : {item['Longueur des gousses (cm)']}\n"
                message += f"Couleur des graines associé : {item['Couleur des graines']}\n"
                message += f"Couleur du hile associé : {item['Couleur du hile']}\n"
                message += f"Nombre de graines par plante individuelle associé : {item['Nombre de graines par plante individuelle']}\n"
                message += f"Poids 1000 grains associé : {item['Poids 1000 grains']}\n"
                message += f"Hauteur (maturite) associé : {item['Hauteur (maturite)']}\n"
                message += f"Etat phytosanitaire associé : {item['Etat phytosanitaire']}\n"
                message += f"Rendement par plante individuelle associé : {item['Rendement par plante individuelle']}\n"
                message += f"Rendement q/ha associé : {item['Rendement q/ha']}\n"
                found = True
                break

        if not found:
            message = "L'IG n'existe pas dans les données."

        # Afficher le message dans le widget QLabel
        message_label.setText(message)



def add_species():
    
    nom_fichier = ('')
    
    nv_element = {}
    
    nv_element['id'], _=QInputDialog.getInt(window, "ajouter une nouvelle especes id ", "ajouter une nouvelle especes id:")
    nv_element['IG'], _=QInputDialog.getInt(window, "ajouter une nouvelle especes ig ", "ajouter une nouvelle especes IG:")
    
# je pense que manghir had cas makainch chi cas khur aykheso ndiro lih excepetion ms bn ankhli had message hna bach nrje2 nfkere fhad blan juj marat ealam khur 
    for item in data : 
        if item['id'] == nv_element['id'] or item['IG'] == nv_element['IG']:
            msg_alert = QMessageBox()
            msg_alert.setIcon(QMessageBox.Warning)
            if item['id'] == nv_element['id']:
                msg_alert.setText("id que vous venez d'entre existe deja veuillez entre une nouvelle valeur ")
            elif item['IG'] == nv_element['IG'] :
                msg_alert.setText("IG que vous venez d'entre existe deja veuillez entre une nouvelle valeur ")
            msg_alert.setWindowTitle('erreur')
            msg_alert.exec_()
            return

    nv_element['Crop'], _=QInputDialog.getInt(window, "ajouter une nouvelle especes crop ", "ajouter une nouvelle especes crop:")
    nv_element['DOI'], _=QInputDialog.getInt(window, "ajouter une nouvelle especes doi ", "ajouter une nouvelle especes doi:") 
    nv_element['Origin'], _=QInputDialog.getInt(window, "ajouter ", "Origin:")
    nv_element['Taxon'], _=QInputDialog.getInt(window, "ajouter  ", "Taxon:")
    nv_element['Precocite'], _=QInputDialog.getInt(window, "ajouter ", "Precocite:")
    
    nv_element['Premieres gousses'], _=QInputDialog.getInt(window, "ajouter ", "Premieres gousses:")
    nv_element['Jours a la maturite'], _=QInputDialog.getInt(window, "ajouter ", "Jours a la maturite:")
    nv_element['Couleur de la fleur (petales)'], _=QInputDialog.getInt(window, "ajouter ", "Couleur de la fleur (petales):")
    
    nv_element['Intensite des stries florales (streaks)'], _=QInputDialog.getInt(window, "ajouter  ", "Intensite des stries florales (streaks):")
    nv_element["Couleur de l'aile florale"], _=QInputDialog.getInt(window, "ajouter ", "Couleur de l'aile florale:")
    nv_element['Nombre de fleur/ inflorescence'], _=QInputDialog.getInt(window, "ajouter ", "Nombre de fleur/ inflorescence:")
    nv_element['Nombre de branches'], _=QInputDialog.getInt(window, "ajouter  ", "Nombre de branches:")

    nv_element['Ramification terminale'], _=QInputDialog.getInt(window, "ajouter ", "Ramification terminale:")
    nv_element['Hauteur (maturite)'], _=QInputDialog.getInt(window, "ajouter  ", "Hauteur (maturite):") 
    nv_element['Vigueur de la plante'], _=QInputDialog.getInt(window, "ajouter ", "Vigueur de la plante:")

    nv_element['Couleur de la gousse'], _=QInputDialog.getInt(window, "ajouter  ", "Couleur de la gousse:")
    nv_element['Reflectance de la surface de la gousse'], _=QInputDialog.getInt(window, "ajouter ", "Reflectance de la surface de la gousse:")
    nv_element['Inclinaison de la gousse'], _=QInputDialog.getInt(window, "ajouter  ", "Inclinaison de la gousse:")

    nv_element['Nombre de gousses par plante'], _=QInputDialog.getInt(window, "ajouter  ", "Nombre de gousses par plante:")
    nv_element['Nombre de graines viables par gousse'], _=QInputDialog.getInt(window, "ajouter ", "Nombre de graines viables par gousse:")
    nv_element['Nombre moyen des graines par gousse'], _=QInputDialog.getInt(window, "ajouter  ", "Nombre moyen des graines par gousse:")
    nv_element['Longueur des gousses (cm)'], _=QInputDialog.getInt(window, "ajouter ", "Longueur des gousses (cm):")

    nv_element['Couleur des graines'], _=QInputDialog.getInt(window, "ajouter ", "Couleur des graines:")
    nv_element['Couleur du hile'], _=QInputDialog.getInt(window, "ajoutez ", "Couleur du hile:")
    nv_element['Nombre de graines par plante individuelle'], _=QInputDialog.getInt(window, "ajouter  ", "Nombre de graines par plante individuelle:")
    
    nv_element['Poids 1000 grains'], _=QInputDialog.getInt(window, "ajouter ", "Poids 1000 grains:")
    nv_element['Etat phytosanitaire'], _=QInputDialog.getInt(window, "ajouter ", "Etat phytosanitaire:")
    nv_element['Rendement par plante individuelle'], _=QInputDialog.getInt(window, "ajouter  ", "Rendement par plante individuelle:")
    nv_element['Rendement q/ha'], _=QInputDialog.getInt(window, "Rendement q/ha ", "Rendement q/ha:")


    nom_fichier, _ = QFileDialog.getSaveFileName(window, "Enregistrer sous", "", "JSON Files (*.json)")
    
    
    with open (nom_fichier,'w') as file :
        json.dump((nv_element),file)
    
    
    # Vérifier si l'IG de nouvel_element est différente de celle de tous les éléments déjà présents dans data
    
    ig_doublon = False
    
    for item in data:
        if nv_element['IG'] == item['IG']:
            ig_doublon = True
            break

    if not ig_doublon:
        # Ajouter le nouvel élément aux données existantes
        with open('data.json', 'w') as file:
            data.append(nv_element)
            json.dump(data, file, indent=4)
        




# Création manipulation styles des boutons
btn1 = QtWidgets.QPushButton("Chercher par id", window)
btn2 = QtWidgets.QPushButton("Chercher par IG", window)
btn3 = QtWidgets.QPushButton("Ajouter une nouvelle espèce", window)
btn4 = QtWidgets.QPushButton("new ", window)

btn1.setIcon(QtGui.QIcon(icon1))
btn2.setIcon(QtGui.QIcon(icon2))
btn3.setIcon(QtGui.QIcon(icon3))
btn1.move(150, 50)
btn2.move(350, 50)
btn3.move(550, 50)
btn4.move(750, 50)
btn1.setStyleSheet("""
    QPushButton {
        font-size:13px;
        font-weight:bold;          
        padding: 20px;
        border-radius: 7px;
        border: 0.4px solid black;
         background-color: #ffffff;;
        box-shadow: 2px 2px 2px 1px rgba(0, 0, 255, 0.2);
    }
    QPushButton:hover {
        cursor: pointer;
        background-color: #cccccc; 
        box-shadow: 4px 4px 4px 2px rgba(0, 0, 255); 
    }
""")
btn2.setStyleSheet("""
    QPushButton {
        font-weight:bold; 
        font-size:13px;
        opacity:0.5;
        padding: 20px;
        border-radius: 7px;
        border: 0.4px solid black;
        background-color: #ffffff;
        box-shadow: 2px 2px 2px 1px rgba(0, 0, 255, 0.2);
    }
    
    QPushButton:hover {
        opacity:1;
        cursor: pointer;
        background-color: #cccccc; 
        box-shadow: 4px 4px 4px 2px rgba(0, 0, 255); 
    }
""")
btn3.setStyleSheet("""
    QPushButton {
        font-weight:bold; 
        font-size:13px;
        padding: 20px;
        border-radius: 7px;
        border: 0.4px solid black;
        background-color: #ffffff;
        box-shadow: 2px 2px 2px 1px black;
    }
    
    QPushButton:hover {
        cursor: pointer;
        background-color: #cccccc; 
        box-shadow: 4px 4px 4px 2px rgba(0, 0, 255); 
    }
""")
btn1.clicked.connect(search_by_id)
btn2.clicked.connect(search_by_ig)

def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()

def btn3click():
    def check_credentials():
        username = user_login.text()
        password = password_login.text()
        for user in admin:
            if username == user['user'] and password == user['password']:
                add_species()
                validate_button.clicked.disconnect()
                clear_layout(layout)
                return
        else:
            msg_admin = QMessageBox()
            msg_admin.setText("Admin Required!")
            msg_admin.setIcon(QMessageBox.Warning)
            msg_admin.setWindowTitle('Refused')
            msg_admin.exec_()

    if 'layout' not in locals() or not hasattr(window, "layout"):
        layout = QVBoxLayout()
        window.layout = layout
    else :
        clear_layout(window.layout)

    with open('admin.json', 'r') as file:
        admin = json.load(file) 

    user_login = QLineEdit()
    user_login.setPlaceholderText("Enter Username")
    user_login.setFixedWidth(220)
    user_login.setStyleSheet("padding:10px; font-weight:bold; font-size:13px;border-radius:7px")

    password_login = QLineEdit()
    password_login.setPlaceholderText("Enter Password")
    password_login.setEchoMode(QLineEdit.Password)
    password_login.setFixedWidth(220)
    password_login.setStyleSheet("padding:10px; font-weight:bold; font-size:13px;border-radius:7px")

    validate_button = QPushButton("Validate")
    validate_button.clicked.connect(check_credentials)
    validate_button.setFixedWidth(160)
    validate_button.setStyleSheet('background-color:#207cd8;color:white;font-weight:bold; font-size:12px;')

    button_layout = QVBoxLayout()
    button_layout.addStretch(1)
    button_layout.addWidget(validate_button)
    button_layout.addStretch(1)

    layout.addWidget(user_login)
    layout.addWidget(password_login)
    layout.addLayout(button_layout) 
    layout.setSpacing(20)

    layout_widget = QWidget()
    layout_widget.setLayout(layout)

    central_layout = QVBoxLayout(window)
    central_layout.addWidget(layout_widget, alignment=QtCore.Qt.AlignCenter)

btn3.clicked.connect(btn3click)



btn4.clicked.connect(btn5click)

btn4.clicked.connect(btn5click)
window.show()
sys.exit(app.exec_())