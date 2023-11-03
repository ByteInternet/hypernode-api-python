# Hypernode Backup Script

## Overview
This backup script is designed specifically for use on the Hypernode platform. It facilitates secure backup of files and MySQL databases and can be configured to store backups locally and/or send to a remote server via SSH.

## Features
- Automated backup of files and databases.
- Support for daily, weekly, and monthly backup schedules.
- Cleanup functionality to remove old backups based on retention policy.
- Option to disable local backup storage and SSH/FTP transfer.
- Detailed logging of all backup activities.

## Configuration
Customize the `backup_config.json` file to suit your backup needs. This is where you can set:
- SSH and MySQL connection details.
- Backup paths and schedules.
- Retention policy for backups.

## Installation
1. Clone the repository to your Hypernode server.
2. Install any required external commands (`tar`, `rsync`, `mysqldump`).
3. Configure your backup preferences in `backup_config.json`.
4. Set up a cron job to run the script according to your schedule.

## Usage
The script is intended to run as a cron job but can be started manually with:

```bash
python3 backup_script.py
```

## Cron Job Setup
To schedule the backup script to run automatically, add the following line to your crontab:
Make sure to adjust the paths to match the location of your script and working directory.

```cron
0 * * * * sleep 7; cd /data/web/backup/ && /usr/bin/python3 /data/web/backup/backup_script.py # noflock
```

## Disclaimer
This script is not officially supported by the Hypernode support team. Users should implement this script at their own risk and are responsible for properly configuring and securing their backup processes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.