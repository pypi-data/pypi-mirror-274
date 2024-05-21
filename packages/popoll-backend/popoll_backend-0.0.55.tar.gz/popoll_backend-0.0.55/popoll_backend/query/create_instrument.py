import sqlite3

from popoll_backend.model import Payload
from popoll_backend.query import Query
from popoll_backend.query.get_instrument import GetInstrument


class CreateInstrument(Query):
    
    instrument_id: int
    name: str
    rank: int
    
    def __init__(self, poll: str, name: str, rank: int):
        super().__init__(poll)
        self.name = name
        self.rank = rank
        
    def process(self, cursor: sqlite3.Cursor):
        cursor.execute('INSERT INTO instruments.instruments(name, rank) VALUES (?, ?)', (self.name, self.rank))
        self.instrument_id = cursor.lastrowid
        
    def buildResponse(self, cursor: sqlite3.Cursor) -> Payload:
        return GetInstrument(self.poll, self.instrument_id).run(cursor)
