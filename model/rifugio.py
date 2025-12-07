from dataclasses import dataclass

@dataclass
class Rifugio:
    id: int
    nome : str
    localita : str
    altitudine : int
    capienza : int
    aperto : int


    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Rifugio) and self.id == other.id

    def __str__(self):
        return f"[{self.id}] {self.nome} ({self.localita})"

