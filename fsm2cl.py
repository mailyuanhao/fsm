import fsm
import os
import sys

EVENT_DEF = "/*@@_USER_EVENT_ENUM_@@*/"
STATE_DEF = "/*@@_USER_STATE_ENUM_@@*/"
ACTION_FUNCS_DEF = "/*@@_USER_ACTIONS_DEF_@@*/"
GUARD_FUNCS_DEF = "/*@@_USER_EVENTS_DEF_@@*/"
INIT_EVENT_CASE_DEF = "/*@@_INIT_EVENT_BODY_@@*/"


class Machine2CL:
    def __init__(self, machine: fsm.FSMMachine, line_split="\n"):
        super().__init__()
        self.machine = machine
        self.line_split = "\n"

    def __load_template(self) -> (str, str):
        dir = os.path.dirname(os.path.abspath(__file__))
        with open(dir + r"/c_template/header_template.h") as header, open(dir + r"/c_template/src_template.c") as src:
            h = header.read()
            s = src.read()
        return h, s

    def __mk_user_state_enum(self) -> str:
        machine = self.machine
        t = "{m}_state_{s} = {i},"
        e = [t.format(m=machine.name, s=e[0], i=e[1])
             for e in zip(machine.states, range(len(machine.states)))]
        e.append(self.machine.name + "_state_" + "invalid = -1")
        return "\n".join(e)

    def __mk_user_event_enum_names(self):
        machine = self.machine
        t = "{m}_event_{e}"
        e = {e: t.format(m=machine.name, e=e.name)
             for e in machine.events}
        return e

    def __write_user_event_enums(self, h, ee):
        l = ["{e} = {i},".format(e=z[0],  i=z[1])
             for z in zip(ee.values(), range(len(ee)))]
        return h.replace(EVENT_DEF, self.line_split.join(l))

    def __mk_action_funcs(self) -> str:
        t = "void {func} (pMachine, pBaseEvent);"
        actions = [t.format(func=x.action)
                   for x in self.machine.transition_table if x.action]
        return "\n".join(actions)

    def __mk_guard_funcs(self) -> str:
        t = "int {func} (pMachine, pBaseEvent);"
        actions = [t.format(func=x.guard)
                   for x in self.machine.transition_table if x.guard]
        return "\n".join(actions)

    def __mk_unique_str(self, i):
        s = "abcdefghijklmnopqrstuvwxyz"
        b = "-"
        l = len(s)
        return b * int(i / l) + s[i % l]

    def __mk_event_rlstr(self):
        return {z[0]: self.__mk_unique_str(z[1]) for z in zip(self.machine.events, range(len(self.machine.events)))}

    def __mk_init_event_cases(self, ee, es):
        return ['case {ee}: event->_event_str = "{es}"; break;'.format(
            ee=ee[k], es=es[k]) for k in ee.keys()]

    def show(self, header_fp, rl_fp):
        h, s = self.__load_template()

        h = h.replace(STATE_DEF, self.__mk_user_state_enum())

        ee = self.__mk_user_event_enum_names()
        h = self.__write_user_event_enums(h, ee)

        h = h.replace(ACTION_FUNCS_DEF, self.__mk_action_funcs())
        h = h.replace(GUARD_FUNCS_DEF, self.__mk_guard_funcs())

        es = self.__mk_event_rlstr()

        s = s.replace(INIT_EVENT_CASE_DEF, self.line_split.join(
            self.__mk_init_event_cases(ee, es)))

        header_fp.write(h)
        rl_fp.write(s)
