import networkx as nx
from database.dao import DAO
from datetime import datetime

class Model:
    def __init__(self):

        # definite da me
        self.rifugi = None
        self.connessioni = None

        self.G = nx.Graph()


    def build_graph(self, year: int):
        """
        Costruisce il grafo (self.G) dei rifugi considerando solo le connessioni
        con campo `anno` <= year passato come argomento.
        Quindi il grafo avrà solo i nodi che appartengono almeno ad una connessione, non tutti quelli disponibili.
        :param year: anno limite fino al quale selezionare le connessioni da includere.
        """
        # TODO

        self.rifugi= DAO.get_all_rifugi(year)
        self.connessioni= DAO.get_connessioni(self.rifugi, year)

        self.G.clear()

        self.G.add_nodes_from(self.rifugi.values())
        self.G.add_edges_from([(c.r1, c.r2) for c in self.connessioni.values()])


    def get_nodes(self):
        """
        Restituisce la lista dei rifugi presenti nel grafo.
        :return: lista dei rifugi presenti nel grafo.
        """
        # TODO

        return list(self.G.nodes())


    def get_num_neighbors(self, node):
        """
        Restituisce il grado (numero di vicini diretti) del nodo rifugio.
        :param node: un rifugio (cioè un nodo del grafo)
        :return: numero di vicini diretti del nodo indicato
        """
        # TODO

        return len(list(self.G.neighbors(node)))


    def get_num_connected_components(self):
        """
        Restituisce il numero di componenti connesse del grafo.
        :return: numero di componenti connesse
        """
        # TODO
        return nx.number_connected_components(self.G)
        #è una funzione di NetworkX e serve per calcolare quante componenti connesse ha un grafo non orientato


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

        tic = datetime.now()
        a = self.get_reachable_dfs_tree(start)
        print(f"DFS: {datetime.now() - tic} - {len(a)}")

        tic = datetime.now()
        b = self.get_reachable_bfs_tree(start)
        print(f"BFS: {datetime.now() - tic} - {len(b)}")

        tic = datetime.now()
        c = self.get_reachable_iterative(start)
        print(f"ITER: {datetime.now() - tic} - {len(c)}")

        tic = datetime.now()
        d = self.get_reachable_recursive(start)
        print(f"REC: {datetime.now() - tic} - {len(d)}")

        return a


    def get_reachable_bfs_tree(self, start):
        """Usa networkx.bfs_tree per ottenere i nodi raggiungibili (esclude il nodo iniziale)."""
        # Va per livelli: prima tutti i nodi vicini, poi quelli a distanza maggiore (Queue)
        tree=nx.bfs_tree(self.G, start)
        nodi=list(tree.nodes)
        if start in nodi:
            nodi.remove(start)
        return nodi

    def get_reachable_dfs_tree(self, start):
        """Usa networkx.dfs_tree per ottenere i nodi raggiungibili (esclude il nodo iniziale)."""
        # Va in profondità lungo un ramo finché possibile, poi torna indietro (backtracking) (Stack).
        tree = nx.dfs_tree(self.G, start)
        nodes = list(tree.nodes)
        if start in nodes:
            nodes.remove(start)
        return nodes

    def get_reachable_iterative(self, start):
        """Implementazione iterativa (simile a BFS) che restituisce tutti i nodi raggiungibili."""
        from collections import deque
        #metodo che mi permette di creare una simil-lista che mi permette di prendere sia gli ultimi elementi della lista, sia
        #quelli iniziali

        visited = []
        to_be_visited = deque()  # una double-ended queue (coda a doppia estremità)
        #posso gestire gli elementi dalle doppie estremità, sia dall'inizio che dalla fine

        # add starting node to visited
        visited.append(start) #appendo alla lista il mio elemento di partenza

        # add neighbors of starting node to queue
        to_be_visited.extend(self.G.neighbors(start)) #estendo la coda con tutti i vicini al nodo di partenza

        while to_be_visited: #contnua finchè la lista to_be_visited non è finita
            temp = to_be_visited.popleft()  # prende l'elemento in testa alla coda, lo rimuove da to_be_visited e lo aggiunge a temp

            # mark visited
            visited.append(temp)

            neighbors = list(self.G.neighbors(temp))

            # filter neighbors already visited
            neighbors = [n for n in neighbors if n not in visited]

            # filter neighbors already in to_be_visited
            neighbors = [n for n in neighbors if n not in to_be_visited]

            # enqueue remaining
            to_be_visited.extend(neighbors) #aggiungo gli elementi che non ho già visitato, ma che voglio visitare alla fine di to_be_visited

        # remove starting node from result
        if start in visited:
            visited.remove(start)
        return visited

    def get_reachable_recursive(self, start): #start è il nodo che passo da parametro
        """Versione ricorsiva (DFS) per ottenere i nodi raggiungibili."""
        visited = [] #lista di nodi visitati
        self._recursive_visit(start, visited) #funzione di ricorsione
        if start in visited: #punto limite
            visited.remove(start)
        return visited

    def _recursive_visit(self, node, visited):
        visited.append(node) #metto il nodo che sto passando da parametro come visitato
        for neigh in self.G.neighbors(node): #prendo tutti gli elementi vicini a quel nodo specifico
            if neigh not in visited: #man mano che vedo tutti i possibili vicini, controllo di non aver già visitato quel nodo
                #quando non ho più nodi da visitare finisce
                self._recursive_visit(neigh, visited) #replico sul nuovo nodo vicino
