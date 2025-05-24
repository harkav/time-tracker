import sqlite3
import prettytable
import datetime

def create_table_tasks(cur: sqlite3.Cursor) -> None:
    cur.execute(
        """
                CREATE TABLE IF NOT EXISTS tasks( 
                    taskID INTEGER PRIMARY KEY AUTOINCREMENT, 
                    task text NOT NULL, 
                    start_date text NOT NULL, 
                    end_date text,
                    category text
                )"""
    )


def create_table_tags(cur: sqlite3.Cursor) -> None:
    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS tags(
                tagID  INTEGER PRIMARY KEY AUTOINCREMENT, 
                tag TEXT UNIQUE  
)

        """
    )

def create_table_tagsTasks(cur: sqlite3.Cursor) -> None: 
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS taskTags(
            taskID integer, 
            tagID integer, 
            FOREIGN KEY (taskID) REFERENCES tasks (taskID) on DELETE CASCADE, 
            FOREIGN KEY (tagID) REFERENCES tags (tagID) on DELETE CASCADE, 
            PRIMARY KEY (taskID, tagID)
        )
"""
    )


def drop_table(cur: sqlite3.Cursor, tablename: str) -> None:
    cur.execute(f"DROP table {tablename}")


def view_all_tasks(cur: sqlite3.Cursor) -> None:
    cur.execute(
        """
            SELECT * FROM tasks
        """
    )
    res = cur.fetchall()
    print(res)


def view_headers(cur: sqlite3.Cursor, tablename: str) -> None:
    cur.execute(
        f"""
    PRAGMA table_info({tablename})
    """
    )
    for row in cur.fetchall():
        print(row)

tablenames = ["tasks", "tags", "taskTags"]


def hard_reset(cur: sqlite3.Cursor, tablenames: list[str]) -> None:
    for tablename in tablenames:
        drop_table(cur, tablename)






def print_headers(cur: sqlite3.Cursor, tablenames: list[str]) -> None: 
    for tablename in tablenames:

        view_headers(cur, tablename)


def start_task(
    cur: sqlite3.Cursor,
    task: str,
    category: str | None = None,
    start: str | None = None,
    end: str | None = None,
    tag: str | list[str] | None = None,
) -> None:

    print("Entering add-method")

    try:
        # Check inputs before processing
        print(f"Task: {task}, Category: {category}, Start: {start}, End: {end}, Tags: {tag}")

        # Handle start_date
        if start:
            start_date = datetime.datetime.strptime(start, "%Y-%d-%m %H:%M")
        else:
            start_date = datetime.datetime.now()
            start_date = start_date.strftime("%Y-%d-%m %H:%M")
        
        print(f"Start date: {start_date}")

        # Handle end_date
        if end:
            end_date = datetime.datetime.strptime(end, "%Y-%d-%m %H:%M")
        else:
            end_date = None
        
        print(f"End date: {end_date}")

        # Insert task into the database
        cur.execute(
            """
            INSERT INTO tasks(task, start_date, end_date, category)
            VALUES (?, ?, ?, ?)
            """,
            (task, start_date, end_date, category),
        )
        
        # Check if the task was inserted
        task_id = cur.lastrowid
        print(f"Task inserted, task_id: {task_id}")
        
        if task_id == 0:
            print("No task was inserted, check the INSERT statement!")
            return

        # Handle tags if provided
        if tag:
            if isinstance(tag, str):
                tag = [tag]

            for element in tag:
                # Check if tag already exists
                cur.execute("SELECT tagID FROM tags WHERE tag = ?", (element,))
                tag_id = cur.fetchone()

                if tag_id is None:
                    cur.execute("INSERT INTO tags(tag) VALUES (?)", (element,))
                    tag_id = cur.lastrowid
                else:
                    tag_id = tag_id[0]

                print(f"Tag inserted or found, tag_id: {tag_id}")

                # Check if taskTag combination exists
                cur.execute("SELECT 1 FROM taskTags WHERE taskID = ? AND tagID = ?", (task_id, tag_id))
                if not cur.fetchone():
                    cur.execute(
                        """
                        INSERT INTO taskTags (taskID, tagID) VALUES (?, ?)
                        """,
                        (task_id, tag_id),
                    )
                    print(f"Tag {element} associated with task {task_id}")
        
        # Commit changes to the database
        print("Committing transaction...")
        cur.connection.commit()
        print("Transaction committed successfully.")

    except sqlite3.Error as e:
        print(f"An error has occurred: {task}, {e}")
        cur.connection.rollback()



def display_raw(cur: sqlite3.Cursor, tablenames: list[str]) -> None:
    for tablename in tablenames:
        cur.execute(f"SELECT * FROM {tablename}")
        results = cur.fetchall()
        for r in results:
            print(r)


