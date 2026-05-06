import sqlite3
from datetime import datetime

DATABASE_NAME="debug_history.db"

def get_db_connection():
    """
    Creates and returns database connection.
    
    Why this function is needed:
    instead of writting qsqllite3.connect() again and again,
    we keep it in one reusable function.
    """

    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory=sqlite3.Row
    return connection

def create_history_table():
    """
    Creates the history table if it dont exists.
    This function runs when the Flask app starts.
    """

    connection=get_db_connection()

    connection.execute(""" Create Table if not exists debug_history (
                       id Integer Primary key AUTOINCREMENT,
                       error_text text not null,
                       summary text not null,
                       root_cause text not null,
                       possible_location text,
                       fix_steps text not null,
                       corrected_code_or_command text,
                       created_at text not null
                       )
                       """)
    
    connection.commit()
    connection.close()


def save_analysis(error_text, analysis):
    """
    Saves the user error and AI analysis into the database.
    
    analysis is a dictionary coming from ai_engine.py.
    """

    connection = get_db_connection()
    connection.execute(""" Insert into debug_history(
                       error_text,
                       summary,
                       root_cause,
                       possible_location,
                       fix_steps,
                       corrected_code_or_command,
                       created_at
                       
                       ) values (?,?,?,?,?,?,?)
                       """,(error_text,
                            analysis.get("summary",""),
                            analysis.get("root_cause",""),
                            analysis.get("possible_location",""),
                            "\n".join(analysis.get("fix_steps",[])),
                            analysis.get("corrected_code_or_command",""),
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            ))
    

    connection.commit()
    connection.close()


def get_analysis_history():
    """
    Fectches previous debugging result from the database.
    Latest records come first.
    """
    
    connection=get_db_connection()

    rows= connection.execute("""
                             Select 
                             id,
                             error_text,
                             summary,
                             root_cause,
                             possible_location,
                             fix_steps,
                             corrected_code_or_command,
                             created_at
                             From debug_history
                             Order by id desc
                             """).fetchall()
    
    connection.close()

    history=[]
    for row in rows:
        history.append({
            "id": row["id"],
            "error_text": row["error_text"],
            "summary": row["summary"],
            "root_cause": row["root_cause"],
            "possible_location": row["possible_location"],
            "fix_steps": row["fix_steps"].split("\n"),
            "corrected_code_or_command": row["corrected_code_or_command"],
            "created_at": row["created_at"]
        })

    
    return history