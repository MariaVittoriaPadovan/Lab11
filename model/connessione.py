from dataclasses import dataclass
import datetime #per prendere il valore come tempo
from model.rifugio import Rifugio #così all'interno dell'oggetto Connessione avrò gli oggetti Rifugio corrispondenti

@dataclass
class Connessione:
    r1: Rifugio #rifugio di partenza
    r2: Rifugio #rifugio di arrivo
    distanza: float = 0.0 #la impongo come valore di default a zero
    difficolta: str = "facile" #la impongo di default a facile
    durata: datetime.time = datetime.time(0, 0, 0) #la impongo di default a 0 ore 0 minuti e 0 secondi

    def __str__(self):
        return (f"Connessione: {self.r1.nome} - {self.r2.nome}, distanza: {self.distanza} km, difficoltà: {self.difficolta}, tempo: {self.durata}")
