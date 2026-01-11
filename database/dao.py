from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.rifugio import Rifugio

class DAO:
    """
        Implementare tutte le funzioni necessarie a interrogare il database.
        """
    # TODO
    @staticmethod
    def get_all_rifugi(year): #voglio solo i rifugi che esistono prima di un certo anno
        """
        Restituisce tutti i rifugi presenti nella tabella come lista di OGGETTI Rifugio
        """
        conn = DBConnect.get_connection()
        rifugi= {}
        cursore = conn.cursor(dictionary=True)

        query = ('''SELECT DISTINCT r.id, r.nome, r.localita, r.altitudine, r.capienza, r.aperto
                    FROM rifugio r, connessione c
                    WHERE c.anno <= %s and (r.id = c.id_rifugio1 or r.id = c.id_rifugio2)
                    ORDER BY r.nome
                    ''')
        # (r.id=c.id_rifugio1 or r.id=c.id_rifugio2) verifico che o un sentiero parta da quel rifugio o che un sentiero
        # arrivi a quel rifugio, quindi verifico che il rifugio abbia delle connessioni

        cursore.execute(query, (year,))

        for riga in cursore:
            if rifugi.get(riga['id']) is None: #se il rofugio non è presente nel mio dizionario
                rifugi[riga['id']] = Rifugio(**riga)

        cursore.close()
        conn.close()

        return rifugi

    @staticmethod
    def get_connessioni(rifugi, year):
        """
        Restituisce tutte le connessioni con anno
        Risultato è una lista di dizionari, ad esempio:
        [{'id_rifugio1': 1, 'id_rifugio2': 2}, {'id_rifugio1': 1, 'id_rifugio2': 3}, ...]
        """
        conn = DBConnect.get_connection()
        cursore = conn.cursor(dictionary=True)
        connessioni = {}

        #non conta la direzione dei percorsi, sono sempre da rifugi diversi, quindi posso non usare LEAST or GREATEST
        # (sempre meglio metterli se non so com'è fatto il database, all'esame meglio metterlo)
        query = """
                SELECT id_rifugio1, id_rifugio2, distanza, difficolta, durata
                FROM connessione
                WHERE anno <= %s 
                """

        cursore.execute(query, (year,))

        for riga in cursore:
            r1=rifugi.get(riga['id_rifugio1']) #rifugio di partenza
            r2=rifugi.get(riga['id_rifugio2']) #rifugio di arrivo
            # !r1 e r2 sono degli oggetti rifugio!

            if r1 is not None and r2 is not None and (r1, r2) not in connessioni:
                connessioni[r1, r2] = Connessione(r1, r2, riga['distanza'], riga['difficolta'], riga['durata'])
                #dizionario che ha come chiave la coppia (r1, r2) e come valore un oggetto Connessione

        cursore.close()
        conn.close()

        return connessioni
