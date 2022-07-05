import argparse
from tabnanny import check
import fsm
from fsm2cl import Machine2CL
from pathlib import Path

SRC_DEF = "source json file"
DEST_DEF = "dest folder"

def parse_args():
    parse = argparse.ArgumentParser(description="make rangel file automatically")
    parse.add_argument(SRC_DEF, type = Path, nargs = 1, help = "the json file used to define your fsm")
    parse.add_argument(DEST_DEF, nargs=1, type = Path, help = "the folder where to store the output files")
    return parse.parse_args()

def check_args(args :dict):
    src = dict[SRC_DEF][0]
    dest = dict[DEST_DEF][0]

    if not src.exists() or not dest.exists:
        raise Exception("src or dest not exists")
    
    return src, dest

if __name__ == '__main__':
    args = parse_args()
    src, dest = check_args(args.__dict__)

    with open(src) as fp:
        machine = fsm.FsmLoaderFromJson().load(fp)
        mc = Machine2CL(machine)
        header_file_name = "{}.h".format(machine.name.lower())
        dest_header_path = dest / (header_file_name)
        dest_src_path = dest / ("{}.rl".format(machine.name.lower()))
        with open(dest_header_path, r"w") as header, open(dest_src_path, r"w") as src:
            mc.show(machine.name.lower(), header, src)