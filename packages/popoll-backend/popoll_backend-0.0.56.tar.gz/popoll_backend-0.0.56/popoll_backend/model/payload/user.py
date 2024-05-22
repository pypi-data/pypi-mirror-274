from typing import Any, List
from popoll_backend.model import Payload
from popoll_backend.model.db.user import User
from popoll_backend.model.db.instrument import Instrument
from popoll_backend.model.db.user_instruments import UserInstruments


class UserOut(Payload):
    
    def __init__(self, user: User, instruments: Instrument, user_instruments: List[UserInstruments]):
        self.user = user
        self.main_instrument: Instrument = self.getInstrument(instruments, self.getInstrumentIds(user_instruments, user.id, True)[0])
        self.instruments: List[Instrument] = self.getInstruments(instruments, self.getInstrumentIds(user_instruments, user.id, False))
        
    def getInstrumentIds(self, user_instruments: List[UserInstruments], user_id: int, is_main: bool):
        return [user_instrument.instrument_id for user_instrument in user_instruments if user_instrument.user_id == user_id and user_instrument.is_main == is_main]
    
    def getInstruments(self, instruments: List[Instrument], ids: List[int]):
        return [instrument for instrument in instruments if instrument.instrument.id in ids]
    
    def getInstrument(self, instruments: List[Instrument], id: int):
        return [instrument for instrument in instruments if instrument.instrument.id == id][0]