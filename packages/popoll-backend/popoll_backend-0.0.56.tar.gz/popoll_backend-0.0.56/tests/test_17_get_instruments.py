from tests import IntegrationTest

class TestGetInstruments(IntegrationTest):

    def setUp(self):
        super().setUp()
        self.user1_id = self.create_user('user1', self.instru1_id, [self.instru2_id])

    def test_get_instruments(self):            
        _json = self.get_instruments()
        assert len(_json['instruments']) == 3
        assert self.INSTRU1 in [i['instrument']['name'] for i in _json['instruments']]
        assert self.INSTRU2 in [i['instrument']['name'] for i in _json['instruments']]
        assert self.INSTRU3 in [i['instrument']['name'] for i in _json['instruments']]

