import time
from datetime import datetime
import atexit
import json
import os
from arknights_mower.solvers.base_simu import SimulatorSolver
from arknights_mower.utils.infrast_sim import Simulator
from arknights_mower.utils.log import logger, init_fhlr
from arknights_mower.utils import config
from arknights_mower.utils.plan import Plan, PlanConfig, Room
from arknights_mower.utils.logic_expression import LogicExpression
# 下面不能删除
from arknights_mower.utils.operators import Operators, Operator, Dormitory
from arknights_mower.utils.scheduler_task import SchedulerTask,TaskTypes

maa_config = {
    "maa_enable": False,
}
recruit_config = {
    "recruit_enable":False,
}

# Free (宿舍填充)干员安排黑名单
free_blacklist = ["艾丽妮", "但书", "龙舌兰"]

# 干员宿舍回复阈值
    # 高效组心情低于 UpperLimit  * 阈值 (向下取整)的时候才会会安排休息
    # UpperLimit：默认24，特殊技能干员如夕，令可能会有所不同(设置在 agent-base.json 文件可以自行更改)
resting_threshold = 0.5

# 跑单如果all in 贸易站则 不需要修改设置
# 如果需要无人机加速其他房间则可以修改成房间名字如 'room_1_1'
drone_room = 'room_1_2'
# 无人机执行间隔时间 （小时）
drone_execution_gap = 4

reload_room = []

# 基地数据json文件保存名
state_file_name = 'state.json'

# 邮件时差调整
timezone_offset = 0

# 全自动基建排班计划：
# 这里定义了一套全自动基建的排班计划 plan_1
# agent 为常驻高效组的干员名

# group 为干员编队，你希望任何编队的人一起上下班则给他们编一样的名字
# replacement 为替换组干员备选
# 暖机干员的自动换班
# 目前只支持一个暖机干员休息
# ！！ 会吧其他正在休息的暖机干员赶出宿舍
# 请尽量安排多的替换干员，且尽量不同干员的替换人员不冲突
# 龙舌兰和但书默认为插拔干员 必须放在 replacement的第一位
# 请把你所安排的替换组 写入replacement 否则程序可能报错
# 替换组会按照从左到右的优先级选择可以编排的干员
# 宿舍常驻干员不会被替换所以不需要设置替换组
# 宿舍空余位置请编写为Free，请至少安排一个群补和一个单补 以达到最大恢复效率
# 宿管必须安排靠左，后面为填充干员
# 宿舍恢复速率务必1-4从高到低排列
# 如果有菲亚梅塔则需要安排replacement 建议干员至少为三
# 菲亚梅塔会从replacment里找最低心情的进行充能

agent_base_config = PlanConfig("稀音,黑键,承曦格雷伊,焰尾,伊内丝", "稀音,柏喙,伊内丝", "伺夜,帕拉斯,雷蛇,澄闪,红云,乌有,年,远牙,阿米娅,桑葚,截云",ling_xi=2, free_blacklist="艾丽妮,但书,龙舌兰")

