from uuid import NAMESPACE_DNS
import fsm
import os
from typing import List, Tuple
from operator import attrgetter

EVENT_DEF = "/*@@_USER_EVENT_ENUM_@@*/"
STATE_DEF = "/*@@_USER_STATE_ENUM_@@*/"
ACTION_FUNCS_DEF = "/*@@_USER_ACTIONS_DEF_@@*/"
GUARD_FUNCS_DEF = "/*@@_USER_EVENTS_DEF_@@*/"
INIT_EVENT_CASE_DEF = "/*@@_INIT_EVENT_BODY_@@*/"
INIT_ENTRY_STATE_DEF = "/*@@_ENTRY_STAE_ENUM_@@*/"
RL_DEF = "/*@@_RLS_@@*/"
MACHINE_NAME_DEF = "/*@@_MACHINE_NAME_@@*/"
HEADER_GUARD_DEF = "/*@@_ML_HEADER_NAME_DEF_H_@@*/"
HEADER_FILE_NAME_DEF = "/*@@_HEADER_NAME_@@*/"
NAMESPACE_NAME_DEF = "/*@@_NAMESPACE_NAME_@@*/" 


class Machine2CL:
    def __init__(self, machine: fsm.FSMMachine, line_split="\n"):
        super().__init__()
        self.machine = machine
        self.line_split = "\n"
        #为了防止状态机进入异常状态，状态机接收到非期望的event时会忽略掉该event，并调用如下函数
        self.unexpected_event_action_name = "UNEXPECTED_EVENT_ACTION"
        self.unexpected_event_action_function_name = "unexpected_event_action"

    def __load_template(self) -> Tuple[str, str]:
        dir = os.path.dirname(os.path.abspath(__file__))
        with open(dir + r"/c_template/header_template.h") as header, open(dir + r"/c_template/src_template.rl") as src:
            h = header.read()
            s = src.read()
        return h, s

    def __set_init_state(self, src, states_enum):
        return src.replace(INIT_ENTRY_STATE_DEF,
                           states_enum[self.machine.init_state])

    def __mk_user_state_names(self, states_enum) -> str:
        machine = self.machine
        t = "{s} = {i},"
        e = [t.format(s=e[0], i=e[1])
             for e in zip(states_enum.values(), range(len(machine.states)))]
        e.append(self.machine.name + "_state_" + "invalid = -1")
        return "\n".join(e)

    def __mk_user_state_enum(self) -> str:
        machine = self.machine
        t = "{m}_state_{s}"
        return {e: t.format(m=machine.name, s=e)
                for e in machine.states}

    def __mk_user_event_enum_names(self):
        machine = self.machine
        t = "{m}_event_{e}"
        e = {e: t.format(m=machine.name, e=e.name)
             for e in machine.events}
        return e

    def __write_user_event_enums(self, h, ee):
        l = ["{e} = {i},".format(e=z[0],  i=z[1])
             for z in zip(ee.values(), range(len(ee)))]
        l.append("{m}_event_invalid = -1,".format(m=self.machine.name))
        return h.replace(EVENT_DEF, self.line_split.join(l))

    def __mk_action_funcs(self) -> str:
        t = "void {func} (pMachine, pBaseEvent);"
        actions = [t.format(func=x.action)
                   for x in self.machine.transition_table if x.action]
        actions.append(t.format(func=self.unexpected_event_action_function_name))
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

    def __join_state_tr(self, trs: List[fsm.Transition]):
        '''
        允许一个状态接收同一个事件，有多种跳转方式。
        依照用户配置的顺序挨个尝试每种跳转的guard（如果没有guard，默认允许），直到第一个允许的
        guard，则执行该跳转。
        '''
        trs = sorted(trs, key=attrgetter("sn"))
        event_2_transition = dict()
        for tr in trs:
            if tr.event in event_2_transition:
                event_2_transition[tr.event].append(tr)
            else:
                event_2_transition[tr.event] = [tr]
        return event_2_transition

    def __set_state_rl(self, state: fsm.State,
                       state_2_enum,
                       event_2_enum,
                       event_2_ragel_str):
        transition_template = '"{s}" @ {action};'
        entry_template = '''{state_name}:= |* {transitions} *|;'''

        state_event_2_trs = self.__join_state_tr(state.leave_transition)

        rl_tr_entry = list()
        state_event_2_tr_action_name = dict()
        for t in state_event_2_trs:
            action_name = state.name + "_" + str(t)
            state_event_2_tr_action_name[t] = action_name
            rl_tr = transition_template.format(
                s=event_2_ragel_str[t], action=action_name)
            rl_tr_entry.append(rl_tr)

        # rl state entry Opened: = |* "a" @ Opened_OpenClose; * |
        rl_tr_entry.append('{s} @ {action};'.format(s="any*", action=self.unexpected_event_action_name))
        rl_state_entry = entry_template.format(state_name=state.name,
                                               transitions=self.line_split.join(
                                                   rl_tr_entry)
                                               )

        # rl entry action 代码片段
        action_rl_list = list()
        action_template = 'action {name} {{ {body} }}'
        for e, trs in state_event_2_trs.items():
            trc = list()
            trc_template = "if ({guard}){{ pm->state={ts_enum};{action}; fgoto {target_state}; }}"
            for tr in trs:
                guard_str = "1"  # ok string
                if tr.guard:
                    guard_str = "{func}(pm, pbe)".format(
                        func=tr.guard)
                action_str = ""
                if tr.action:
                    action_str = "{func}(pm, pbe)".format(func=tr.action)
                trc.append(trc_template.format(guard=guard_str,
                                               action=action_str,
                                               target_state=tr.target.name,
                                               ts_enum=state_2_enum[tr.target]))
            action_rl = action_template.format(
                name=state_event_2_tr_action_name[e], body=self.line_split.join(trc))
            action_rl_list.append(action_rl)

        return self.line_split.join(action_rl_list) + self.line_split + rl_state_entry + self.line_split

    def __write_all_ragel_entrys(self,
                                 src,
                                 state_2_enum,
                                 event_2_enum,
                                 event_2_ragel_str):
        state_rls = list()

        #添加未预期的事件action
        state_rls.append('action {name} {{ {body}(pm, pbe); }}'.format(
            name=self.unexpected_event_action_name,
            body=self.unexpected_event_action_function_name))

        for s in self.machine.states:
            state_rls.append(self.__set_state_rl(
                s, state_2_enum,
                event_2_enum, event_2_ragel_str))
        state_rls.append(
            "main:=any* @{{fgoto {init};}};".format(init=self.machine.init_state))
        return src.replace(RL_DEF, (self.line_split * 2).join(state_rls))

    def show(self, header_name: str, header_fp, rl_fp):
        h, s = self.__load_template()

        h = h.replace(HEADER_GUARD_DEF, "_{0}_H_".format(header_name.upper()))
        s = s.replace(HEADER_FILE_NAME_DEF, header_name)

        state_2_enum = self.__mk_user_state_enum()
        h = h.replace(STATE_DEF, self.__mk_user_state_names(state_2_enum))
        s = self.__set_init_state(s, state_2_enum)

        s = s.replace(MACHINE_NAME_DEF, self.machine.name)

        event_2_enum = self.__mk_user_event_enum_names()
        h = self.__write_user_event_enums(h, event_2_enum)

        h = h.replace(ACTION_FUNCS_DEF, self.__mk_action_funcs())
        h = h.replace(GUARD_FUNCS_DEF, self.__mk_guard_funcs())

        event_2_ragel_str = self.__mk_event_rlstr()

        s = s.replace(INIT_EVENT_CASE_DEF, self.line_split.join(
            self.__mk_init_event_cases(event_2_enum, event_2_ragel_str)))

        s = self.__write_all_ragel_entrys(
            s, state_2_enum,
            event_2_enum, event_2_ragel_str)

        h = h.replace(NAMESPACE_NAME_DEF, self.machine.name.lower())
        s = s.replace(NAMESPACE_NAME_DEF, self.machine.name.lower())

        header_fp.write(h)
        rl_fp.write(s)
