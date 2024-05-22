from tests import IntegrationTest

class TestAddInstrument(IntegrationTest):

    def setUp(self):
        super().setUp()

    def test_get_instruments(self):            
        _json = self.get_instruments()
        assert len(_json['instruments']) == 3
        self.create_instrument('newInstru', 15)
        _json = self.get_instruments()
        assert len(_json['instruments']) == 4
        assert _json['instruments'][1]['instrument']['name'] == 'newInstru'

