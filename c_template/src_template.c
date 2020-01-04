/*@@_INC_HEADER_@@*/
#include "header_template.h"

/*@@_EVENT_STR_DEF_@@*/
const char *event_a = "a";

typedef struct __inner_ml
{
} inner_ml, *pinner_ml;

void init_machine(pMachine machine)
{
    machine->state = /*@@_ENTRY_SATE_ENUM_@@*/; /*entry state*/

    pinner_ml pl = (pinner_ml)(machine->_inner_ml);

    //%%ragle_init
}

int init_event(int type, pBaseEvent event)
{
    int ret = 1;
    event->event = type;
    switch (type)
    {
        /*@@_INIT_EVENT_BODY_@@*/
        /*
    case ev_a:
        event->_event_str = "a";
        break;
        */

    default:
        ret = 0;
        break;
    }
    return ret;
}

pMachine new_machine()
{
    pMachine p = (pMachine)user_malloc(sizeof(Machine) + sizeof(inner_ml));
    if (!p)
    {
        return 0;
    }

    init_machine(p);

    return p;
}
void delete_machine(pMachine p)
{
    user_free(p);
}

pBaseEvent new_event(int type)
{
    pBaseEvent pbe = (pBaseEvent)user_malloc(sizeof(BaseEvent));
    if (!pbe)
    {
        return pbe;
    }

    if (!init_event(type, pbe))
    {
        user_free(pbe);
        return 0;
    }

    return pbe;
}
void delete_event(pBaseEvent p)
{
    user_free(p);
}

void process(pMachine pm, pBaseEvent pe)
{
    //todo

    //%%{

    //%%

    //%% ragel exec
}