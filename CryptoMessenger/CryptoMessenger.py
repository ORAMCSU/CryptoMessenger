import socket
from threading import Thread
from tkinter import *
import os
import encryption2 as enc

# Liste des nombres premiers de 100 à 1000 pour pouvoir vérifier les nombres entrés par l'utilisateur
nb_prem = [101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293,
 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397,
 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599,
 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691,
 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797,
 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887,
 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]



# S'assure que le répertoire de travail est le même répertoire que celui dans lequel est le fichier.
os.chdir(os.path.dirname(__file__))

# Si l'utilisateur appuie sur entrée, récupère le message en clair et on l'envoie directement.
def Enter_pressed(event):
    input_get = input_field.get()
    send(input_get)
    input_user.set('')


# Fonction qui active le mode "plein écran".
def fullscreen_on():
    window.wm_attributes("-fullscreen",True)
    messages.insert("end","Vous êtes en mode plein écran, appuyez sur Echap pour quitter\n")
    messages.see("end")


# Si l'utilisateur appuie sur Echap, quitte le mode "plein écran".
def Escape_fullscreen(event=None):
    window.wm_attributes("-fullscreen",False)


# Fonction d'ouverture de la page d'aide
def summon_help():
    help_page = Toplevel()
    help_page.title("Aide Cryptomessenger")
    help_page.wm_attributes("-top", 1)
    help_zone = Text(help_page,width=150,height=50, bg="#424242",wrap="word",fg="white")
    hsb = Scrollbar(help_page, orient="vertical", command=help_zone.yview)
    help_zone.configure(yscrollcommand = hsb.set)
    help_zone.grid(row=0)
    hsb.grid(row=0,column = 1, sticky = N+S)
    with open("aide.txt", "r") as file:
        ecrire = file.read()
        help_zone.insert("end",ecrire)
    help_zone.configure(state=DISABLED)


# Fonction pour transférer le dernier message reçu dans la zone de saisie de la partie décodage.
def transfer():
    index = messages.index("end")
    index = float(index)-2.0
    trf = messages.get(index,"end")
    trf = trf.split(": ",1)[1]
    decod_user.set(trf)

# Fonction de fermeture du client lorsque celui-ci n'est pas encore connecté.
def preQuit():
    window.destroy()

# Fonction qui informe le serveur de notre déconnexion avec le message "%q%u%i%t%" puis ferme la connexion avant de fermer la fenêtre.
def Quit(Event=None):
    send("%q%u%i%t%")
    try:
        connexion_avec_serveur.close()
    except:
        pass
    window.destroy()


# Fonction de réception des messages envoyés par le serveur
def receive():
    """Recevoir des messages"""
    while True:
        # Essaie de recevoir le message.
        try:
            msg = connexion_avec_serveur.recv(BUFSIZ).decode("utf8") # décode le message reçu depuis le serveur en UTF8.

            # Si le début du message est le suivant, traite le message comme une information sur les utilisateurs connectées et les affiche.
            if msg[0:8]=='%!;??;!%':
                msg= msg[9:]
                list_users = msg.split(';')
                listbox_users.delete(0,END)
                listbox_users.insert(END, "Utilisateurs Connectés:")
                for i in range (len(list_users)):
                    listbox_users.insert(END, list_users[i])
            else:
                messages.insert(END, msg + "\n") # Revient à la ligne et écrit le message
                messages.see("end") # permet de toujours afficher la dernière ligne

        # Si le client est déconnecté du chat, coupe la réception et informe l'utilisateur.
        except OSError:
            messages.insert("end","Le contact avec le serveur a été perdu, veuillez vérifier votre connexion et redémarrer l'application.\n")
            messages.see("end")
            break # stop

# Fonction du choix du destinataire
def destinataire():
    choix = listbox_users.curselection()
    if choix == (0,):
        key_user.set("Choisissez un utilisateur")
    elif choix != ():
        user_RSA = listbox_users.get(listbox_users.curselection())
        clef_RSA = '(' + user_RSA.split("(")[1]
        key_user.set(clef_RSA)


# Fonction d'envoi du message au serveur qui lui s'occupera de le partager à tous les clients.
def send(message,event=None):  # event au cas où on l'utilise pour une reconnaissance de touche.
    """Envoyer des messages"""
    try:
        connexion_avec_serveur.send(bytes(message, "utf8")) # envoie le message codé en binaire au serveur.
    except:
        messages.insert("end","Impossible d'envoyer des informations au serveur, veuillez vérifier votre connexion et redémarrer l'application.\n")
        messages.see("end")


