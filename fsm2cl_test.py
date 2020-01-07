import os
import sys
import unittest
from io import StringIO

import fsm
from fsm2cl import Machine2CL


class FSM2ClTest(unittest.TestCase):
    def setUp(self):
        super(FSM2ClTest, self).setUp
        self.project_path = os.path.dirname(
            os.path.abspath(__file__))
        with open(self.project_path + r"/testjson/sample.json") as fp:
            self.machine = fsm.FsmLoaderFromJson().load(fp)

    def test_machine2cl(self):
        mc = Machine2CL(self.machine)
        h = StringIO()
        rl = StringIO()
        mc.show(h, rl)
        print(h.getvalue(), rl.getvalue())
