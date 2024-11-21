import sqlite3

def connect_to_db():
    """
    Establishes a connection to the SQLite database and returns a cursor and connection object.

    Returns:
        tuple: A tuple containing the cursor and connection objects.
    """
    conn = sqlite3.connect('Verifica_28-11-2024/file.db')
    cur = conn.cursor()
    return cur, conn

def send_query(query, conn, cur):  # LISTA[][] : RESTITUISCE UNA LISTA DI TUPLE
    cur.execute(query)
    conn.commit()
    return cur.fetchall()


def are_there_files(cur, conn, filename):
    """
    Checks if there are any files in the database with the specified filename.

    Parameters:
        cur (sqlite3.Cursor): The database cursor used to execute the query.
        conn (sqlite3.Connection): The database connection object.
        filename (str): The name of the file to search for in the database.

    Returns:
        bool: True if the file exists in the database, False otherwise.
    """
    query = f'''SELECT count(*)
        FROM Files
        WHERE files.nome like "{filename}"
    '''
    
    if send_query(query, conn, cur)[0][0] == 0: 
        return False
    else:
        return True

def n_frag_from_name(filename, cur, conn):
    """
    Retrieves the total number of fragments for a given file name from the database.

    Parameters:
        filename (str): The name of the file to search for in the database.
        cur (sqlite3.Cursor): The database cursor used to execute the query.
        conn (sqlite3.Connection): The database connection object.

    Returns:
        list: A list of tuples containing the file name and the total number of fragments.
    """
    query = f'''
        SELECT files.nome, files.tot_frammenti
        FROM Files
        WHERE Files.nome LIKE "{filename}";
    '''
    return send_query(query, cur=cur, conn=conn)

def ip_host_from_name_and_frag_number(filename, n_frag, cur, conn):
    """
    Retrieves the host IP address for a specific fragment of a given file name.

    Parameters:
        filename (str): The name of the file to search for in the database.
        n_frag (int): The fragment number to retrieve the host IP for.
        cur (sqlite3.Cursor): The database cursor used to execute the query.
        conn (sqlite3.Connection): The database connection object.

    Returns:
        list: A list of tuples containing the host IP address for the specified fragment.
    """
    query = f'''
        SELECT frammenti.host
        FROM Files INNER JOIN frammenti ON files.id_file = frammenti.id_file
        WHERE frammenti.n_frammento = {n_frag} AND files.nome like "{filename}";
    '''
    return send_query(query=query, conn=conn, cur=cur)

def all_ips_of_fragments(filename, cur, conn):
    """
    Retrieves all host IP addresses for all fragments of a given file name.

    Parameters:
        filename (str): The name of the file to search for in the database.
        cur (sqlite3.Cursor): The database cursor used to execute the query.
        conn (sqlite3.Connection): The database connection object.

    Returns:
        list: A list of tuples containing the host IP addresses for all fragments of the file.
    """
    query = f'''
        SELECT frammenti.host
        FROM Files INNER JOIN frammenti ON files.id_file = frammenti.id_file
        WHERE files.nome like "{filename}";
    '''
    return send_query(query=query, conn=conn, cur=cur)


cur, conn = connect_to_db()

# print(are_there_files(conn=conn, cur=cur, filename="Dune.mov"))
# print(n_frag_from_name(filename="Dune.mov", conn=conn, cur=cur))
# print(ip_host_from_name_and_frag_number(filename="Dune.mov", n_frag=2, conn=conn, cur=cur))
# print(all_ips_of_fragments(filename="Dune.mov", cur=cur, conn=conn))