# Une des fonctions principales du programme, qui récupère le message à crypter et le crypte, puis l'envoie en appelant la fonction "send".
def cryptage():
    input_get = input_field.get()
    choix = codlist.curselection()
    if choix == (0,):
        key_get = key_field.get()
        crypt = enc.DES_crypt(key_get,input_get)
        send(crypt)
        input_user.set('')
    elif choix == (1,):
        key_get = key_field.get()
        if key_get != "":
            rep = enc.RSA_crypt(input_get,key_get)
            if rep != "Clef invalide":
                send(rep)
                input_user.set('')
            else:
                key_user.set("Forme de la clef: (n,c)")
        else:
            key_user.set("Veuillez mettre une clef")


# Une des fonctions principales du programme, qui récupère le message à décrypter et le décrypte, en fonction du choix de l'utilisateur sur la liste des cryptages.
def decryptage():
    input_get = decod_field.get()
    choix = decodlist.curselection()
    if choix == (0,):
        key_get = keydc_field.get()
        decrypt = enc.DES_decrypt(key_get,input_get)
        msg_decode.insert("end",decrypt + "\n")
        msg_decode.see("end")
        decod_user.set("")
    elif choix == (1,):
        rep = enc.RSA_decrypt(input_get)
        keydc_user.set(rep)
        msg_decode.insert("end",rep+"\n")
        msg_decode.see("end")
        decod_user.set('')


# Fonction qui efface l'intégralité des messages reçus et la clef choisie pour crypter.
def vidcod():
    messages.delete(1.0,END)
    key_user.set("")


# Fonction qui efface l'intégralité des messages décodés et la clef utilisée pour décrypter.
def viddecod():
    msg_decode.delete(1.0,END)
    keydc_user.set("")

# Fonction de sélection de l'hôte choisi dans l'historique
def select_host():
    choix = Historic_list.curselection()

    if choix != ():
        hote = Historic_list.get(choix)
        hote = hote.replace("(","")
        hote = hote.replace(")","")
        IP_hote = hote.split("'")[1]
        PORT_hote = hote.split(" ")[1]
        IP_user.set(IP_hote)
        PORT_user.set(PORT_hote)

# Fonction de suppression de l'hôte choisi dans l'historique
def sup_host():
    choix = Historic_list.curselection()

    if choix != ():
        Historic_list.delete(choix)
        indice = choix[0]
        del donnees["hosts"][indice]
        with open("cles_ordi","wb") as file:
            enc.pk.Pickler(file).dump(donnees)


# Variables nécessaires au bon fonctionnement de la fonction initier
connexion_avec_serveur = None
donnees = None

# Fonction de connexion au serveur
def initier():
    global connexion_avec_serveur
    global donnees
    IP = IP_field.get()
    nom = Name_field.get()


# Teste les valeurs rentrées différemment en fonction de l'existence du fichier "cles_ordi", interrompt la fonction en cas d'erreur.
    if os.path.exists("cles_ordi"):
        try:

            p = int(p_field.get())
            q = int(q_field.get())

        except:
            invalid_p["text"] = ""
            invalid_q["text"] = ""
            pass

        else:

            if (100<p<1000 and 100<q<1000 and p in nb_prem and q in nb_prem):
                data = enc.creat_clef(nom,p,q)
                donnees["clé_privée"] = data["clé_privée"]
                donnees["clé_publique"] = data["clé_publique"]
                invalid_p["text"] = ""
                invalid_q["text"] = ""
            else:
                invalid_p["text"] = "Veuillez entrer un entier premier entre 100 et 1000"

                invalid_q["text"] = "Veuillez entrer un entier premier entre 100 et 1000"
                return

    else:

        if nom == "":

            noName["text"] = "Veuillez entrer votre nom"
            return
        else:
            noName["text"] = ""

        try:

            p = int(p_field.get())
            q = int(q_field.get())


            if not (100<p<1000 and 100<q<1000 and p in nb_prem and q in nb_prem):

                invalid_p["text"] = "Veuillez entrer un entier premier entre 100 et 1000"

                invalid_q["text"] = "Veuillez entrer un entier premier entre 100 et 1000"
                return


        except:

            invalid_p["text"] = "Veuillez entrer un entier premier"

            invalid_q["text"] = "Veuillez entrer un entier premier"
            return

        else:
            invalid_p["text"] = ""
            invalid_q["text"] = ""
            donnees = enc.creat_clef(nom,p,q)
            donnees["hosts"] = []

    # Teste les valeurs d'hôte rentrées, interrompt la fonction en cas d'erreur.
    try:

        PORT = int(PORT_field.get())

    except ValueError:

        falseport["text"] = "Veuillez rentrer un NUMERO de port!"
        PORT = -10
    else:
        if not 0<=PORT<=65535:
            falseport["text"] = "Le numéro d'un port va de 0 à 65535!"
        else:
            falseport["text"] = ""

    # Essaie de se connecter au serveur. Si ça ne fonctionne pas, informe l'utilisateur avec un message d'erreur et interrompt la fonction.
    finally:

        try:
            connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # paramètres de connexion au serveur (AF_inet = adresses internet et SOCK_STREAM = socket TCP)
            connexion_avec_serveur.connect((IP, PORT)) # connexion au serveur via IP et port du serveur

        except:

            inexhost["text"] = "L'adresse IP que vous souhaitez rejoindre n'est pas valide, essayez avec une autre."

            return

    receive_thread = Thread(target=receive) # appel à la fonction de réception en parallèle
    receive_thread.start() # lance la fonction de réception

    with open("cles_ordi","wb") as file:

        donnees["name"]= nom

        if not (IP,PORT) in donnees["hosts"]:
            donnees["hosts"].append((IP,PORT))

        enc.pk.Pickler(file).dump(donnees)

    # Dès que la connexion au serveur est établie, envoie un tout premier message qui est interprété comme le nom qui sera affiché pour chaque message.
    # Le nom est stocké dans le fichier "cles_ordi".
    clef = str(donnees["clé_publique"])
    connexion_avec_serveur.send(bytes(nom + " " + clef,"utf8"))


    # Ferme la fenêtre d'accueil.
    accueil.destroy()

    # Affiche la fenêtre de chat et la met au premier plan.
    window.wm_deiconify()
    window.wm_attributes("-topmost", True)



