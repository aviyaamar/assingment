
import sqlite3, json
from flask import Flask, request, jsonify, Response

app = Flask(__name__)
DATABASE = 'storage.db'


def get_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
    except Exception as e:
        print(e)
    return conn


@app.route('/file/', methods=['GET'])
def get_files():
    conn = get_connection()
    cursor = conn.cursor()
    cursor = conn.execute("SELECT * FROM files")
    sql = conn.execute('SELECT COUNT(*) from files')
    avg = conn.execute(" SELECT AVG(Average_file_size) FROM files")
    largest_file = conn.execute("SELECT MAX(Largest_file_received), file_name FROM files")
    last_ten_result = conn.execute("SELECT file_name FROM files LIMIT 10")
    frequnacy = conn.execute("""
                     SELECT Most_frequent_media_type
                     FROM files
                     GROUP By Most_frequent_media_type
                     Having Count(*) = (
                     SELECT MAX(Cnt) FROM(
                     SELECT COUNT(*) as Cnt
                     FROM files
                     GROUP BY Most_frequent_media_type) tmp)
                     """
                     )
           
    files = [
            dict(num_file=sql.fetchone(), 
             avg= avg.fetchone(),
             largest =largest_file.fetchone(),
             last_files=last_ten_result.fetchall() ,
             media_type = frequnacy.fetchone(), 
            #  file_name=row[0], Total_number_of_files_received=row[1], Largest_file_received=row[2], 
            # Average_file_size=row[3], Most_frequent_media_type=row[4], List_files_received=row[5])
            # for row in cursor.fetchall()
            )
        ]

    if files is not None:
      return jsonify(files)

@app.route('/file', methods=['POST'])
def post_file():
    req = json.loads(json.dumps(request.get_json()))
    # req =  request.json
    file_name = req.get("file_name")
    Total_number_of_files_received = req.get("Total_number_of_files_received")
    Largest_file_received = req.get("Largest_file_received")
    Average_file_size = req.get("Average_file_size")
    Most_frequent_media_type = req.get("Most_frequent_media_type")
    List_files_received = req.get("List_files_received")

    conn = get_connection()
    print(conn)
    print(type( Total_number_of_files_received))
    sql = """INSERT INTO files (file_name, Total_number_of_files_received, Largest_file_received, Average_file_size, Most_frequent_media_type, List_files_received)
                     VALUES (?,?,?,?,?,?)"""
    conn.execute(sql,(file_name, Total_number_of_files_received, Largest_file_received, Average_file_size, Most_frequent_media_type, List_files_received))
    conn.commit()
    return Response('Hello, {}'.format(req.get("file_name")), status=201)

# @app.route('/file', methods=['GET'])
# def get_all_files(filename):
#     return 'Hello, {}'.format(filename)


@app.route('/file/<file_name>', methods=['GET'])
def get_specific_file(file_name):
    conn = get_connection()
    cursor = conn.cursor()
    file = None
    cursor.execute("SELECT * FROM files WHERE file_name=?", (file_name,))
    rows = cursor.fetchall()
    for r in rows:
            file = r
    if file is not None:
         return jsonify(file), 200
    else:
            return "Something wrong", 404
    
      

@app.route('/file/<file_name>', methods=['PUT'])
def modify_data(file_name):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """ UPDATE files 
           SET Total_number_of_files_received=?,
            Largest_file_received=?,
            Average_file_size=?,
            Most_frequent_media_type=?,
            List_files_received=?
                WHERE file_name=? """

    req = json.loads(json.dumps(request.get_json()))
    # req = request.json

    file_name = req.get("file_name")
    Total_number_of_files_received = req.get("Total_number_of_files_received")
    Largest_file_received = req.get("Largest_file_received")
    Average_file_size = req.get("Average_file_size")
    Most_frequent_media_type = req.get("Most_frequent_media_type")
    List_files_received = req.get("List_files_received")

    update_files = {
        "file_name": file_name,
        "Total_number_of_files_received": Total_number_of_files_received,
        "Largest_file_received": Largest_file_received,
        "Average_file_size": Average_file_size,
        "Most_frequent_media_type": Most_frequent_media_type,
        "List_files_received": List_files_received

    }
    conn.execute(sql,(file_name, Total_number_of_files_received, Largest_file_received, Average_file_size, Most_frequent_media_type, List_files_received))
    conn.commit()
    return jsonify(update_files)



if __name__ == '__main__':
    app.run(debug=True)  # Enable reloader and debugger
