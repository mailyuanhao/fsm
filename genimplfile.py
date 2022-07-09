import argparse
import re
from email import header
from pathlib import Path
from typing import List, Tuple

SRC_DEF = "source header file"
name_space_regex = re.compile(
    r"^[\t ]*namespace[\t ]+(\w+)[\t ]*\{.*$", re.DOTALL | re.UNICODE)
event_action_regex = re.compile(
    r"^[\t ]*void[\t ]+(\w*_event_\w*action)[\t ]+\(.+\);.*$", re.DOTALL | re.UNICODE)
event_guard_regex = re.compile(
    r"^[\t ]*int[\t ]+(\w*_event_\w*_guard)[\t ]+\(.+\);.*$", re.DOTALL | re.UNICODE)

action_template = '''void {func_name}(pMachine p, pBaseEvent)
{{
    throw std::logic_error("{func_name} not implemented");
}}
'''

guard_template = '''int {func_name}(pMachine p, pBaseEvent)
{{
    throw std::logic_error("{func_name} not implemented");
}}
'''

template_file = '''
/**
 * @file 自动生成的框架文件，用户可以在该文件中实现action函数和guard函数
 *
 * @copyright Copyright (c) 2022
 *
 */
# include <memory>
# include <stdexcept>
# include "{header_name}"

namespace {name_space}
{{
    {actions}

	// 0 for deny 1 for ok
    {guards}

	class MachineWrapper;
	/**
	 * @brief 事件封装类
	 *
	 */
	class Event
	{{
	public:
		friend class MachineWrapper;
		typedef std::shared_ptr<BaseEvent> EventPtr;
		explicit Event(int type, void *data)
		{{
			auto p = new_event(type);
			if (!p)
			{{
				throw std::runtime_error("event type invalid or not enough memory");
			}}
			reset_user_data(data);
			e_.reset(p, delete_event);
		}}

		// 请自行保障返回值的生命周期
		const void *get_user_data() const {{ return e_->user_data; }}
		void *get_user_data() {{ return e_->user_data; }}
		void *reset_user_data(void *data)
		{{
			void *t = e_->user_data;
			e_->user_data = data;
			return t;
		}}

	private:
		EventPtr e_;
	}};

	/**
	 * @brief 状态机封装类，请注意自行保障多线程安全
	 *
	 */
	class MachineWrapper
	{{
	public:
		typedef std::shared_ptr<Machine> MachinePtr;
		explicit MachineWrapper(void *data)
		{{
			auto p = new_machine();
			if (!p)
			{{
				throw std::runtime_error("not enough memory");
			}}
			reset_user_data(data);
			m_.reset(p, delete_machine);
		}}

		// 请自行保障返回值的生命周期
		const void *get_user_data() const {{ return m_->user_data; }}
		void *get_user_data() {{ return m_->user_data; }}
		void *reset_user_data(void *data)
		{{
			void *t = m_->user_data;
			m_->user_data = data;
			return t;
		}}

		void process_event(Event &event)
		{{
			process(m_.get(), event.e_.get());
		}}

	private:
		MachinePtr m_;
	}};
}}
'''


def parse_args():
    parse = argparse.ArgumentParser(description="用于辅助生成实现文件")
    parse.add_argument(SRC_DEF, type=Path, nargs=1, help="the header file")
    return parse.parse_args()


def check_args(args: dict) -> Path:
    src: Path = args[SRC_DEF][0]

    if not (src.exists() and src.is_file):
        raise Exception("src not valid")

    return src


def extract_frist_group(pattern: re.Pattern, target_str: str) -> str:
    try:
        matches = pattern.finditer(target_str)
        for _, match in enumerate(matches, start=1):
            for groupNum in range(0, len(match.groups())):
                return match.group(groupNum + 1)
        return str()
    except:
        return str()


def parse_header_file(fp) -> Tuple[str, List[str], List[str], List[str]]:
    '''Parse the header file and return a tuple contains:
    namespace, user actions callbacks, user guard callbacks'''
    fp.seek(0)
    events, actions, guards = list(), list(), list()
    namespace = str()
    for l in fp.readlines():
        s = l if type(l) is str else l.decode('utf-8')
        if len(s) == 0:
            continue
        if len(namespace) == 0:
            namespace = extract_frist_group(name_space_regex, s)

        t = extract_frist_group(event_action_regex, s)
        if len(t) != 0:
            actions.append(t)

        t = extract_frist_group(event_guard_regex, s)
        if len(t) != 0:
            guards.append(t)
    return namespace, events, actions, guards


def mk_src_content(header_file_name, namespace, actions, guards) -> str:

    action_functions = "\n".join(
        [action_template.format(func_name=i) for i in actions])
    guard_functions = "\n".join(
        [guard_template.format(func_name=i) for i in guards])

    return template_file.format(header_name=header_file_name,
                                name_space=namespace,
                                actions=action_functions,
                                guards=guard_functions)


def _main():
    header = check_args(parse_args().__dict__)
    dest = header.with_suffix(".cpp")
    if dest.exists():
        print("{src}文件已经存在，为了防止误操作，请手动删除后重新运行!!!\n".format(dest))
        raise Exception("dest exists")

    with open(header, r"r") as fsrc:
        namespace, _, actions, guards = parse_header_file(fsrc)

    content = mk_src_content(header.name, namespace, actions, guards)

    with open(dest, r"w") as fdest:
        fdest.write(content)


if __name__ == '__main__':
    _main()
