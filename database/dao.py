from database.DB_connect import DBConnect
from model.rifugio import Rifugio

class DAO:
    """
        Implementare tutte le funzioni necessarie a interrogare il database.
        """
    # TODO
    @staticmethod
    def get_all_rifugi():
        """
        Restituisce tutti i rifugi presenti nella tabella come lista di OGGETTI Rifugio
        """
        conn = DBConnect.get_connection()
        cursore = conn.cursor(dictionary=True)

        query = "SELECT * FROM rifugio"
        cursore.execute(query)

        risultato = []
        for riga in cursore:
            risultato.append(Rifugio(
                riga['id'], riga['nome'], riga['localita'], riga['altitudine'],
                riga['capienza'], riga['aperto']
            ))
        cursore.close()
        conn.close()

        return risultato

    @staticmethod
    def get_connessione_per_anno(year: int):
        """
        Restituisce tutte le connessioni con anno
        Risultato è una lista di dizionari, ad esempio:
        [{'id_rifugio1': 1, 'id_rifugio2': 2}, {'id_rifugio1': 1, 'id_rifugio2': 3}, ...]
        """
        conn = DBConnect.get_connection()
        cursore = conn.cursor(dictionary=True)

        query = """
                SELECT id_rifugio1, id_rifugio2
                FROM connessione
                WHERE anno <= %s \
                """

        cursore.execute(query, (year,))
        risultato = cursore.fetchall()

        cursore.close()
        conn.close()

        return risultato


    @staticmethod
    def get_rifugio_by_id(id_rifugio: int):
        """
        Recupera un rifugio specifico tramite il suo ID e lo restituisce come OGGETTO Rifugio.
        """
        conn = DBConnect.get_connection()
        cursore = conn.cursor(dictionary=True)

        query = "SELECT * FROM rifugio WHERE id = %s"

        cursore.execute(query, (id_rifugio,))

        risultato=[]
        for riga in cursore:
            risultato.append(Rifugio(
                riga['id'], riga['nome'],
                riga['localita'], riga['altitudine'],
                riga['capienza'], riga['aperto']
            ))

        cursore.close()
        conn.close()

        return risultato
