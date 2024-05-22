from typing import List
from tests import IntegrationTest

class TestGetInstrumentIsUsed(IntegrationTest):
    
    def create_answer_false(self, user_id, date_id):
        id = self.create_answer(user_id=user_id, date_id=date_id)
        return self.update_answer(id, False)

    def setUp(self):
        super().setUp()
        self.user1_id = self.create_user('user1', self.instru1_id, [self.instru2_id])
        self.user2_id = self.create_user('user2', self.instru1_id, [])
        self.date1_id = self.create_date(date='2025-03-10', time='15:00:00', title='firstDate', end_time=None)

        

    def test_not_used_at_all(self):            
        _json = self.get_instruments()
        assert len(_json['instruments']) == 3
        print(_json['instruments'][0]['is_used'])
        
        def _assertInstrument(instruments, id, is_used):
            instru = [instru for instru in instruments if instru['instrument']['id'] == id][0]
            assert instru['is_used'] == is_used
        
        _assertInstrument(_json['instruments'], 1, True)
        _assertInstrument(_json['instruments'], 2, True)
        _assertInstrument(_json['instruments'], 3, False)
