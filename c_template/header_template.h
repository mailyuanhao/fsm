#ifndef _ML_DEF_H_
#define _ML_DEF_H_

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

void *user_malloc(int size);
void user_free(void *);

/*@@_USER_ACTIONS_DEF_@@*/

//0 for deny 1 for ok
enum
{
    deny = 0,
    allowd,
};
/*@@_USER_EVENTS_DEF_@@*/

#endif //_ML_DEF_H_