
#line 1 "cd_machine.rl"
/*@@_INC_HEADER_@@*/
#include <cstdlib>
#include <cstring>
#include "cd_machine.h"

namespace cd_machine{

#line 8 "cd_machine.rl"

typedef struct __inner_ml
{
	 int cs;
	 const char* ts;
	 const char* te;
	 int act;
} inner_ml, *pinner_ml;


#line 22 "cd_machine.cpp"
static const char _CD_MACHINE_actions[] = {
	0, 1, 5, 1, 6, 1, 8, 1, 
	11, 1, 14, 1, 18, 1, 21, 2, 
	6, 7, 3, 9, 0, 10, 3, 9, 
	0, 13, 3, 9, 0, 17, 3, 9, 
	0, 20, 4, 9, 1, 12, 0, 4, 
	9, 2, 15, 0, 4, 9, 3, 16, 
	0, 4, 9, 4, 19, 0
};

static const char _CD_MACHINE_key_offsets[] = {
	0, 0, 0, 0, 0, 1, 1, 3, 
	3, 4
};

static const char _CD_MACHINE_trans_keys[] = {
	98, 98, 99, 97, 0
};

static const char _CD_MACHINE_single_lengths[] = {
	0, 0, 0, 0, 1, 0, 2, 0, 
	1, 0
};

static const char _CD_MACHINE_range_lengths[] = {
	0, 0, 0, 0, 0, 0, 0, 0, 
	0, 0
};

static const char _CD_MACHINE_index_offsets[] = {
	0, 0, 1, 2, 3, 5, 6, 9, 
	10, 12
};

static const char _CD_MACHINE_trans_targs[] = {
	1, 3, 3, 5, 5, 5, 7, 7, 
	7, 7, 9, 9, 9, 2, 4, 6, 
	8, 0
};

static const char _CD_MACHINE_trans_actions[] = {
	1, 18, 18, 34, 22, 22, 39, 44, 
	26, 26, 49, 30, 30, 7, 9, 11, 
	13, 0
};

static const char _CD_MACHINE_to_state_actions[] = {
	0, 3, 15, 0, 3, 0, 3, 0, 
	3, 0
};

static const char _CD_MACHINE_from_state_actions[] = {
	0, 0, 5, 0, 5, 0, 5, 0, 
	5, 0
};

static const char _CD_MACHINE_eof_trans[] = {
	0, 0, 0, 14, 0, 15, 0, 16, 
	0, 17
};

static const int CD_MACHINE_start = 1;
static const int CD_MACHINE_first_final = 1;
static const int CD_MACHINE_error = 0;

static const int CD_MACHINE_en_PalyInvalid = 2;
static const int CD_MACHINE_en_Opened = 4;
static const int CD_MACHINE_en_Closed = 6;
static const int CD_MACHINE_en_Playing = 8;
static const int CD_MACHINE_en_main = 1;


#line 18 "cd_machine.rl"

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
    event->user_data = 0;
    event->event = type;
    switch (type)
    {
        case CD_MACHINE_event_Stop: event->_event_str = "a"; break;
case CD_MACHINE_event_OpenClose: event->_event_str = "b"; break;
case CD_MACHINE_event_Play: event->_event_str = "c"; break;
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

    
#line 108 "cd_machine.rl"



#line 164 "cd_machine.cpp"
	{
	int _klen;
	unsigned int _trans;
	const char *_acts;
	unsigned int _nacts;
	const char *_keys;

	if ( p == pe )
		goto _test_eof;
	if (  pl->cs == 0 )
		goto _out;
_resume:
	_acts = _CD_MACHINE_actions + _CD_MACHINE_from_state_actions[ pl->cs];
	_nacts = (unsigned int) *_acts++;
	while ( _nacts-- > 0 ) {
		switch ( *_acts++ ) {
	case 8:
#line 1 "NONE"
	{ pl->ts = p;}
	break;
#line 185 "cd_machine.cpp"
		}
	}

	_keys = _CD_MACHINE_trans_keys + _CD_MACHINE_key_offsets[ pl->cs];
	_trans = _CD_MACHINE_index_offsets[ pl->cs];

	_klen = _CD_MACHINE_single_lengths[ pl->cs];
	if ( _klen > 0 ) {
		const char *_lower = _keys;
		const char *_mid;
		const char *_upper = _keys + _klen - 1;
		while (1) {
			if ( _upper < _lower )
				break;

			_mid = _lower + ((_upper-_lower) >> 1);
			if ( (*p) < *_mid )
				_upper = _mid - 1;
			else if ( (*p) > *_mid )
				_lower = _mid + 1;
			else {
				_trans += (unsigned int)(_mid - _keys);
				goto _match;
			}
		}
		_keys += _klen;
		_trans += _klen;
	}

	_klen = _CD_MACHINE_range_lengths[ pl->cs];
	if ( _klen > 0 ) {
		const char *_lower = _keys;
		const char *_mid;
		const char *_upper = _keys + (_klen<<1) - 2;
		while (1) {
			if ( _upper < _lower )
				break;

			_mid = _lower + (((_upper-_lower) >> 1) & ~1);
			if ( (*p) < _mid[0] )
				_upper = _mid - 2;
			else if ( (*p) > _mid[1] )
				_lower = _mid + 2;
			else {
				_trans += (unsigned int)((_mid - _keys)>>1);
				goto _match;
			}
		}
		_trans += _klen;
	}

_match:
_eof_trans:
	 pl->cs = _CD_MACHINE_trans_targs[_trans];

	if ( _CD_MACHINE_trans_actions[_trans] == 0 )
		goto _again;

	_acts = _CD_MACHINE_actions + _CD_MACHINE_trans_actions[_trans];
	_nacts = (unsigned int) *_acts++;
	while ( _nacts-- > 0 )
	{
		switch ( *_acts++ )
		{
	case 0:
#line 83 "cd_machine.rl"
	{ unexpected_event_action(pm, pbe); }
	break;
	case 1:
#line 89 "cd_machine.rl"
	{ if (1){ pm->state=CD_MACHINE_state_Closed;from_Opened_to_Closed_event_OpenClose_action(pm, pbe); { pl->cs = 6;goto _again;} } }
	break;
	case 2:
#line 94 "cd_machine.rl"
	{ if (from_Closed_to_Opened_event_OpenClose_guard(pm, pbe)){ pm->state=CD_MACHINE_state_Opened;from_Closed_to_Opened_event_OpenClose_action(pm, pbe); { pl->cs = 4;goto _again;} } }
	break;
	case 3:
#line 95 "cd_machine.rl"
	{ if (from_Closed_to_Playing_event_Play_guard(pm, pbe)){ pm->state=CD_MACHINE_state_Playing;from_Closed_to_Playing_event_Play_action(pm, pbe); { pl->cs = 8;goto _again;} }
if (from_Closed_to_PalyInvalid_event_Play_guard(pm, pbe)){ pm->state=CD_MACHINE_state_PalyInvalid;; { pl->cs = 2;goto _again;} } }
	break;
	case 4:
#line 102 "cd_machine.rl"
	{ if (from_Playing_to_Closed_event_Stop_guard(pm, pbe)){ pm->state=CD_MACHINE_state_Closed;; { pl->cs = 6;goto _again;} } }
	break;
	case 5:
#line 107 "cd_machine.rl"
	{{ pl->cs = 6;goto _again;}}
	break;
	case 9:
#line 1 "NONE"
	{ pl->te = p+1;}
	break;
	case 10:
#line 86 "cd_machine.rl"
	{ pl->act = 1;}
	break;
	case 11:
#line 1 "NONE"
	{	switch(  pl->act ) {
	case 0:
	{{ pl->cs = 0;goto _again;}}
	break;
	default:
	{{p = (( pl->te))-1;}}
	break;
	}
	}
	break;
	case 12:
#line 90 "cd_machine.rl"
	{ pl->act = 2;}
	break;
	case 13:
#line 91 "cd_machine.rl"
	{ pl->act = 3;}
	break;
	case 14:
#line 1 "NONE"
	{	switch(  pl->act ) {
	default:
	{{p = (( pl->te))-1;}}
	break;
	}
	}
	break;
	case 15:
#line 97 "cd_machine.rl"
	{ pl->act = 4;}
	break;
	case 16:
#line 98 "cd_machine.rl"
	{ pl->act = 5;}
	break;
	case 17:
#line 99 "cd_machine.rl"
	{ pl->act = 6;}
	break;
	case 18:
#line 1 "NONE"
	{	switch(  pl->act ) {
	default:
	{{p = (( pl->te))-1;}}
	break;
	}
	}
	break;
	case 19:
#line 103 "cd_machine.rl"
	{ pl->act = 7;}
	break;
	case 20:
#line 104 "cd_machine.rl"
	{ pl->act = 8;}
	break;
	case 21:
#line 1 "NONE"
	{	switch(  pl->act ) {
	default:
	{{p = (( pl->te))-1;}}
	break;
	}
	}
	break;
#line 350 "cd_machine.cpp"
		}
	}

_again:
	_acts = _CD_MACHINE_actions + _CD_MACHINE_to_state_actions[ pl->cs];
	_nacts = (unsigned int) *_acts++;
	while ( _nacts-- > 0 ) {
		switch ( *_acts++ ) {
	case 6:
#line 1 "NONE"
	{ pl->ts = 0;}
	break;
	case 7:
#line 1 "NONE"
	{ pl->act = 0;}
	break;
#line 367 "cd_machine.cpp"
		}
	}

	if (  pl->cs == 0 )
		goto _out;
	if ( ++p != pe )
		goto _resume;
	_test_eof: {}
	if ( p == eof )
	{
	if ( _CD_MACHINE_eof_trans[ pl->cs] > 0 ) {
		_trans = _CD_MACHINE_eof_trans[ pl->cs] - 1;
		goto _eof_trans;
	}
	}

	_out: {}
	}

#line 111 "cd_machine.rl"
}

void init_machine(pMachine machine)
{
    machine->state = CD_MACHINE_state_Closed; /*entry state*/

    pinner_ml pl = (pinner_ml)(machine->_inner_ml);
    
    
#line 397 "cd_machine.cpp"
	{
	 pl->cs = CD_MACHINE_start;
	 pl->ts = 0;
	 pl->te = 0;
	 pl->act = 0;
	}

#line 120 "cd_machine.rl"

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