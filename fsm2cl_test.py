import os
import sys
import unittest
import string
import random

import fsm
from fsm2cl import Machine2CL
from mkrandomfsm import mk_fsm


def random_str(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


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

    def test_randomcl(self):
        s = set([random_str(random.randint(5, 10)) for i in range(20)])
        e = set([random_str(random.randint(5, 10)) for i in range(40)])

        ml = mk_fsm("test", s, e)
        print(ml)
        machine = fsm.FsmLoaderFromJson().loads(ml)
        mc = Machine2CL(machine)
        dir = os.path.dirname(os.path.abspath(__file__))
        with open(dir + r"/test_machine.h", r"w") as header, open(dir + r"/src.rl", r"w") as src:
            mc.show("test_machine", header, src)
