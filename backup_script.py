import os
import subprocess
import datetime
import json
import logging
import glob

# Load configuration from file
with open('backup_config.json', 'r') as config_file:
    config = json.load(config_file)

# Ensure backup folder exists
if not os.path.exists(config["local"]["backup_folder"]):
    os.makedirs(config["local"]["backup_folder"])

# Setup logging
log_file = os.path.join(config["local"]["backup_folder"], "backup_log.txt")
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def backup_files(backup_type):
    if config.get('disable_local_save'):
        logging.info("Local backup saving is disabled.")
        return None

    try:
        backup_name = f"{backup_type}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.tar.gz"
        backup_path = os.path.join(config["local"]["backup_folder"], backup_name)

        subprocess.run(['tar', '-czf', backup_path, config["local"]["source_folder"]])

        if not config.get('disable_ssh_ftp'):
            rsync_command = [
                'rsync',
                '-avz',
                '-e', f'ssh -p {config["ssh"]["port"]}',
                backup_path,
                f'{config["ssh"]["user"]}@{config["ssh"]["host"]}:{config["ssh"]["location"]}'
            ]
            subprocess.run(rsync_command)

        logging.info(f"{backup_type} file backup-up successful.")
        return backup_name

    except Exception as e:
        logging.error(f"Error during {backup_type} file backup: {str(e)}")
        return None

def backup_mysql(backup_type):
    if config.get('disable_local_save'):
        logging.info("Local backup saving is disabled.")
        return None

    try:
        backup_name = f"{backup_type}_db_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.sql.gz"
        backup_path = os.path.join(config["local"]["backup_folder"], backup_name)

        dump_command = [
            'mysqldump',
            '--single-transaction',
            '-h', config["mysql"]["host"],
            '-u', config["mysql"]["user"],
            f'--password={config["mysql"]["password"]}',
            config["mysql"]["database"],
            '|', 'gzip', '>', backup_path
        ]
        subprocess.run(' '.join(dump_command), shell=True)

        if not config.get('disable_ssh_ftp'):
            rsync_command = [
                'rsync',
                '-avz',
                '-e', f'ssh -p {config["ssh"]["port"]}',
                backup_path,
                f'{config["ssh"]["user"]}@{config["ssh"]["host"]}:{config["ssh"]["location"]}'
            ]
            subprocess.run(rsync_command)

        logging.info(f"{backup_type} database backup-up successful.")
        return backup_name

    except Exception as e:
        logging.error(f"Error during {backup_type} database backup: {str(e)}")
        return None

def cleanup_backups(config):
    try:
        for backup_type, retention_period in config["retention"].items():
            file_backup_pattern = os.path.join(config["local"]["backup_folder"], f"{backup_type}_*.tar.gz")
            db_backup_pattern = os.path.join(config["local"]["backup_folder"], f"{backup_type}_db_*.sql.gz")

            file_backups = sorted(glob.glob(file_backup_pattern))
            db_backups = sorted(glob.glob(db_backup_pattern))

            delete_file_count = max(0, len(file_backups) - retention_period)
            delete_db_count = max(0, len(db_backups) - retention_period)

            for i in range(delete_file_count):
                os.remove(file_backups[i])
                logging.info(f"Cleaned up old file backup: {file_backups[i]}")

            for i in range(delete_db_count):
                os.remove(db_backups[i])
                logging.info(f"Cleaned up old database backup: {db_backups[i]}")

    except Exception as e:
        logging.error(f"Error during cleanup: {str(e)}")

def main():
    now = datetime.datetime.now()
    
    if now.hour in config["schedule"]["daily"]:
        backup_type = "daily"
    elif now.weekday() == config["schedule"]["weekly"]["weekday"] and now.hour == config["schedule"]["weekly"]["hour"]:
        backup_type = "weekly"
    elif (config["schedule"]["monthly"]["day_range"][0] <= now.day <= config["schedule"]["monthly"]["day_range"][1]) and now.weekday() == config["schedule"]["monthly"]["weekday"] and now.hour == config["schedule"]["monthly"]["hour"]:
        backup_type = "monthly"
    else:
        logging.info("No Backups for this time frame.")
        return

    logging.info(f"Starting {backup_type} file back-up...")
    backup_files(backup_type)

    logging.info(f"Starting {backup_type} database back-up...")
    backup_mysql(backup_type)

    logging.info("Starting cleanup old back-ups...")
    cleanup_backups(config)
    logging.info("Cleanup successful.")

if __name__ == "__main__":
    main()
