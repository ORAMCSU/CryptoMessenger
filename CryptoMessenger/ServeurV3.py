"""Serveur pour une application de chat asynchrone."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from time import sleep


def accept_incoming_connections():
    """Définit la réception du client."""
    while True:
        client, client_address = SERVER.accept() # Accepte un client et stocke ses caractéristiques.
        print("%s:%s s'est connecté." % client_address)
        client.send(bytes("Vous êtes bien connecté!", "utf8"))

        # Stocke l'adresse du client dans un dictionnaire pour pouvoir s'en resservir.
        addresses[client] = client_address

        # Lance la fonction qui s'occupe de gérer les messages envoyés par le client, en parallèle.
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Prend le socket du client en argument (pour pouvoir le cibler lors de la réception des messages).
    """Cette fonction gère l'arrivée du client, reçoit en premier message son pseudo
    et gère ensuite tous les messages envoyés par le client en les partageant aux autres clients."""

    # Prépare le message contenant les noms des utilisateurs.
    list_clients = "%!;??;!%"

    # Reçoit le premier message du client (son nom), et lui souhaite la bienvenue.
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Bienvenue %s! Si tu veux quitter, appuie sur le bouton Quitter.' % name
    client.send(bytes(welcome, "utf8"))

    # Informe ensuite les autres clients de l'arrivée du nouveau.
    msg = "%s a rejoint le chat!" % name
    broadcast(bytes(msg, "utf8"))

    # Stocke le nouveau client dans le dictionnaire des clients pour qu'il puisse recevoir les messages généraux.
    clients[client] = name

    # Attend une seconde avant d'envoyer la liste des utilisateurs.
    sleep(1)
    for nom in clients:
        list_clients += ";" + clients[nom]
    broadcast(bytes(list_clients, "utf8"))

    # Réceptionne de manière permanente les messages du client.
    while True:
        msg = client.recv(BUFSIZ)

        # Si le message n'indique pas que le client veut partir, le partage à tous. Sinon, coupe les connexions avec le client, le supprime du dictionnaire et sort de la boucle.
        if msg != bytes("%q%u%i%t%", "utf8"):
            broadcast(msg, name+": ")
        else:

            # Renvoie la liste des utilisateurs restants.
            list_clients = "%!;??;!%"
            print(addresses[client][0],":",addresses[client][1]," est parti...",sep="")
            client.close()
            del clients[client]
            for nom in clients:
                list_clients += ";" + clients[nom]
            broadcast(bytes(list_clients, "utf8"))
            break


def broadcast(msg, prefix=""):  # Le préfixe sert pour le pseudo de l'utilisateur.
    """Envoie le message placé en argument à tous les clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


clients = {}
addresses = {}

# Définit tous les paramètres nécessaires à la création du serveur. Laisser un nom d'hôte vide indique au serveur de se créer sur la machine.
# BUFSIZ est le nombre de caractères traités simultanément par message reçu.
HOST = ''
PORT = 60000
BUFSIZ = 1024
ADDR = (HOST, PORT)

# Lance le serveur.
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("En attente d'une connexion...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()