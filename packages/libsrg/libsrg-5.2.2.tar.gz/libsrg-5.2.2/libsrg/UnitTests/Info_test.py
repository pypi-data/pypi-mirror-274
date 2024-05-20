# libsrg (Code and Documentation) is published under an MIT License
# Copyright (c) 2023,2024 Steven Goncalo
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

import unittest
from libsrg.Info import Info
import os
import pprint
class MyTestCase(unittest.TestCase):
    def test_something(self):
        info = Info()
        con = info.to_config()
        sysname,nodename,release,version,machine = os.uname()
        pprint.pp(con)
        self.assertEqual(machine, con["machine"])
        self.assertEqual(nodename, con["fqdn"])
        self.assertEqual(release, con["kernel"])


if __name__ == '__main__':
    unittest.main()