""" Pour le Tkinter, les variables portent le suffixe "_user", les champs de saisie portent le suffixe "_field", et tous les widgets sont placés
à l'aide de la méthode ".grid" """

#Fenêtre principale de chat
window = Tk()
window.wm_attributes("-top", 2)
window.geometry("1920x795"+"0"+"0")
window.configure(bg="#B6B0AD")
window.title("CryptoMessenger")
icontkinter = PhotoImage(file='cadena.ico')
window.iconphoto(True,icontkinter)

# Le menu
menubar = Menu(window)
window.config(menu=menubar)

menufichier = Menu(menubar,tearoff=0)
menubar.add_cascade(label="Affichage", menu=menufichier)
menufichier.add_command(label="Plein écran", command =fullscreen_on)
menufichier.add_command(label="Ecran fenêtré", command =Escape_fullscreen)
menufichier.add_separator()
menufichier.add_command(label="Quitter", command = Quit)

menuaide = Menu(menubar,tearoff=0)
menubar.add_cascade(label= "Aide", menu=menuaide)
menuaide.add_command(label="Questions Fréquentes", command = summon_help)


# Le titre de la zone des messages codés.
title_msg = Label(window,text="Messages codés", bg="#B6B0AD", font=("Ubuntu", "12"))
title_msg.grid(row=0, pady='2p')

# La zone de texte des messages codés et sa barre de défilement vertical.
messages = Text(window, height=20, width=120, bd='5p', wrap="word")
vsb = Scrollbar(window, orient="vertical", command=messages.yview)
messages.configure(yscrollcommand=vsb.set)

# On positionne la zone de texte et sa barre de défilement.
messages.grid(row = 1, rowspan=3, padx='5p')
vsb.grid(row=1,column=1,rowspan=3,sticky=N+S)

# La liste de choix de la méthode de cryptage.
codlist = Listbox(window, font=("Ubuntu", "12"), activestyle='none', selectbackground='orange')
codlist.grid(row=1, column=2, columnspan=2, sticky=N+S+W+E, padx='5p')

# On place les noms de nos méthodes de cryptage dans la liste pour que l'utilisateur puisse les sélectionner.
codlist.insert(END, "DES")
codlist.insert(END, "RSA")

# La liste des personnes connectées
listbox_users = Listbox(window, font=("Ubuntu", "12"), activestyle='none', foreground='white', relief='flat',background='#848484', selectbackground='orange', borderwidth='5p', width = 25)
listbox_users.grid(row=1, column=4, rowspan=8, sticky=N+S+W+E, padx='8p')

# Le bouton de choix du destinataire
destinataire_btn = Button(window,text="Sélectionner",command = destinataire, bg = "#8181F7", relief= 'groove', font=("Ubuntu","12"))
destinataire_btn.grid(row=9, column=4, padx="3p", pady="2p", sticky=W+E)

# Le titre de la zone d'entrée destinée aux clefs
label_key = Label(window,text="Entrer Clef", bg="#B6B0AD", font=("Ubuntu", "12"))
label_key.grid(row=2, column=2, padx='3p')

