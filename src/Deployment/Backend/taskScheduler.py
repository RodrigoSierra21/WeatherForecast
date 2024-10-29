import win32com.client
from datetime import datetime, timedelta


import win32com.client
from datetime import datetime, timedelta


def create_scheduled_task(task_name, script_path, trigger_type="daily", time="08:00"):
    # Initialize Task Scheduler
    scheduler = win32com.client.Dispatch("Schedule.Service")
    scheduler.Connect()
    root_folder = scheduler.GetFolder("\\")

    # Create the task definition
    task_def = scheduler.NewTask(0)
    task_def.RegistrationInfo.Description = f"{task_name} - runs {trigger_type}"

    # Set the task to run whether the user is logged on or not
    task_def.Principal.LogonType = 3  # TASK_LOGON_INTERACTIVE_TOKEN

    # Define the trigger based on the task frequency
    start_time = datetime.now() + timedelta(seconds=30)  # Delay start by 30 seconds

    if trigger_type == "daily":
        trigger = task_def.Triggers.Create(2)  # TASK_TRIGGER_DAILY
    elif trigger_type == "weekly":
        trigger = task_def.Triggers.Create(3)  # TASK_TRIGGER_WEEKLY
        trigger.DaysOfWeek = 1  # Only on Mondays
    else:
        raise ValueError("Invalid trigger type. Use 'daily' or 'weekly'.")

    # Set the start time for the trigger
    trigger.StartBoundary = start_time.strftime("%Y-%m-%dT%H:%M:%S")

    # Define the action to run the Python script
    action = task_def.Actions.Create(0)  # TASK_ACTION_EXEC
    action.Path = r"C:\Users\34618\AppData\Local\Programs\Python\Python310\python.exe"
    action.Arguments = script_path  # Pass the path to taskRunner.py

    # Register the task in the scheduler
    task = root_folder.RegisterTaskDefinition(
        task_name,
        task_def,
        6,  # TASK_CREATE_OR_UPDATE
        None,  # No username, runs for current user
        None,  # No password
        3,  # TASK_LOGON_INTERACTIVE_TOKEN
        None,
    )
    print(f"Scheduled task '{task_name}' created successfully.")


# Usage example
script_path = r"C:\Users\34618\OneDrive\Documentos\UNI\ML4Industry\Group14-ML4Industry\ForecastingProject\src\Deployment\Backend\taskRunner.py"
create_scheduled_task("DailyTask", script_path, trigger_type="daily", time="08:00")
