import unittest
import typewise_alert


class TypewiseTest(unittest.TestCase):
    def test_infers_breach_as_per_limits(self):
        self.assertTrue(typewise_alert.infer_breach(20, 50, 100) == 'TOO_LOW')
        self.assertTrue(typewise_alert.infer_breach(110, 50, 100) == 'TOO_HIGH')
        self.assertTrue(typewise_alert.infer_breach(60, 50, 100) == 'NORMAL')

    def test_classify_temperature_breach(self):
        self.assertTrue(typewise_alert.classify_temperature_breach('PASSIVE_COOLING', 50) == 'TOO_HIGH')
        self.assertTrue(typewise_alert.classify_temperature_breach('HI_ACTIVE_COOLING', 10) == 'NORMAL')
        self.assertTrue(typewise_alert.classify_temperature_breach('MED_ACTIVE_COOLING', 45) == 'TOO_HIGH')
        self.assertTrue(typewise_alert.classify_temperature_breach('HI_ACTIVE_COOLING', 100) == 'TOO_HIGH')
        self.assertTrue(typewise_alert.classify_temperature_breach('PASSIVE_COOLING', 20) == 'NORMAL')
        self.assertTrue(typewise_alert.classify_temperature_breach('HI_ACTIVE_COOLING', -10) == 'TOO_LOW')
        self.assertTrue(typewise_alert.classify_temperature_breach('ACTIVE_COOLING', 40) == 'no such cooling type')

    def test_send_to_controller(self):
        self.assertTrue(typewise_alert.send_to_controller('TOO_HIGH') == f'{0xfeed}, TOO_HIGH')
        self.assertTrue(typewise_alert.send_to_controller('TOO_LOW') == f'{0xfeed}, TOO_LOW')
        self.assertTrue(typewise_alert.send_to_controller('NORMAL') == '')

    def test_send_to_email(self):
        self.assertTrue(typewise_alert.send_to_email('TOO_HIGH') == 'To: a.b@c.com, c.a@b.com\nHi, the temperature is too high')
        self.assertTrue(typewise_alert.send_to_email('TOO_LOW') == 'To: a.b@c.com, c.a@b.com\nHi, the temperature is too low')
        self.assertTrue(typewise_alert.send_to_email('NORMAL') == '')

    def test_check_and_alert_as_per_limits(self):
        self.assertTrue(typewise_alert.check_and_alert("TO_EMAIL", {'coolingType' : 'HI_ACTIVE_COOLING'}, 90 ) == 'To: a.b@c.com, c.a@b.com\nHi, the temperature is too high')
        self.assertTrue(typewise_alert.check_and_alert("TO_EMAIL", {'coolingType' : 'MED_ACTIVE_COOLING'}, -1 ) == 'To: a.b@c.com, c.a@b.com\nHi, the temperature is too low')
        self.assertTrue(typewise_alert.check_and_alert("TO_EMAIL", {'coolingType' : 'HI_ACTIVE_COOLING'}, 10 ) == '')
        self.assertTrue(typewise_alert.check_and_alert("TO_EMAIL", {'coolingType' : 'PASSIVE_COOLING'}, 20 ) == '')
        self.assertTrue(typewise_alert.check_and_alert("TO_CONTROLLER", {'coolingType' : 'MED_ACTIVE_COOLING'}, 60) == f'{0xfeed}, TOO_HIGH')
        self.assertTrue(typewise_alert.check_and_alert("TO_CONTROLLER", {'coolingType' : 'HI_ACTIVE_COOLING'}, -1) == f'{0xfeed}, TOO_LOW')
        self.assertTrue(typewise_alert.check_and_alert("TO_CONTROLLER", {'coolingType' : 'PASSIVE_COOLING'}, 0) == '')
if __name__ == '__main__':
  unittest.main()