# La zone d'entrée de la clef.
key_user = StringVar()
key_field = Entry(window, text=key_user)
key_field.grid(row=2, column=3, padx='3p')

# Le bouton qui permet déclencher le cryptage.
valicod = Button(window,text="Crypter/Envoyer",command = cryptage, fg="white", bg="#1290F2", relief= 'groove', font=("Ubuntu", "12"))
valicod.grid(row=3, column=2, sticky=W+E, padx='3p')

# Le bouton qui permet de vider la zone des messages.
clearcod = Button(window,text="Vider",command=vidcod, fg="white", bg="#EE4530", relief= 'groove', font=("Ubuntu", "12"))
clearcod.grid(row=3, column=3, sticky=W+E, padx='3p')

# La zone de saisie du message à crypter.
input_user = StringVar()
input_field = Entry(window, text=input_user, bd='5p')
input_field.grid(row=4, column=0, sticky=W+E, padx='6p',pady="5p")

# Le bouton qui permet de transférer la dernière ligne de message reçue dans la zone de saisie du décodage.
transfert = Button(window,text="Transférer",command=transfer, bg = "#FD8601", relief= 'groove', font=("Ubuntu","12"))
transfert.grid(row=4,column=2,columnspan=2,sticky=W+E,padx=3)

# Le titre de la zone de décodage.
title_msgdc = Label(window,text="Messages reçus décodés", bg="#B6B0AD", font=("Ubuntu", "12"))
title_msgdc.grid(row=6, pady='3p')

# La zone de texte où s'affichent les messages décodés et sa barre de défilement vertical.
msg_decode = Text(window, height=18, width=120, bd='5p',wrap="word")
vsb2 = Scrollbar(window, orient="vertical", command=msg_decode.yview)

# On place la zone de texte et sa barre de défilement dans la fenêtre et on les relie grâce à la méthode ".configure".
msg_decode.grid(row=7, rowspan=2, padx='5p', sticky=W)
vsb2.grid(row=7,column=1,rowspan=2,sticky=N+S+W)
msg_decode.configure(yscrollcommand=vsb2.set)

# La liste de choix de la méthode de décryptage.
decodlist = Listbox(window, font=("Ubuntu", "12"), height= 5, activestyle='none', selectbackground='orange')
decodlist.grid(row=7, column=2, columnspan=2, sticky=N+S+W+E, padx='5p')

# On place les noms de nos méthodes de décryptage dans la liste pour que l'utilisateur puisse les sélectionner.
decodlist.insert(END,"DES")
decodlist.insert(END,"RSA")

# Le titre de la zone d'entrée destinée aux clefs.
label_keydc = Label(window,text="Clef (sauf RSA)", bg="#B6B0AD", font=("Ubuntu", "12"))
label_keydc.grid(row=8, column=2, padx='3p')

# La zone de saisie réservée à la clef pour décoder.
keydc_user = StringVar()
keydc_field = Entry(window,text=keydc_user)
keydc_field.grid(row=8, column=3, padx='3p')

# Le bouton qui permet de déclencher le décryptage.
validecod = Button(window,text="Décrypter",command = decryptage, fg="white", bg="#46C124", relief= 'groove', font=("Ubuntu", "12"))
validecod.grid(row=9, column=2, sticky=W+E, padx='3p')

# Le bouton qui permet de vider la zone de texte de messages décodés.
cleardecod = Button(window,text="Vider",command=viddecod, fg="white", bg="#EE4530", relief= 'groove', font=("Ubuntu", "12"))
cleardecod.grid(row=9, column=3, sticky=W+E, padx='3p')

# La zone de saisie du message à décoder.
decod_user = StringVar()
decod_field = Entry(window, text=decod_user, bd='5p')
decod_field.grid(row=9, column=0, sticky=W+E, padx='6p', pady='5p')



# La méthode ".bind" permet de détecter l'appui sur une touche.
input_field.bind("<Return>", Enter_pressed)
window.bind("<Escape>", Escape_fullscreen)

# On spécifie la directive à suivre lors de la fermeture de la fenêtre.
window.protocol("WM_DELETE_WINDOW", Quit)
window.wm_iconify()



#-----------------------------------------------------------------------------

# Page d'accueil
accueil = Toplevel()
accueil.wm_attributes("-topmost", True)
accueil.title("Accueil CryptoMessenger")
accueil.configure(bg="#B6B0AD")
accueil.protocol("WM_DELETE_WINDOW",preQuit)