plan_config = {"room_1_1": [Room("绮良", "", []),
                            Room("黑键", "黑键", ["龙舌兰", "伺夜"]),
                            Room("巫恋", "黑键", ["但书", "空弦"])],
               "room_2_1": [Room("砾", "砾", ["夜烟"]),
                            Room("斑点", "斑点", ["夜烟"]),
                            Room("苍苔", "", [])],
               "room_3_1": [Room("至简", "", ["夜烟", "梅尔"]),
                            Room("淬羽赫默", "多萝西", ["泡泡"]),
                            Room("多萝西", "多萝西", ["火神"])],
               "room_3_2": [Room("乌有", "乌有", ["空弦"]),
                            Room("图耶", "", ["但书"]),
                            Room("鸿雪", "", ["龙舌兰", "能天使"])],
               "room_3_3": [Room("雷蛇", "澄闪", ["炎狱炎熔", "格雷伊"])],
               "room_1_2": [Room("槐琥", "", ["梅尔"]),
                            Room("迷迭香", "黑键", ["梅尔", "夜烟"]),
                            Room("截云", "乌有", ["梅尔", "夜烟"])],
               "room_1_3": [Room("承曦格雷伊", "自动化", ["炎狱炎熔", "格雷伊"])],
               "room_2_2": [Room("温蒂", "自动化", ["泡泡"]),
                            Room("森蚺", "自动化", ["火神"]),
                            Room("清流", "自动化", ["贝娜"])],
               "room_2_3": [Room("澄闪", "澄闪", ["炎狱炎熔", "格雷伊"])],
               "central": [Room("阿米娅", "", ["诗怀雅"]),
                           Room("琴柳", "乌有", ["清道夫", "杜宾", "玛恩纳", "临光"]),
                           Room("重岳", "乌有", ["杜宾"]),
                           Room("夕", "乌有", ["玛恩纳"]),
                           Room("令", "乌有", ["临光"])],
               "dormitory_1": [Room("流明", "", []),
                               Room("闪灵", "", []),
                               Room("Free", "", []),
                               Room("Free", "", []),
                               Room("Free", "", [])],
               "dormitory_2": [Room("杜林", "", []),
                               Room("断罪者", "", []),
                               Room("褐果", "", []),
                               Room("Free", "", []),
                               Room("Free", "", [])],
               "dormitory_3": [Room("斥罪", "", []),
                               Room("蜜莓", "", []),
                               Room("桃金娘", "", []),
                               Room("爱丽丝", "", []),
                               Room("Free", "", [])],
               "dormitory_4": [Room("纯烬艾雅法拉", "", []),
                               Room("车尔尼", "", []),
                               Room("菲亚梅塔", "", ["绮良", "鸿雪", "图耶", "苍苔", "至简"]),
                               Room("Free", "", []),
                               Room("Free", "", [])],
               "meeting": [Room("伊内丝", "", ["红"]),
                           Room("见行者", "", ["陈"])],
               "contact": [Room("桑葚", "乌有", ["絮雨"])],
               "factory": [Room("年", "乌有", ["九色鹿"])],
               }
backup_plan1_config = {"central": [Room("阿米娅", "", ["诗怀雅"]),
                                   Room("清道夫", "", ["诗怀雅"]),
                                   Room("杜宾", "", ["泡泡"]),
                                   Room("玛恩纳", "", ["火神"]),
                                   Room("森蚺", "", ["诗怀雅"])],
                       "room_2_2": [Room("温蒂", "", ["泡泡"]),
                                    Room("掠风", "", ["贝娜"]),
                                    Room("清流", "", ["火神"])],
                       "room_1_3": [Room("炎狱炎熔", "自动化", ["承曦格雷伊"])],
                       "room_2_3": [Room("澄闪", "", ["承曦格雷伊", ])],
                       "room_3_3": [Room("雷蛇", "", ["承曦格雷伊"])],
                       }

agent_base_config0 = PlanConfig("稀音,黑键,焰尾,伊内丝", "稀音,柏喙,伊内丝", "伺夜,帕拉斯,雷蛇,澄闪,红云,乌有,年,远牙,阿米娅,桑葚,截云,掠风", ling_xi=2)

plan = {
    # 阶段 1
    "default_plan": Plan(plan_config, agent_base_config),
    # "backup_plans": [Plan(backup_plan1_config, agent_base_config0,
    #                       trigger=LogicExpression("op_data.operators['令'].current_room.startswith('dorm')", "and",
    #                                               LogicExpression(
    #                                                   "op_data.operators['温蒂'].current_mood() - op_data.operators['承曦格雷伊'].current_mood()",
    #                                                   ">", "4")),
    #                       task={'dormitory_2': ['Current', 'Current', 'Current', 'Current', '承曦格雷伊']})]
    "backup_plans":[]
}

