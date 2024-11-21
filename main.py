import sqlite3
import argparse
import sql_commands

connection = sqlite3.connect("tracker.db")
cur = connection.cursor()


res = cur.execute("SELECT name FROM sqlite_master")

sql_commands.create_table_tasks(cur)
sql_commands.create_table_tags(cur)
sql_commands.create_table_tagsTasks(cur)




parser = argparse.ArgumentParser(description="A cli app for keeping track on tasks")


subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")
    
# Subcommand: Display
display_parser = subparsers.add_parser("display", help="Display tasks")
group = display_parser.add_mutually_exclusive_group(required=True)
group.add_argument("--finished", action="store_true", help="Show finished tasks")
group.add_argument("--unfinished", action="store_true", help="Show unfinished tasks")

# Subcommand: Add
add_parser = subparsers.add_parser("add", help="Add a new task")
add_parser.add_argument("--task", type=str, required=True, help="Task description")
add_parser.add_argument("--category", type=str,  help="Task category")
add_parser.add_argument("--start_date", type=str, help="Start date (YYYY-MM-DD), defaults to current time")
add_parser.add_argument("--end_date", type=str,help="End date (YYYY-MM-DD), defaults to None" )
add_parser.add_argument(
        "--tag",
        type=str,
        nargs="*",
        help="Tag(s) associated with the task (optional, can specify multiple)"
    )


# Subcommand: Mark as finished

finish_parser = subparsers.add_parser("finish", help="Mark a task as finished")
finish_parser.add_argument("--task_id", type=int, required=True, help="The taskID of the task that should be updated")
finish_parser.add_argument("--end_date", type=str, help="End date for completion of task, default is now.")

# Subcommand: Delete
delete_parser = subparsers.add_parser("delete", help="Delete a task")
delete_parser.add_argument("--task_id", type=int, required=True, help="ID of the task to delete")

# Subcommand: View all
view_all_parser = subparsers.add_parser("view all", help= "View all tasks")


args = parser.parse_args() 



try: 
    if args.command == "add": 
        sql_commands.start_task(
            cur, 
            task=args.task, 
            category=args.category, 
            start = args.start_date, 
            end = args.end_date, 
            tag = args.tag
        )
    elif args.command == "display": 
        sql_commands.display_unfinished_or_finished(cur, args.finished)
    elif args.command == "delete": 
        sql_commands.delete_task(cur, args.task_id)
    elif args.command == "finish": 
        sql_commands.mark_task_as_finished(cur, args.task_id, args.end_date)
    elif args.command == "view all": 
        sql_commands.display_pretty(cur) 
finally: 
    connection.close() 


