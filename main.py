import sys
import glob
import asyncio
import logging
import importlib.util
import urllib3
from pathlib import Path
from config import X1

# Constants
MODULES_PATH = "JARVIS/modules"
LOG_FORMAT = '[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s'
LOG_LEVEL = logging.WARNING

def configure_logging():
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)

def disable_insecure_warnings():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_plugin_module(plugin_name):
    path = Path(f"{MODULES_PATH}/{plugin_name}.py")
    spec = importlib.util.spec_from_file_location(f"{MODULES_PATH}.{plugin_name}", path)
    module = importlib.util.module_from_spec(spec)
    module.logger = logging.getLogger(plugin_name)
    spec.loader.exec_module(module)
    sys.modules[f"{MODULES_PATH}.{plugin_name}"] = module
    print(f"FRIDAY has Imported {plugin_name}")

def load_all_plugins():
    files = glob.glob(f"{MODULES_PATH}/*.py")
    for name in files:
        with open(name) as file:
            plugin_name = Path(file.name).stem
            load_plugin_module(plugin_name)

async def main():
    await X1.run_until_disconnected()

if __name__ == "__main__":
    configure_logging()
    disable_insecure_warnings()
    load_all_plugins()
    print("\nThe Bot Has Been Deployed Successfully. 👻\nMy Master ---> @JARVIS_V2")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