def debuglog():
    logger.handlers[0].setLevel('DEBUG')


def savelog():
    config.LOGFILE_PATH = './log1'
    init_fhlr()


def initialize(tasks, scheduler=None):
    if scheduler is None:
        base_scheduler = SimulatorSolver() # use SimulatorSolver instead of BaseSchedulerSolver
        base_scheduler.package_name = config.APPNAME
        base_scheduler.operators = {}
        base_scheduler.global_plan = plan
        base_scheduler.current_base = {}
        base_scheduler.resting = []
        base_scheduler.tasks = tasks
        base_scheduler.last_room = ''
        base_scheduler.MAA = None
        base_scheduler.send_message_config = {}
        base_scheduler.ADB_CONNECT = None
        base_scheduler.maa_config = maa_config
        base_scheduler.recruit_config = recruit_config
        base_scheduler.error = False
        base_scheduler.drone_count_limit = 102  # 无人机高于于该值时才使用
        base_scheduler.drone_room = drone_room
        base_scheduler.drone_execution_gap = drone_execution_gap
        base_scheduler.run_order_delay = 5  # 跑单提前10分钟运行
        base_scheduler.reload_room = reload_room
        return base_scheduler
    else:
        scheduler.handle_error(True)
        return scheduler


def save_state():
    with open(state_file_name, 'w') as f:
        if base_scheduler is not None and base_scheduler.op_data is not None:
            json.dump(vars(base_scheduler.op_data), f, default=str)


def load_state():
    try:
        if not os.path.exists(state_file_name):
            return None
        with open(state_file_name, 'r') as f:
            state = json.load(f)
        operators = {k: eval(v) for k, v in state['operators'].items()}
        for k, v in operators.items():
            if not v.time_stamp == 'None':
                v.time_stamp = datetime.strptime(v.time_stamp, '%Y-%m-%d %H:%M:%S.%f')
            else:
                v.time_stamp = None
        return operators
    except Exception:
        return None



def simulate():
    global ope_list, base_scheduler
    tasks = []
    success = False
    while not success:
        try:
            base_scheduler = initialize(tasks)
            success = True
        except Exception as E:
            raise E
    validation_msg = base_scheduler.initialize_operators()
    if validation_msg is not None:
        logger.error(validation_msg)
        return
    _loaded_operators = load_state()
    if _loaded_operators is not None:
        for k, v in _loaded_operators.items():
            if k in base_scheduler.op_data.operators and not base_scheduler.op_data.operators[k].room.startswith(
                    "dorm"):
                # 只复制心情数据
                base_scheduler.op_data.operators[k].mood = v.mood
                base_scheduler.op_data.operators[k].time_stamp = v.time_stamp
                base_scheduler.op_data.operators[k].depletion_rate = v.depletion_rate
                base_scheduler.op_data.operators[k].current_room = v.current_room
                base_scheduler.op_data.operators[k].current_index = v.current_index
    base_scheduler.op_data.first_init = False
    if len(base_scheduler.op_data.backup_plans) > 0:
        for idx, backplan in enumerate(base_scheduler.op_data.backup_plans):
            validation_msg = base_scheduler.op_data.swap_plan(idx,True)
            if validation_msg is not None:
                logger.error(f"替换排班验证错误：{validation_msg}")
                return
            base_scheduler.op_data.swap_plan(-1,True)
    while True:
        try:
            if len(base_scheduler.tasks) > 0:
                (base_scheduler.tasks.sort(key=lambda x: x.time, reverse=False))
                sleep_time = (base_scheduler.tasks[0].time - datetime.now()).total_seconds()
                logger.info('||'.join([str(t) for t in base_scheduler.tasks]))
                base_scheduler.sleep(sleep_time)
            base_scheduler.run()
        except Exception as E:
            logger.exception(f"程序出错--->{E}")


# debuglog()
atexit.register(save_state)
Simulator.load()
savelog()
simulate()
