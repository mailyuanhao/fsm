import json
import random
from typing import Set


def mk_fsm(m: str, s: Set[str], e: Set[str]):
    x = [(i, j, k) for i in s for j in e for k in s if i != k]
    d = {"machine": m, "init_state": random.choice(list(s))}
    ts = []
    for t in x:
        tr = {"start": t[0],  "event": t[1], "target": t[2],
              "action": random.choice([True, False]),
              "guard": random.choice([True, False])
              }
        ts.append(tr)
    d["transition_table"] = ts

    return json.dumps(d)


if __name__ == "__main__":
    s = set({"a", "b", "c"})
    e = set({"x", "y", "z"})

    print(mk_fsm("t", s, e))
