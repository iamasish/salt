# -*- coding: utf-8 -*-
'''
integration tests for mac_timezone
'''

# Import python libs
from __future__ import absolute_import
from datetime import datetime

# Import Salt Testing libs
from salttesting.helpers import ensure_in_syspath
ensure_in_syspath('../../')

# Import salt libs
import integration
import salt.utils

USE_NETWORK_TIME = False
TIME_SERVER = 'time.apple.com'
TIME_ZONE = ''


class MacTimezoneModuleTest(integration.ModuleCase):
    '''
    Validate the mac_timezone module
    '''

    def setUp(self):
        '''
        Get current settings
        '''
        if not salt.utils.is_darwin():
            self.skipTest('Test only available on Mac OS X')
        if not salt.utils.which('xattr'):
            self.skipTest('Test requires xattr binary')
        if salt.utils.get_uid(salt.utils.get_user()) != 0:
            self.skipTest('Test requires root')

        USE_NETWORK_TIME = self.run_function('timezone.get_using_network_time')
        TIME_SERVER = self.run_function('timezone.get_time_server')
        TIME_ZONE = self.run_function('timezone.get_zone')
        super(MacTimezoneModuleTest, self).setUp()

    def tearDown(self):
        '''
        Reset to original settings
        '''
        self.run_function('timezone.set_time_server', [TIME_SERVER])
        self.run_function('timezone.set_using_network_time', [USE_NETWORK_TIME])
        self.run_function('timezone.set_zone', [TIME_ZONE])
        super(MacTimezoneModuleTest, self).tearDown()

    def test_get_set_date(self):
        '''
        Test timezone.get_date
        Test timezone.set_date
        '''
        self.run_function('timezone.set_date', ['2/20/2011'])
        self.assertEqual(self.run_function('timezone.get_date'), '2/20/2011')

    def test_get_set_time(self):
        '''
        Test timezone.get_time
        Test timezone.set_time
        '''
        self.run_function('timezone.set_time', ['3:14'])
        new_time = self.run_function('timezone.get_time')
        new_time = datetime.strptime(new_time, '%H:%M:%S').strftime('%H:%M')
        self.assertEqual(new_time, '03:14')

    def test_get_set_zone(self):
        '''
        Test timezone.get_zone
        Test timezone.set_zone
        '''
        self.run_function('timezone.set_zone', ['Pacific/Wake'])
        self.assertEqual(self.run_function('timezone.get_zone'), 'Pacific/Wake')

    def test_get_offset(self):
        '''
        Test timezone.get_offset
        '''
        self.run_function('timezone.set_zone', ['Pacific/Wake'])
        self.assertEqual(self.run_function('timezone.get_offset'), '+1200')

    def test_get_zonecode(self):
        '''
        Test timezone.get_zonecode
        '''
        self.run_function('timezone.set_zone', ['Pacific/Wake'])
        self.assertEqual(self.run_function('timezone.get_zonecode'), 'WAKT')

    def test_list_zones(self):
        '''
        Test timezone.list_zones
        '''
        ret = self.run_function('timezone.list_zones')


if __name__ == '__main__':
    from integration import run_tests
    run_tests(MacXattrModuleTest)
