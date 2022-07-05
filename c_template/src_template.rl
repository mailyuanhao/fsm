/*@@_INC_HEADER_@@*/
#include <cstdlib>
#include <cstring>
#include "/*@@_HEADER_NAME_@@*/.h"

namespace /*@@_NAMESPACE_NAME_@@*/{
%% machine /*@@_MACHINE_NAME_@@*/;

typedef struct __inner_ml
{
	 int cs;
	 const char* ts;
	 const char* te;
	 int act;
} inner_ml, *pinner_ml;

%%write data;

#ifndef USE_USER_MEM_ALLOCATION
void *user_malloc(int size)
{
    return malloc(size);
}

void user_free(void * p)
{
    return free(p);
}
#endif

int init_event(int type, pBaseEvent event)
{
    int ret = 1;
    event->event = type;
    switch (type)
    {
        /*@@_INIT_EVENT_BODY_@@*/
    default:
        ret = 0;
        break;
    }
    return ret;
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

void process(pMachine pm, pBaseEvent pbe)
{
    const char* p = pbe->_event_str;
    const char* pe = p + strlen(pbe->_event_str);
    const char* eof = pe;

    pinner_ml pl = (pinner_ml)(pm->_inner_ml);

    %%{
        access pl->;
        /*@@_RLS_@@*/
    }%%

%% write exec;
}

void init_machine(pMachine machine)
{
    machine->state = /*@@_ENTRY_STAE_ENUM_@@*/; /*entry state*/

    pinner_ml pl = (pinner_ml)(machine->_inner_ml);
    
    %% write init;

    BaseEvent be;
    be._event_str="0";
    process(machine, &be);

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
}