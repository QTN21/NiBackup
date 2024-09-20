"""
DESCRIPTION
"""
import requests
import logging

def syno_login(URL, USER, PASS):
    """
    Login function on the SYNOLOGY NAS
    URL (str): URL quickconnect/IP du synology
    USER (str): nom d'utilisateur pour la récupération de données
    PASS (str): mot de passe de l'utilisateur
    return : SID de la connexion au NAS 
    """
    try:
        url_login = f"{URL}/webapi/auth.cgi?api=SYNO.API.Auth&version=6&method=login&account={USER}&passwd={PASS}"
        r_auth = requests.get(url_login, verify=True, headers={'Referer': URL})
        
        if r_auth.status_code == 200:
            r_auth = r_auth.json()
            if r_auth["data"] and r_auth["success"]:
                return r_auth["data"]["sid"]
        logging.error("Login failed on", URL)
        return False
    
    except requests.exceptions.RequestException as e:
        logging.error("Request error: %s", e)
        return False


def syno_logout(URL, SID):
    """
    Logout Function on the SYNOLOGY NAS
    URL (str) : URL quickconnect/IP du synology
    SID (str) : ID de la session 
    return : True/False sur le logout
    """
    try:
        url_logout = f"{URL}/webapi/auth.cgi?api=SYNO.API.Auth&version=6&method=logout&_sid={SID}"
        r_logout = requests.get(url_logout, verify=True, headers={"Referer": URL})
        
        if r_logout.status_code == 200:
            r_logout = r_logout.json()
            if r_logout["success"]:
                return True
        logging.error("Logout failed on", URL)
        return False
    
    except requests.exceptions.RequestException as e:
        logging.error("Request error: %s", e)
        return False


def syno_hyper_backup(URL, SID):
    """
    Fonction de récupération de données de l'application Hyper Backup
    URL (str) : URL quickconnect/IP du synology
    SID (str) : ID de la session 
    return : liste contenant un dictionnaire des infos sur chaque tache de backup
    """
    backup_data = list()
    
    try:
        # Récupération de la liste des tâches de backup
        url_backup = f"{URL}/webapi/entry.cgi?api=SYNO.Backup.Task&version=1&method=list&_sid={SID}"
        r_backup = requests.get(url_backup, verify=True, headers={"Referer": URL}).json()
        
        if r_backup["data"]:
            for task in r_backup["data"]["task_list"]:
                # Récupération du détail sur le backup
                url_detail = f"{URL}/webapi/entry.cgi?api=SYNO.Backup.Task&method=status&version=1&blOnline=false&additional=[\"last_bkp_time\",\"next_bkp_time\",\"last_bkp_result\",\"is_modified\",\"last_bkp_progress\"]&task_id={task['task_id']}&_sid={SID}"
                
                r_detail = requests.get(url_detail, verify=True, headers={"Referer": URL}).json()
                
                if r_detail["data"] and ("usb" not in task["name"].lower() and "local" not in task["name"].lower() and "old" not in task["name"].lower()):
                    # Ajout du dictionnaire
                    backup_data.append({
                        "name": task["name"],
                        "data_enc" : task["data_enc"],
                        "last_bkp_start": r_detail["data"]["last_bkp_time"],
                        "last_bkp_end": r_detail["data"]["last_bkp_end_time"],
                        "last_bkp_error_code": r_detail["data"]["last_bkp_error_code"],
                        "state": r_detail["data"]["last_bkp_result"],
                        "schedule_enable": r_detail["data"]["schedule"]["schedule_enable"]
                    })
            logging.info("Backup data retrieved successfully")
            return backup_data
        logging.error("Failed to retrieve backup data")
        return False
    
    except requests.exceptions.RequestException as e:
        logging.error("Request error: %s", e)
        return False


if __name__ == "__main__":
    pass