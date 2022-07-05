import fsm
import unittest
import os
import sys


class FsmTest(unittest.TestCase):
    def setUp(self):
        super(FsmTest, self).setUp
        self.project_path = os.path.dirname(
            os.path.abspath(__file__))

    def tearDown(self):
        super(FsmTest, self).tearDown

    def test_mk_fsm_duplicate(self):
        with open(self.project_path + r"/testjson/sample_dupicate_tr.json") as fp:
            self.assertRaises(ValueError, fsm.FsmLoaderFromJson().load, fp)

    def test_mk_fsm(self):
        with open(self.project_path + r"/testjson/sample.json") as fp:
            f = fsm.FsmLoaderFromJson().load(fp)
            self.assertEqual(len(f.states), 4)
            self.assertTrue(all(x.name in ("Opened", "Closed", "Playing", "PalyInvalid")
                                for x in f.states))

            self.assertEqual(len(f.events), 3)
            self.assertTrue(all(x.name in ("OpenClose", "Play", "Stop")
                                for x in f.events))

    def test_mk_dot(self):
        with open(self.project_path + r"/testjson/sample_dot.json") as fp:
            f = fsm.FsmLoaderFromJson().load(fp)
            dot = fsm.Machine2Dot().Show(f)
            print(dot)
