"""
DESCRIPTION
"""

from pysqlcipher3 import dbapi2 as sqlite
import logging

def db_connect(FILE, PASS):
    """
    Ouvre une connexion à une base de données SQLite chiffrée.
    
    :param FILE: Le chemin du fichier de la base de données.
    :param PASS: Le mot de passe de chiffrement de la base de données.
    :return: Un objet de connexion à la base de données.
    """
    try:
        conn = sqlite.connect(FILE)
        conn.execute(f"PRAGMA key = '{PASS}';")  # Configurer la clé de chiffrement

        # Vérifier l'intégrité de la DB
        cursor = conn.execute("PRAGMA integrity_check;")
        result = cursor.fetchone()

        if result[0] != 'ok':
            logging.error("Database corrupted")
            return None

        logging.info("Database opened successfully")
        return conn
    
    except sqlite.Error as e:
        logging.error("Error during opening the database : %s", e)
        return None


def db_disconnect(CONN):
    """
    Ferme la connexion à une base de données SQLite.
    
    :param CONN: L'objet de connexion à la base de données.
    """
    try:
        if CONN:
            CONN.close()
            logging.info("Database closed successfully")
        else:
            logging.info("Impossible to close the database")
    except sqlite.Error as e:
        logging.error("Error during closing the database : %s", e)



def db_select(FILE, PASS):
    """
    Récupère toutes les données de la table credentials et les retourne sous forme de dictionnaire.

    :param db_file: Le chemin du fichier de la base de données.
    :param db_password: Le mot de passe de chiffrement de la base de données.
    :return: Un dictionnaire contenant toutes les données de la table credentials.
    """
    CONN = db_connect(FILE, PASS)
    data_dict = {}
    
    if CONN is None:
        return None
    
    try:
        # Exécuter la requête pour récupérer toutes les données
        cursor = CONN.execute(f"SELECT * FROM credentials")
        
        # Parcourir les résultats et ajouter au dictionnaire
        data_dict = {
            row[0]: {
                'clients': row[1],
                'url': row[2],
                'user': row[3],
                'pass': row[4]
            } for row in cursor.fetchall()
        }
        logging.info("Data retrieved successfully from the database")
    
    except sqlite.Error as e:
        logging.error("Error while getting data from database : %s", e)
        data_dict = None
    
    finally:
        # Fermer la base de données
        db_disconnect(CONN)
    
    return data_dict

if __name__ == "__main__":
    pass