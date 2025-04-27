import os
import shutil
import logging

logger = logging.getLogger("DDNetConfig")

class DDNetConfig:
    def __init__(self):
        # 检查DDNet配置文件是否存在
        self.config_dict = {}
        self.bind_dict = {}
        self.friend_list = []
        self.config_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "DDNet", "settings_ddnet.cfg")
        if not os.path.exists(self.config_path):
            # 用户可能使用的是Teewords客户端
            self.config_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Teeworlds", "settings_teeworlds.cfg")
            if not os.path.exists(self.config_path):
                self.config_path = None
        
        if self.config_path is not None:
            logger.info(f"配置文件路径：{self.config_path}")
            self.load_config()
        else:
            logger.error("配置文件路径为空")

    def backup_config(self):
        # 是否已经备份过
        if os.path.exists(self.config_path + ".mcpserver.bak"):
            logger.info("配置文件备份已存在")
            return
        if self.config_path is not None:
            shutil.copy(self.config_path, self.config_path + ".mcpserver.bak")
            logger.info("配置文件备份成功")
        else:
            logger.error("配置文件路径为空")

    def load_config(self):
        self.backup_config()

        with open(self.config_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('bind '):
                parts = line.split(' ', 2)
                if len(parts) >= 3:
                    key = parts[1]
                    action = parts[2]
                    self.bind_dict[key] = action
            elif line.startswith('add_friend '):
                self.friend_list.append(line)
            elif ' ' in line:
                key, value = line.split(' ', 1)
                self.config_dict[key] = value

    def save_config(self):
        if self.config_path is None:
            logger.error("配置文件路径为空")
            return
        lines = []
        # 添加普通配置
        for key, value in self.config_dict.items():
            lines.append(f"{key} {value}")
        
        lines.append("unbindall")
        
        # 添加按键绑定
        for key, action in self.bind_dict.items():
            lines.append(f"bind {key} {action}")
        
        # 添加好友列表
        for friend in self.friend_list:
            lines.append(friend)
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

    def get_friend_list(self):
        return self.friend_list

    def get_bind_dict(self):
        return self.bind_dict

    def get_config_dict(self):
        return self.config_dict

