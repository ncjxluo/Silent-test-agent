# -*- coding: utf-8 -*-
# @Time    : 2026/4/4 22:15
# @Author  : lwc
# @File    : agent.py
# @Description : 常驻服务（已修复任务重复执行问题）

from collections import deque
from src.utils.str_helper import get_local_ip, get_local_cpu, get_local_memory, get_local_io
import time
import threading
import httpx
import subprocess
import json
from src.utils.str_config import StrConfig

# ====================== 配置 ======================
str_config = StrConfig()
PLATFORM_API = f'http://{str_config.get_config().get("backend").get("host")}:{str_config.get_config().get("backend").get("port")}/api/v1'

FETCH_TASK_INTERVAL = 60
HEARTBEAT_INTERVAL = 10

AGENT_NAME = get_local_ip()
AGENT_ID = f"ncjx-{AGENT_NAME}"

MAX_JOBS = 5

# ====================== 全局状态 ======================
running_jobs = []        # [(process, task_id)]
task_queue = deque()
task_seen = set()        # 已接收任务（防重复）

running = True
lock = threading.Lock()  # 线程加锁避免多线程抢夺导致的重复

# ====================== 工具函数 ======================

def get_task_id(task: dict):
    """统一任务唯一标识"""
    return task.get('suite_key') or task.get('plan_key')


# ====================== 心跳 ======================

def heartbeat_thread():
    while running:
        try:
            with lock:
                running_task_ids = [task_id for _, task_id in running_jobs]

            print(f"[心跳] {AGENT_ID} 在线 | 运行中: {len(running_task_ids)}")

            httpx.post(
                f"{PLATFORM_API}/agent/agent_heart_beat",
                json={
                    "agent_key": AGENT_ID,
                    "agent_name": AGENT_NAME,
                    "status": 1,
                    "agent_running_tasks": json.dumps(running_task_ids, ensure_ascii=False),
                    "agent_max_tasks": str(MAX_JOBS),
                    "agent_cpu": get_local_cpu(),
                    "agent_memory": get_local_memory(),
                    "agent_io": get_local_io()
                }
            )
        except Exception as e:
            print(f"[心跳] 异常: {e}")

        time.sleep(HEARTBEAT_INTERVAL)


# ====================== 拉任务 ======================

def fetch_task_thread():
    while running:
        try:
            print("[查任务] 拉取平台任务...")

            res = httpx.get(f"{PLATFORM_API}/agent/get_task?agent_id={AGENT_ID}")
            print(f"[查任务] 平台返回: {res.status_code}")

            data = res.json()
            print(f"[查任务] 平台返回任务: {data}")
            tasks = data.get('data') or []

            if data.get('status') and tasks:
                for task in tasks:
                    task_id = get_task_id(task)
                    if not task_id:
                        continue
                    with lock:
                        if task_id in task_seen:
                            print(f"[跳过重复任务] {task_id}")
                            continue

                        print(f"[接收任务] {task_id}")
                        task_seen.add(task_id)

                    try_start_new_job(task)
            else:
                print("[查任务] 无任务")

        except Exception as e:
            print(f"[查任务] 异常: {e}")

        time.sleep(FETCH_TASK_INTERVAL)


# ====================== 启动任务 ======================

def try_start_new_job(task: dict):
    task_id = get_task_id(task)
    if not task_id:
        return

    with lock:
        # 清理已结束任务
        alive_jobs = []
        for p, tid in running_jobs:
            if p.poll() is None:
                alive_jobs.append((p, tid))
            else:
                print(f"[任务完成] PID={p.pid}, task_id={tid}")
                task_seen.discard(tid)

        running_jobs[:] = alive_jobs

        if len(running_jobs) < MAX_JOBS:
            print(f"[启动任务] {task.get('plan_name')} | {task_id}")

            try:
                # print()
                p = subprocess.Popen([
                    "python3", "interfaceMain.py",
                    "--task_key", str(task.get('suite_key', '')),
                    "--plan_key", str(task.get('plan_key', '')),
                    "--case_content", str(task.get('case_content', '')),
                    "--doc_content", str(task.get('doc_content', '')),
                ])

                running_jobs.append((p, task_id))

            except Exception as e:
                print(f"[启动失败] {task_id} -> {e}")
                task_seen.discard(task_id)
        else:
            print(f"[加入队列] {task_id}")
            task_queue.append(task)


# ====================== 队列调度 ======================

def monitor_queue():
    while running:
        try:
            with lock:
                # 清理已结束任务
                alive_jobs = []
                for p, tid in running_jobs:
                    if p.poll() is None:
                        alive_jobs.append((p, tid))
                    else:
                        print(f"[任务完成] PID={p.pid}, task_id={tid}")
                        task_seen.discard(tid)

                running_jobs[:] = alive_jobs

                # 启动队列任务
                while task_queue and len(running_jobs) < MAX_JOBS:
                    task = task_queue.popleft()
                    print(f"[队列调度] 启动 {get_task_id(task)}")

                    # ⚠️ 这里不要再加 task_seen（已经加过了）
                    try_start_new_job(task)

                print(f"[状态] 运行中: {len(running_jobs)} | 队列: {len(task_queue)} | 已接收: {len(task_seen)}")

        except Exception as e:
            print(f"[监控异常] {e}")

        time.sleep(2)


# ====================== 主入口 ======================

if __name__ == "__main__":
    print("=" * 60)
    print("          Agent 启动")
    print("=" * 60)

    thread_list = [
        threading.Thread(target=heartbeat_thread, daemon=True),
        threading.Thread(target=fetch_task_thread, daemon=True),
        threading.Thread(target=monitor_queue, daemon=True),
    ]

    for t in thread_list:
        t.start()
    try:
        for t in thread_list:
            t.join()
    except KeyboardInterrupt:
        print("\n收到 Ctrl+C，正在关闭...")
    finally:
        running = False
        print("Agent 已安全退出")