def display_pretty(cur: sqlite3.Cursor) -> None:
    """
    Displays the the rows of TaskTags prettified
    
    Args: 
        cur (sqlite3.Cursor) the cursor
    
    """
    
    cur.execute(
        """
                SELECT 

                    t.taskID,
                    t.task,  
                    t.start_date, 
                    t.end_date,
                    t.category, 
                    GROUP_CONCAT (tag.tag, ', ') AS tags

                FROM 

                    tasks t 
                
                LEFT JOIN 

                    taskTags tt ON t.taskID = tt.taskID

                LEFT JOIN 

                    tags tag ON tt.tagID = tag.tagID 
                
                GROUP BY 
                    
                    t.taskID 

                """
    )
    rows = cur.fetchall()

    table = prettytable.PrettyTable()
    table.title = "All tasks"
    table.field_names = ["ID", "Task", "Start", "End", "Category", "Tag(s)"]
    


    for row in rows: 
        table.add_row(row)

    print(table) 



def display_unfinished_or_finished(cur: sqlite3.Cursor, finished : bool = False) -> None:

    if finished: 
        is_finished_str = "IS NOT NULL"
        title = "All finished tasks"
    else: 
        is_finished_str = "IS NULL"
        title = "All unfinished tasks"
    cur.execute(
        f"""
                SELECT 

                    t.taskID,
                    t.task,  
                    t.start_date, 
                    t.end_date,
                    t.category, 
                    GROUP_CONCAT (tag.tag, ', ') AS tags

                FROM 

                    tasks t 
                
                LEFT JOIN 

                    taskTags tt ON t.taskID = tt.taskID

                LEFT JOIN 

                    tags tag ON tt.tagID = tag.tagID 
                
                WHERE 

                    t.end_date {is_finished_str} 
                
                GROUP BY 
                    
                    t.taskID 

                """
    )
    rows = cur.fetchall()

    table = prettytable.PrettyTable()
    table.title = title
    table.field_names = ["ID", "Task", "Start", "End", "Category", "Tag(s)"]
    


    for row in rows:
        table.add_row(row)

    print(table) 


def delete_task(cur : sqlite3.Cursor, taskID: str) -> None: 
    try:     
        cur.execute(
            f"DELETE FROM Tasks Where TaskID = ?", (taskID, )
        )
        
        if cur.rowcount > 0: 
            cur.connection.commit()
            print(f"Task with {taskID} deleted sucessfully")
        else: 
            print(f"No task with task id {taskID} was found")

    except sqlite3.Error as e: 
        print(f"Could not delete task with ID {taskID}")
        cur.connection.rollback()


def mark_task_as_finished(cur : sqlite3.Cursor, taskID: str, end_date: str | None = None  ): 
    try: 
        cur.execute("SELECT * FROM Tasks WHERE taskID = ?", (taskID, ))
        task = cur.fetchone() 

        if not task: 
            print(f"Task with id {taskID} not found, no changes made")
            return 
        if not end_date: 
            end_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        cur.execute("UPDATE tasks SET end_date = ? WHERE taskID = ?", 
                    (end_date, taskID))
        
        cur.connection.commit() 

        print(f"Task with id {taskID} updated")
    except sqlite3.Error as e: 
        print(f"Failed to update task")
        cur.connection.rollback() 


def update_task(cur: sqlite3.Cursor, taskID: str, task_column : str, new_cell_data : str): 
    #TODO add validation for editing time. 
    
    try: 
        cur.execute("SELECT * FROM Tasks WHERE taskID = ?", (taskID, ))
        task = cur.fetchone()
        allowed_column_names = get_column_names_task(cur, "tasks")
        
        if not task_column in allowed_column_names: 
            print(f"Could not find column {task_column}, found {allowed_column_names}")
            return
        
        if task_column in {"start_date", "end_date"}: 
            time = validate_time(new_cell_data)
            if not time: 
                return
        
        if task_column == "ID": 
            print("Cannot change ID")
            return   
        

        if not task: 
            print(f"Task with id {taskID} not found, no changes made")
            return 
       
        cur.execute(f"UPDATE tasks SET {task_column} = ? WHERE taskID = ?", 
                    (new_cell_data, taskID))
        
        cur.connection.commit() 

        print(f"Task with id {taskID} updated")
    except sqlite3.Error as e: 
        print(f"Failed to update task")
        cur.connection.rollback()
        

def get_column_names_task(cur: sqlite3.Cursor, table_name : str) -> list[str]: 
    cur.execute(f"PRAGMA table_info({table_name});")
    
    return [col[1] for col in cur.fetchall()]


def validate_time(maybe_time : str) -> datetime.datetime: 
    
    try: 
        time = datetime.datetime.strptime(maybe_time, "%Y-%m-%d %H:%M")
        return time 
    except ValueError: 
        raise ValueError(f"Could not read time {maybe_time}, enter time on the format YYYY-MM-DD")
    