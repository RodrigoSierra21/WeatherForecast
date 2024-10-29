import win32com.client


def run_scheduled_task(task_name):
    try:
        scheduler = win32com.client.Dispatch("Schedule.Service")
        scheduler.Connect()
        root_folder = scheduler.GetFolder("\\")
        task = root_folder.GetTask(task_name)
        task.Run()
        print(f"Successfully ran task: {task_name}")
    except Exception as e:
        print(f"Failed to run task '{task_name}': {e}")


def list_tasks():
    scheduler = win32com.client.Dispatch("Schedule.Service")
    scheduler.Connect()
    root_folder = scheduler.GetFolder("\\")
    tasks = root_folder.GetTasks(0)
    for task in tasks:
        print(task.Name)


list_tasks()


# Example of how to run your task
run_scheduled_task("DailyTask")
