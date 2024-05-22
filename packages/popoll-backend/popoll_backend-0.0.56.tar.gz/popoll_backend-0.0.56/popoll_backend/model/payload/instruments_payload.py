from typing import List
from popoll_backend.model.db.instrument import Instrument
from popoll_backend.model import Payload
from popoll_backend.model.payload.instrument_payload import InstrumentPayload

class InstrumentsPayload(Payload):
    
    def __init__(self, instruments: List[Instrument], all_used_instruments: List[int]):
        self.instruments: List[InstrumentPayload] = [InstrumentPayload(instrument, instrument.id in all_used_instruments) for instrument in instruments]