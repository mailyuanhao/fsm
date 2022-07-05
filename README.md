# fsm
通过ragel生成状态机的代码，通过每次状态跳转的action实现action和guard
根据json描述的状态机，生成对应的ragel文件，然后由ragel编译为c文件。
