import sqlite3


class GPTDB:

    def __init__(self):
        """
            Initialisation de la class et créé de la table si existe pas.
        """
        connexion = sqlite3.connect("data/gptservchan.db")
        cur = connexion.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS Servchan ("
            "idServ INTEGER NOT NULL, "
            "idChan INTEGER NOT NULL, "
            "PRIMARY KEY (idServ, idChan));"
        )
        connexion.commit()
        cur.close()


    def insertServerChannel(self, serv_id, chan_id):
        """
        Permet d'ajouter un server, channel à la db
        :argument serv_id: identifiant du server.
        :argument chan_id: identifiant du channel.
        """
        connexion = sqlite3.connect("data/gptservchan.db")
        cur = connexion.cursor()
        cur.execute("INSERT INTO Servchan VALUES (?, ?);", (serv_id, chan_id))
        connexion.commit()
        cur.close()

    def deleteServerChannel(self, serv_id, chan_id):
        """
        Permet de supprimer un server, channel de la db
        :param serv_id:
        :param chan_id:
        """
        connexion = sqlite3.connect("data/gptservchan.db")
        cur = connexion.cursor()
        cur.execute("DELETE FROM Servchan WHERE idServ = ? AND idChan = ?;", (serv_id, chan_id))
        connexion.commit()
        cur.close()

    def isChanServExist(self, serv_id, chan_id) -> bool:
        """
        Vérifier si la clé {serv_id, chan_id} se trouve dans la db.
        :param serv_id: identifiant du serveur
        :param chan_id: identifiant du channel
        :return: True si existe, sinn False
        """
        connexion = sqlite3.connect("data/gptservchan.db")
        cur = connexion.cursor()
        cur.execute("SELECT COUNT(*) FROM Servchan WHERE idServ = ? AND idChan = ?", (serv_id, chan_id))
        resultat = cur.fetchone()[0]
        connexion.close()

        return resultat > 0
