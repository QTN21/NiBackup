import lib.synology_api as syno
from lib.manage_db import db_select
import csv
import sys
import logging

# Set up logging to a file
logging.basicConfig(filename='./files/syno-script.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def csv_create(dico, DST_FILE):
    """
    Creates a CSV file from a dictionary.
    """
    try:
        fieldnames = ["client", "bckp_name", "encryption", "last_state", "last_bkp_start", "last_bkp_end", "error_code", "schedule_enable"]

        with open(DST_FILE, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(fieldnames)

            for client, backups in dico.items():
                for backup in backups:
                    row = [client, backup["name"], backup["data_enc"], backup["state"], backup["last_bkp_start"], backup["last_bkp_end"], backup["last_bkp_error_code"], backup["schedule_enable"]]
                    writer.writerow(row)
        logging.info("CSV data wrote successfully")
    except Exception as e:
        logging.error("Error creating CSV file: %s", e)


def main(password):
    DB_FILE = "./files/nas-database.db"
    DB_PASS = password
    CSV_FILE = "./files/backup.csv"
    data = dict()

    try:
        # Récupération des données de la DB
        db_data = db_select(DB_FILE, DB_PASS)

        for value in db_data.values():
            try:
                sid = syno.syno_login(value["url"], value["user"], value["pass"])

                if sid:
                    data[value["clients"]] = syno.syno_hyper_backup(value["url"], sid)

                syno.syno_logout(value["url"], sid)
            except Exception as e:
                logging.error("Error processing %s: %s", value["url"], e)

        if data:
            csv_create(data, CSV_FILE)
    except Exception as e:
        logging.error("Error in main function: %s", e)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <password>")
        sys.exit(1)

    password = sys.argv[1]
    main(password)