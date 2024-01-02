#!/usr/bin/env python3
import platform
import os
from pathlib import Path

link_name = "gitauto"
dir_name = "gitauto"


os_type = platform.system()




class ThePathWin:
    home_path = ""
    path_dir = Path(os.path.join(home_path, dir_name))