# Zone d'entrée de l'adresse IP
label_IP = Label(accueil, text = "Rentrez l'IP du serveur à rejoindre: ", bg="#B6B0AD")
label_IP.grid(row=0,column=0)


IP_user = StringVar()
IP_field = Entry(accueil, text = IP_user, width=55)
IP_field.grid(row=0,column=1, padx= '20p')

# Zone d'affichage du message d'erreur en cas de mauvais IP
inexhost = Label(accueil, text = "", bg="#B6B0AD", fg='red')
inexhost.grid(row=1,column=1)


# Zone de l'historique des adresses IP
Historic_list = Listbox(accueil, font=("Ubuntu", "12"), activestyle='none', selectbackground='orange', height = 6, width= 30)
Historic_list.grid(row=0, column=2, rowspan = 6, padx= '10p', pady= '10p')


# Zone de saisie du port
label_PORT = Label(accueil, text = "Rentrez le port du serveur à rejoindre: ", bg="#B6B0AD")
label_PORT.grid(row=2,column=0)


PORT_user = StringVar()
PORT_field = Entry(accueil, text = PORT_user, width=55)
PORT_field.grid(row=2,column=1, padx= '20p')

# Zone d'affichage du message d'erreur en cas de port invalide
falseport = Label(accueil, text = "", bg="#B6B0AD", fg='red')
falseport.grid(row=3, column=1)


# Zone de saisie du nom
label_Name = Label(accueil, text="Votre nom: ", bg="#B6B0AD")
label_Name.grid(row=4,column=0)


Name_user = StringVar()
Name_field = Entry(accueil,text=Name_user, width=55)
Name_field.grid(row=4,column=1, padx= '20p')

# Zone d'affichage du message d'erreur en cas de zone de nom vide
noName = Label(accueil,text = "", bg="#B6B0AD", fg='red')
noName.grid(row=5, column=1)


# Zone de saisie du premier nombre premier
label_p = Label(accueil, text="Nombre premier 100<p<1000 : ", bg="#B6B0AD")
label_p.grid(row=6,column=0)


p_user = StringVar()
p_field = Entry(accueil, text=p_user, width=55)
p_field.grid(row=6,column=1, padx= '20p')

# Zone d'affichage du message d'erreur en cas de nombre premier invalide
invalid_p = Label(accueil,text="", bg="#B6B0AD", fg='red')
invalid_p.grid(row=7,column=1)


# Zone de saisie du second nombre premier
label_q = Label(accueil, text="Nombre premier 100<q<1000 : ", bg="#B6B0AD")
label_q.grid(row=8,column=0)


q_user = StringVar()
q_field = Entry(accueil,text=q_user, width=55)
q_field.grid(row=8,column=1, padx= '20p')

# Zone d'affichage du message d'erreur en cas de nombre premier invalide
invalid_q = Label(accueil,text="", bg="#B6B0AD", fg='red')
invalid_q.grid(row=9,column=1)


# Bouton de sélection de l'adresse choisie dans l'historique
Historic_slt = Button(accueil, text = "Sélectionner",font=("Ubuntu", "12"), command = select_host, relief= 'groove', bg='#58FA58')
Historic_slt.grid(row=6,column=2, rowspan = 2, padx= '10p', pady= '3p', sticky = W+E)


# Bouton de suppression de l'adresse choisie dans l'historique
Historic_sup = Button(accueil, text = "Supprimer", font=("Ubuntu", "12"), command = sup_host, relief= 'groove', bg='#FE2E2E')
Historic_sup.grid(row=8,column=2, rowspan = 2, padx= '10p', pady= '3p', sticky = W+E)


# Bouton de lancement de la procédure de connexion
Lancer = Button(accueil, text = "Se connecter", font=("Ubuntu", "12"), command = initier, relief= 'groove', bg='#2E64FE')
Lancer.grid(row=10,column=0, columnspan = 3, sticky = W+E)


# Dans le cas où l'utilisateur a déjà utilisé ce programme, on l'informe qu'il n'a pas besoin de tout renseigner.
if os.path.exists("cles_ordi"):

    p_user.set("Déjà renseigné, mettez-en un si vous souhaitez le modifier")
    q_user.set("Déjà renseigné, mettez-en un si vous souhaitez le modifier")
    with open("cles_ordi","rb") as file:
        donnees = enc.pk.Unpickler(file).load()
        nom = donnees["name"]
        Name_user.set(nom)

        for i in range(len(donnees["hosts"])):
            Historic_list.insert(END,str(donnees["hosts"][i]))



BUFSIZ = 1024 # nombre de caractères lus en une seule fois par la fonction de réception

window.mainloop() # lance la boucle principale