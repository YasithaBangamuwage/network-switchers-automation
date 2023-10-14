# network-switches-automation

### Configure python environment
Download python windows installer according to your machine specification.<br>
Download url : https://www.python.org/downloads/windows/ <br>
Remanded python version : Python 3.12.0 <br>
Please make sure to add python into the machine PATH variable.<br>
Open PowerShell and type `python --version` command to verify the python installation.<br>

#### Install python packages into the environment
Open PowerShell and execute below commands one by one.
```
pip install schedule
pip install netmiko
pip install python-dotenv
pip install pyinstaller
pip install jsonschema
```

### Deploying CISCO_XE backup schedule manager


#### Creating CISCO_XE backup schedule manager executable file

Verify `.env` file device information under `scripts/device/cisco_xe/dist` directory. (It should mentioned correct values in order to run the schedule)<br>
Open PowerShell and navigate to `scripts/device/cisco_xe` directory.<br>
Execute below command to generate executable file.
```
pyinstaller --onefile --noconsole cisco_xe_backup_schedule_manager.py
```
Create directory called `cisco_xe_backup_schedule_manager` in your machine.<br>
This directory will be hold all generated Log fils and switch configuration Backup files.<br>
Navigate to `scripts/device/cisco_xe/dist` directory and copy `.env` and `cisco_xe_backup_schedule_manager.exe`. <br>
Paste above copy files into `cisco_xe_backup_schedule_manager` directory.<br>
Now you have successfully setup the schedule manager directory in your environment.<br>

There are two options to run schedule manager in your windows environment.<br>
- Run by double click on executable file.
- Configure python executable file via windows service. (recommended option)

#### Run by double click on executable file

Navigate to `cisco_xe_backup_schedule_manager` directory.<br>
Verify `.env` file device information.<br>
Double click on `cisco_xe_backup_schedule_manager.exe` application.<br>
It will be created to directories called `Logs` and `Backups` under `cisco_xe_backup_schedule_manager` directory.<br>
Now backup schedule manager started according to the mentioned device information.<br>
Refer Log file under `Logs` directory to verify the scheduler task activities.<br>
Refer backup files under `Backups` directory. Backup files will be created script mentioned time frame.<br>

#### Configure python executable file via windows service.

Navigate to `cisco_xe_backup_schedule_manager` directory.<br>
Verify `.env` file device information.<br>
Copy `scripts/device/cisco_xe/dist/nssm.exe` file into the `cisco_xe_backup_schedule_manager` directory.<br>
Open PowerShell in `cisco_xe_backup_schedule_manager` directory and run below command.<br>
```
nssm.exe install network_switches_backup_schedule_manager
```
Now NSSM will open up a GUI for you to configure the service. Mandatory to select at least the Path, Startup Directory and Service name. You can check other settings like Actions when the service stops, priority, automatic/manual startup, etc.<br>
Go to windows services window and verify the service. Start if not started already.<br>
It will be created to directories called `Logs` and `Backups` under `cisco_xe_backup_schedule_manager` directory.<br>
Now backup schedule manager started according to the mentioned device information.<br>
Refer Log file under `Logs` directory to verify the scheduler task activities.<br>
Refer backup files under `Backups` directory. Backup files will be created script mentioned time frame.<br>

### Troubleshooting  CISCO_XE backup schedule manager

This scheduler will not stop until machine is shutdown or forcefully stop the process via Task Manager or windows service.<br>
If you need to change the device information, first stop the `cisco_xe_backup_schedule_manager` process via Task Manager or windows service.<br>
Change `.env` file device information.<br>
Start `cisco_xe_backup_schedule_manager` windows service again.<br>
In case you see multiple `cisco_xe_backup_schedule_manager` process in Task Manager please kill all the process and Start `cisco_xe_backup_schedule_manager` windows service again.<br>
