import os
import sys
import unittest

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
        dir = os.path.dirname(os.path.abspath(__file__))
        with open(dir + r"/test_machine.h", r"w") as header, open(dir + r"/src.rl", r"w") as src:
            mc.show("test_machine", header, src)
