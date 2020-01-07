import json
import re
from typing import List

START_NAME = "start"
EVENT_NAME = "event"
TARGET_NAME = "target"
ACTION_NAME = "action"
GUARD_NAME = "guard"
SN_NAME = "sn"
MACHINE_NAME = "machine"
INIT_STATE_NAME = "init_state"
TRANSITION_TABLE_NAME = "transition_table"


ELEM_NAME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]*$")


def name_valid(name: str):
    if not isinstance(name, str):
        return False

    return ELEM_NAME_RE.match(name) is not None


class TransitionDict:
    def __init__(self, transition_dict: dict):
        self.__keys = (START_NAME, EVENT_NAME, TARGET_NAME)
        self.transition_dict = transition_dict

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return all(self.transition_dict[k] == other.transition_dict[k] for k in self.__keys)

    def __hash__(self):
        names = [self.transition_dict[k] for k in self.__keys]
        return hash(",".join(names))

    def __is_valid(self):
        if not isinstance(self.transition_dict, dict):
            return False, "invlaid transition_dict type"

        if any(k not in self.transition_dict for k in self.__keys):
            return False, "lack of Necessary key"

        return all(name_valid(self.transition_dict[k]) for k in self.__keys)


class Item:
    def __init__(self, name: str):
        if ELEM_NAME_RE.match(name) is None:
            raise ValueError("Invalid Item name {0}".format(name))
        self.name = name

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.name == other.name


class State(Item):
    def __init__(self, name):
        super(State, self).__init__(name)
        self.enter_transition = list()
        self.leave_transition = list()

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.name == other.name


class Event(Item):
    pass


class Transition:
    def __init__(self, start: State, event: Event, target: State, action: str, guard: str, sn: int):
        self.start = start
        self.event = event
        self.target = target
        self.action = action
        self.guard = guard
        self.sn = sn


class FSMMachine:
    def __init__(self, name: str, init_state_name: str, transition_dict_table: List[TransitionDict]):
        self.name = name
        self.init_state_name = init_state_name
        self.init_state = None
        self.__transition_table = list()
        self.__states = set()
        self.__events = set()
        self.__mk_transition_table(transition_dict_table)
        self.__check_machine()

    @property
    def events(self):
        return self.__events

    @property
    def states(self):
        return self.__states

    @property
    def transition_table(self):
        return self.__transition_table

    def __str__(self):
        return self.name

    def __mk_transition_table(self, transition_dict_table: List[TransitionDict]):
        if len(set(transition_dict_table)) != len(transition_dict_table):
            raise ValueError("duplicate transition")

        for trd in transition_dict_table:
            s = self.__new_state(trd.transition_dict[START_NAME])
            e = self.__new_event(trd.transition_dict[EVENT_NAME])
            t = self.__new_state(trd.transition_dict[TARGET_NAME])
            sn = trd.transition_dict[SN_NAME]

            a = None
            if ACTION_NAME in trd.transition_dict and trd.transition_dict[ACTION_NAME]:
                a = "from_{0}_to_{1}_event_{2}_action".format(
                    s.name, t.name, e.name)
            g = None
            if GUARD_NAME in trd.transition_dict and trd.transition_dict[GUARD_NAME]:
                g = "from_{0}_to_{1}_event_{2}_guard".format(
                    s.name, t.name, e.name)

            tr = Transition(s, e, t, a, g, sn)
            s.leave_transition.append(tr)
            t.enter_transition.append(tr)
            self.__transition_table.append(tr)

    def __check_machine(self):
        if len(self.transition_table) == 0:
            raise ValueError("Empty Transition Table")

        for s in self.states:
            if s.name == self.init_state_name:
                self.init_state = s
            else:
                if len(s.enter_transition) == 0:
                    raise ValueError("Not Init State has no enter transition")

    def __new_state(self, name: str):
        for x in self.__states:
            if name == x.name:
                return x
        x = State(name)
        self.__states.add(x)
        return x

    def __new_event(self, name: str):
        for x in self.__events:
            if name == x.name:
                return x
        x = Event(name)
        self.__events.add(x)
        return x


class FsmLoaderFromJson:
    def __init__(self):
        pass

    def __mk_td(self, o, i):
        if isinstance(o, dict):
            o[SN_NAME] = i
            return o
        elif isinstance(o, list) and len(o) >= 3:
            d = {START_NAME: o[0], EVENT_NAME: o[1],
                 TARGET_NAME: o[2], SN_NAME: i}
            if len(o) >= 4:
                d[ACTION_NAME] = o[3]
            if len(o) >= 5:
                d[GUARD_NAME] = o[4]
            return d
        else:
            raise ValueError("invalid transition")

    def __mk_fsm(self, obj) -> FSMMachine:
        name = obj[MACHINE_NAME]
        if ELEM_NAME_RE.match(name) is None:
            raise ValueError("Invalid machine name {0}".format(name))

        init_state = obj[INIT_STATE_NAME]
        if ELEM_NAME_RE.match(name) is None:
            raise ValueError("Invalid state name {0}".format(init_state))

        trt = obj[TRANSITION_TABLE_NAME]
        trs = [TransitionDict(self.__mk_td(d[0], d[1]))
               for d in zip(trt, range(len(trt)))]

        return FSMMachine(name, init_state, trs)

    def load(self, fp):
        obj = json.load(fp)
        return self.__mk_fsm(obj)

    def loads(self, j):
        obj = json.loads(j)
        return self.__mk_fsm(obj)


class Machine2Dot:
    __entry_type = "shape = point"
    __common_state = "shape = circle"
    __end_state = "fixedsize = true, height = 0.65, shape = doublecircle"
    __graph_parameters = "rankdir = LR;"

    def __init__(self, **kwargs):
        self.__entry_type = Machine2Dot.__entry_type
        self.__common_state = Machine2Dot.__common_state
        self.__end_state = Machine2Dot.__end_state
        self.__graph_parameters = Machine2Dot.__graph_parameters

    def __mk_entry(self, fsm: FSMMachine):
        l = []
        n = "node [{0}];".format(self.__entry_type)
        l.append(n)
        l.append("Entry;")

        return l

    def __mk_nodes(self, fsm: FSMMachine):
        l = []
        n = "node[{0}];".format(self.__common_state)
        l.append(n)
        for s in fsm.states:
            n += "{0};".format(s.name)
            l.append(n)
        return l

    def __mk_transition(self, tr: Transition):
        edge_style = "dashed" if tr.guard else "solid"
        label = '[label = "event:{e}\naction:{a}\nguard:{g}" style = {s}]'.format(
            e=str(tr.event), a=tr.action, g=tr.guard, s=edge_style)
        t = "{s} -> {t} {l};".format(s=str(tr.start),
                                     t=str(tr.target),
                                     l=label)
        return [t]

    def Show(self, fsm: FSMMachine):
        g = []
        g.append("digraph {0} {{".format(
            fsm.name))
        g.append(self.__graph_parameters)
        g += self.__mk_entry(fsm)
        g += self.__mk_nodes(fsm)
        for tr in fsm.transition_table:
            g += self.__mk_transition(tr)
        g.append(
            '{e} -> {i} [label = "Entry"];'.format(i=fsm.init_state_name, e="Entry"))
        g.append("}")
        return "\n".join(g)
