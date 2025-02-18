import yaml
import importlib


def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


def main():
    config = load_config('config_task.yml')
    sites = config.get('sites', {})
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
                TaskClass = getattr(module, 'Tasks')
                task_instance = TaskClass(cookie)
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
    main()
