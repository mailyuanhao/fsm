#ifndef /*@@_ML_HEADER_NAME_DEF_H_@@*/
#define /*@@_ML_HEADER_NAME_DEF_H_@@*/

namespace /*@@_NAMESPACE_NAME_@@*/{

enum
{
    /*@@_USER_STATE_ENUM_@@*/
};

typedef struct _Machine
{
    int state;
    void *user_data;
    char _inner_ml[0];
} Machine, *pMachine;

enum
{
    /*@@_USER_EVENT_ENUM_@@*/
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

/*@@_USER_ACTIONS_DEF_@@*/

//0 for deny 1 for ok
/*@@_USER_EVENTS_DEF_@@*/

}
#endif //_ML_DEF_H_