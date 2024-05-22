import sqlite3
from typing import List

from popoll_backend.model.db.instrument import Instrument
from popoll_backend.model.payload.instruments_payload import InstrumentsPayload
from popoll_backend.query import Query


class GetInstruments(Query):
    
    instruments: List[Instrument]
    all_used_instruments: List[int]
    
    def __init__(self, poll: str):
        super().__init__(poll)
    
    def process(self, cursor: sqlite3.Cursor):
        self.instruments = [Instrument(row) for row in cursor.execute('SELECT * from instruments.instruments ORDER BY rank').fetchall()]
        self.all_used_instruments = [i[0] for i in cursor.execute('SELECT DISTINCT instrument_id FROM user_instruments').fetchall()]
        
    def buildResponse(self, cursor: sqlite3.Cursor) -> InstrumentsPayload:
        return InstrumentsPayload(self.instruments, self.all_used_instruments)