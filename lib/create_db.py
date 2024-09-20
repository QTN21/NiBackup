from pysqlcipher3 import dbapi2 as sqlite

# Nom du fichier de base de données
db_file = "nas-database.db"

# Mot de passe pour chiffrer la base de données
db_password = "securepassword123"

# Connexion à la base de données et configuration du chiffrement
conn = sqlite.connect(db_file)

# Activer le chiffrement en configurant la clé
conn.execute(f"PRAGMA key = '{db_password}';")

# Création de la table URL, USER, PASS
conn.execute('''CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                clients VARCHAR(100) NOT NULL,
                url VARCHAR(100) NOT NULL,
                user VARCHAR(100) NOT NULL,
                pass VARCHAR(100) NOT NULL
            );''')

# Sauvegarder les changements
conn.commit()

# Fermeture de la connexion à la base de données
conn.close()