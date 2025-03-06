import os
import sys
import io
import contextlib
import yaml
import importlib
from utils.cookie_cloud import fetch_cookie


def load_config(file_path):
    cur_path = os.path.abspath(os.path.dirname(__file__))
    abs_file_path = os.path.join(cur_path, file_path)
    with open(abs_file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


def save_config(file_path, config):
    cur_path = os.path.abspath(os.path.dirname(__file__))
    abs_file_path = os.path.join(cur_path, file_path)
    with open(abs_file_path, 'w', encoding='utf-8') as file:
        yaml.safe_dump(config, file)


"""
加载青龙推送服务
"""


def load_send():
    cur_path = os.path.abspath(os.path.dirname(__file__))
    if os.path.exists(cur_path + "/notify.py"):
        try:
            from notify import send
            return send
        except ImportError:
            return False
    else:
        return False


class TeeIO(io.TextIOBase):
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for s in self.streams:
            s.write(data)

    def flush(self):
        for s in self.streams:
            s.flush()


def main():
    config = load_config('config_task.yml')
    sites = config.get('sites', {})

    # 首次运行调用CookieCloud拉取站点Cookie
    if config.get("Global").get("FirstRun"):
        new_sites = fetch_cookie(sites)
        config['Global']['FirstRun'] = False
        config['sites'] = new_sites
        save_config('config_task.yml', config)
        print("Cookies synced and configuration updated.")

    # 筛选已启用站点
    enabled_sites = [{site_name: site_config} for site_name, site_config in sites.items() if site_config.get('enabled')]
    print(f"Enabled Sites Length: {len(enabled_sites)}")
    print("--------------------------------------------------")
    for site in enabled_sites:
        site_name, site_config = list(site.items())[0]
        try:
            print(f"Processing Site: {site_name}")
            cookie = site_config.get('cookie', '')
            if not cookie:
                print(f"Cookie not found for site: {site_name}")
                continue
            tasks = site_config.get('tasks', [])
            if not tasks:
                print(f"There are no task select in site: {site_name}")
                continue
            try:
                module = importlib.import_module(f'nexus.{site_name}')
                task_class = getattr(module, 'Tasks')
                task_instance = task_class(cookie)
            except (ModuleNotFoundError, AttributeError) as e:
                print(f"Error importing module or class for site: {site_name} - {e}")
                continue

            for task in tasks:
                if hasattr(task_instance, task):
                    print("------")
                    print(f"Task {task} started")
                    try:
                        print(getattr(task_instance, task)())
                    except Exception as e:
                        print(f"Error processing task: {task} - {e}")
                    finally:
                        print(f"Task {task} finished")
                        print("------")
                else:
                    print(f"Task {task} not found in {site_name} Tasks class")
                    continue
        except Exception as e:
            print(f"Error processing site: {site_name} - {e}")
        finally:
            print(f"Site {site_name} processed")
            print("--------------------------------------------------")


if __name__ == "__main__":
    buffer = io.StringIO()
    with contextlib.redirect_stdout(TeeIO(sys.stdout, buffer)):
        main()
    all_logs = buffer.getvalue()
    notify = load_send()
    if callable(notify):
        # 如果推送服务可用
        notify("PT_AUTO_TASK 日志", all_logs)
