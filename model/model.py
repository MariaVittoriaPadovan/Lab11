import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.Graph()

    def build_graph(self, year: int):
        """
        Costruisce il grafo (self.G) dei rifugi considerando solo le connessioni
        con campo `anno` <= year passato come argomento.
        Quindi il grafo avrà solo i nodi che appartengono almeno ad una connessione, non tutti quelli disponibili.
        :param year: anno limite fino al quale selezionare le connessioni da includere.
        """
        # TODO
        self.G.clear()

        connessioni = DAO.get_connessione_per_anno(year)

        for c in connessioni:
            r1 = c['id_rifugio1']
            r2 = c['id_rifugio2']

            # Aggiungo nodi e archi senza pesi
            self.G.add_node(r1)
            self.G.add_node(r2)
            self.G.add_edge(r1, r2)

    def get_nodes(self):
        """
        Restituisce la lista dei rifugi presenti nel grafo.
        :return: lista dei rifugi presenti nel grafo.
        """
        # TODO

        lista_oggetti_rifugio = []
        for id_rifugio in self.G.nodes:
            # Chiama il DAO che restituisce una lista di oggetti Rifugio.
            risultato_dao = DAO.get_rifugio_by_id(id_rifugio)

            # Se la lista non è vuota, estraiamo l'oggetto.
            if risultato_dao:
                lista_oggetti_rifugio.append(risultato_dao[0])

        return lista_oggetti_rifugio

    def get_num_neighbors(self, node):
        """
        Restituisce il grado (numero di vicini diretti) del nodo rifugio.
        :param node: un rifugio (cioè un nodo del grafo)
        :return: numero di vicini diretti del nodo indicato
        """
        # TODO

        # Il Controller passa l'OGGETTO Rifugio, uso l'attributo .id per interrogarne il grado
        node_id = node.id

        if node_id in self.G:
            return self.G.degree[node_id]
        else:
            return 0

    def get_num_connected_components(self):
        """
        Restituisce il numero di componenti connesse del grafo.
        :return: numero di componenti connesse
        """
        # TODO
        return nx.number_connected_components(self.G)
        #è una funzione di NetworkX e serve per calcolare quante componenti connesse ha un grafo non orientato



    def get_reachable_dfs_tree(self, start_id: int):
        """
        Trova i nodi raggiungibili usando nx.dfs_tree().
        :param start_id: ID del nodo di partenza.
        :return: Lista di ID dei nodi raggiungibili (escluso il nodo di partenza).
        """
        dfs_graph = nx.dfs_tree(self.G, source=start_id) # nx.dfs_tree() restituisce un grafo contenente tutti i nodi raggiungibili
        reachable_ids = list(dfs_graph.nodes) # il .nodes() fornisce gli ID

        if start_id in reachable_ids:
            reachable_ids.remove(start_id) #rimuove il nodo di partenza

        return reachable_ids

    def get_reachable_ricorsivo(self, start_id: int):
        """
                Algoritmo DFS ricorsivo. Restituisce lista di ID.
        """

        visitati = set() # Inizializzo l'insieme dei nodi visitati

        def dfs(u):
            # Segna u come visitato all'inizio della chiamata ricorsiva
            if u not in visitati:
                visitati.add(u)
                for v in self.G.neighbors(u):
                    dfs(v)

        if start_id not in self.G:
            return []

        dfs(start_id)

        # gestione del nodo iniziale per l'algoritmo ricorsivo
        if start_id in visitati:
            visitati.remove(start_id)

        return list(visitati)


    def get_reachable(self, start):
        """
        Deve eseguire almeno 2 delle 3 tecniche indicate nella traccia:
        * Metodi NetworkX: `dfs_tree()`, `bfs_tree()`
        * Algoritmo ricorsivo DFS
        * Algoritmo iterativo
        per ottenere l'elenco di rifugi raggiungibili da `start` e deve restituire uno degli elenchi calcolati.
        :param start: nodo di partenza, da non considerare nell'elenco da restituire.

        ESEMPIO
        a = self.get_reachable_bfs_tree(start)
        b = self.get_reachable_iterative(start)
        b = self.get_reachable_recursive(start)

        return a
        """

        # TODO

        start_id = start.id #estraggo l'ID dall'oggetto Rifugio
        if start_id not in self.G:
            return []

        #eseguo l'algoritmo (che restituisce una lista di ID)
        a_reachable_ids = self.get_reachable_dfs_tree(start_id)
        #eseguo la seconda tecnica
        b_reachable_ids =self.get_reachable_ricorsivo(start_id)

        #converto gli ID in OGGETTI Rifugio per il Controller
        reachable_objects = []
        for id_rifugio in a_reachable_ids:
            risultato_dao = DAO.get_rifugio_by_id(id_rifugio) # il DAO restituisce una lista con 0 o 1 oggetto

            #se la lista non è vuota, aggiungo l'oggetto
            if risultato_dao:
                reachable_objects.append(risultato_dao[0])

        return reachable_objects

