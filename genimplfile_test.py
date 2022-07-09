from pathlib import Path
from io import BytesIO
import unittest
from genimplfile import mk_src_content, parse_header_file

src = '''
# ifndef _CD_MACHINE_H_
# define _CD_MACHINE_H_

namespace cd_machine{

enum
{
    CD_MACHINE_state_Playing = 0,
CD_MACHINE_state_PalyInvalid = 1,
CD_MACHINE_state_Closed = 2,
CD_MACHINE_state_Opened = 3,
CD_MACHINE_state_invalid = -1
};

typedef struct _Machine
{
    int state;
    void *user_data;
    char _inner_ml[0];
} Machine, *pMachine;

enum
{
    CD_MACHINE_event_Play = 0,
CD_MACHINE_event_OpenClose = 1,
CD_MACHINE_event_Stop = 2,
CD_MACHINE_event_invalid = -1,
};

typedef struct _Event
{
    int event;
    const char *_event_str;
    void *user_data;
} BaseEvent, *pBaseEvent;

pMachine new_machine();
void delete_machine(pMachine p);

pBaseEvent new_event(int type);
void delete_event(pBaseEvent p);

//Plz implement these memory functions
void *user_malloc(int size);
void user_free(void *);

void process(pMachine pm, pBaseEvent pbe);

//how to play
/*
{
pMachine m = new_machine();
m->user_data=YourCtx;

pBaseEvent p = new_event(EventTypeEnum);
process(m, p);
delete_event(p);

pBaseEvent p2 = new_event(EventTypeEnum);
process(m, p2);
delete_event(p2);

delete_machine(m);
}
*/

//implement your atcions and guards

void from_Closed_to_Opened_event_OpenClose_action (pMachine, pBaseEvent);
void from_Opened_to_Closed_event_OpenClose_action (pMachine, pBaseEvent);
void from_Closed_to_Playing_event_Play_action (pMachine, pBaseEvent);
void unexpected_event_action (pMachine, pBaseEvent);

//0 for deny 1 for ok
int from_Closed_to_Opened_event_OpenClose_guard (pMachine, pBaseEvent);
int from_Closed_to_Playing_event_Play_guard (pMachine, pBaseEvent);
int from_Closed_to_PalyInvalid_event_Play_guard (pMachine, pBaseEvent);
int from_Playing_to_Closed_event_Stop_guard (pMachine, pBaseEvent);

}
# endif //_ML_DEF_H_
'''


class GenimplFileTest(unittest.TestCase):
    def setUp(self) -> None:
        super(GenimplFileTest, self).setUp
        self.src_file = BytesIO()
        self.src_file.write(bytes(src, r'utf-8'))
        self.src_file.seek(0)

    def test_parsefile(self):
        namespace, a, actions, guards = parse_header_file(self.src_file)
        self.assertEqual(namespace, "cd_machine")
        actions_str = '''from_Closed_to_Opened_event_OpenClose_action
from_Opened_to_Closed_event_OpenClose_action
from_Closed_to_Playing_event_Play_action
unexpected_event_action'''
        self.assertEqual(actions, actions_str.split('\n'))
        guards_str = '''from_Closed_to_Opened_event_OpenClose_guard
from_Closed_to_Playing_event_Play_guard
from_Closed_to_PalyInvalid_event_Play_guard
from_Playing_to_Closed_event_Stop_guard'''
        self.assertEqual(guards, guards_str.split('\n'))

        src_content = mk_src_content(
            Path("/mnt/c/d/abc.h").name, namespace, actions, guards)
