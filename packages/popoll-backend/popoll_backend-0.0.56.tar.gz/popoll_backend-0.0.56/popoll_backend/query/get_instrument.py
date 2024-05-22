import sqlite3

from popoll_backend.model.db.instrument import Instrument
from popoll_backend.model.payload.instrument_payload import InstrumentPayload
from popoll_backend.query import Query


class GetInstrument(Query):
    
    id: int
    
    def __init__(self, poll: str, id: int):
        super().__init__(poll)
        self.id = id
    
    def process(self, cursor: sqlite3.Cursor):
        pass
        
    def buildResponse(self, cursor: sqlite3.Cursor) -> InstrumentPayload:
        instrument: Instrument = self.selectItem(cursor, 'SELECT * FROM instruments.instruments WHERE id=?', self.id, Instrument)
        all_used_instruments = cursor.execute('SELECT COUNT(instrument_id) FROM user_instruments WHERE instrument_id = ?', (self.id,)).fetchall()
        return InstrumentPayload(instrument, all_used_instruments[0][0] > 0)