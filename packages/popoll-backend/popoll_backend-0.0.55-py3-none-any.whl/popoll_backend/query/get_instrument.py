import sqlite3

from popoll_backend.model.db.instrument import Instrument
from popoll_backend.model.payload.instruments_payload import InstrumentsPayload
from popoll_backend.query import Query


class GetInstrument(Query):
    
    id: int
    
    def __init__(self, poll: str, id: int):
        super().__init__(poll)
        self.id = id
    
    def process(self, cursor: sqlite3.Cursor):
        pass
        
    def buildResponse(self, cursor: sqlite3.Cursor) -> InstrumentsPayload:
        return self.selectItem(cursor, 'SELECT * FROM instruments WHERE id=?', self.id, Instrument)