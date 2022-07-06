#include <cstdlib>
#include <cstring>
#include <stdio.h>
#include "cd_machine.h"

namespace cd_machine
{

	// implement your atcions and guards
	void from_Closed_to_Opened_event_OpenClose_action(pMachine p, pBaseEvent)
	{
		printf("from_Closed_to_Opened_event_OpenClose_action\n");
		printf("machine: %d\n", p->state);
	}

	void from_Opened_to_Closed_event_OpenClose_action(pMachine p, pBaseEvent)
	{
		printf("from_Opened_to_Closed_event_OpenClose_action\n");
		printf("machine: %d\n", p->state);
	}

	void from_Closed_to_Playing_event_Play_action(pMachine p, pBaseEvent)
	{
		printf("from_Closed_to_Playing_event_Play_action\n");
		printf("machine: %d\n", p->state);
	}

	// 0 for deny 1 for ok
	int from_Closed_to_Opened_event_OpenClose_guard(pMachine p, pBaseEvent)
	{
		printf("from_Closed_to_Opened_event_OpenClose_guard\n");
		return 1;
	}

	int from_Closed_to_Playing_event_Play_guard(pMachine p, pBaseEvent)
	{
		printf("from_Closed_to_Playing_event_Play_guard\n");
		return 1;
	}

	int from_Closed_to_PalyInvalid_event_Play_guard(pMachine p, pBaseEvent)
	{
		printf("from_Closed_to_PalyInvalid_event_Play_guard\n");
		return 1;
	}

	int from_Playing_to_Closed_event_Stop_guard(pMachine p, pBaseEvent)
	{
		printf("from_Playing_to_Closed_event_Stop_guard\n");
		return 1;
	}

	void unexpected_event_action(pMachine p, pBaseEvent e)
	{
		printf("unexpected_event_action %d %s\n", p->state, e->_event_str);
	}
}

using namespace cd_machine;
int main(int argc, char **argv)
{
	pMachine m = new_machine();
	m->user_data = nullptr;

	pBaseEvent p = new_event(CD_MACHINE_event_OpenClose);
	process(m, p);
	delete_event(p);

	{
		pBaseEvent p2 = new_event(CD_MACHINE_event_Play);
		process(m, p2);
		delete_event(p2);
	}

	pBaseEvent p2 = new_event(CD_MACHINE_event_OpenClose);
	process(m, p2);
	delete_event(p2);

	{
		pBaseEvent p2 = new_event(CD_MACHINE_event_Play);
		process(m, p2);
		delete_event(p2);
	}

	delete_machine(m);
}