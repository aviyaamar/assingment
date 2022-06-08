import sqlite3

conn = sqlite3.connect("storage.db")

cursor = conn.cursor()
sql_query = """ CREATE TABLE files (
    file_name TEXT ,
    Total_number_of_files_received int,
    Largest_file_received int,
    Average_file_size REAL ,
    Most_frequent_media_type TEXT,
    List_files_received TEXT 
)"""
cursor.execute(sql_query)
10