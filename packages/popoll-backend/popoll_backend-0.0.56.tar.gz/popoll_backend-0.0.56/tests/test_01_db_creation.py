from tests import IntegrationTest

class TestDBCreation(IntegrationTest):

    def test_db_creation(self):
        _json = self.get_instruments()
        
        assert _json['instruments'][0]['instrument']['id'] == self.instru1_id
        assert _json['instruments'][0]['instrument']['name'] == self.INSTRU1
        assert _json['instruments'][1]['instrument']['id'] == self.instru3_id
        assert _json['instruments'][1]['instrument']['name'] == self.INSTRU3
        assert _json['instruments'][2]['instrument']['id'] == self.instru2_id
        assert _json['instruments'][2]['instrument']['name'] == self.INSTRU2
