# server.py
from fastmcp import FastMCP
import logging
import signal
import sys

from ddnet_mcpserver.app import DDNetConfig
from ddnet_mcpserver.tools.ddnetprocess import get_process_status, stop_process

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("FastMCP-Server")

# 在现有日志配置下方添加
# 添加文件日志处理
file_handler = logging.FileHandler('ddnet_mcp_server.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# 初始化ddnetconfig获取配置文件
logger.info("初始化ddnetconfig获取配置文件")
ddnetconfig = DDNetConfig()
# 创建MCP服务器
mcp = FastMCP(
    name="ddnet_mcp_server",
    instructions="ddnet助手工具，提供以下功能（修改配置文件需要在关闭ddnet进程后进行）可以获取ddnet游戏状态，操作配置文件（修改配置文件增加或删除bind，关闭ddnet进程等），查询玩家分数（points）等游戏数据。"
)

# 获取ddnet游戏状态, 返回游戏状态
@mcp.tool()
def get_ddnet_game_status() -> str:
    """获取ddnet进程状态"""
    return get_process_status()
# 检查按键是否被占用
@mcp.tool()
def check_bind(bindkey: str) -> str:
    """检查按键是否被占用"""
    logger.info("检查按键是否被占用")
    return f"按键{bindkey}被占用！"
# 增加bind
@mcp.tool()
def add_bind(bindkey: str, bindvalue: str) -> str:
    """增加bind"""
    logger.info("增加bind")
    return f"按键{bindkey}已增加！"
# 删除bind
@mcp.tool()
def delete_bind(bindkey: str) -> str:
    """删除bind"""
    logger.info("删除bind")
    return f"按键{bindkey}已删除！"

@mcp.tool()
def get_friend_list() -> str:
    """获取好友列表"""
    logger.info("获取好友列表")
    return f"好友列表：{ddnetconfig.get_friend_list()}"

# 处理终止信号
def signal_handler(sig, frame):
    logger.info("接收到终止信号，正在关闭服务器...")
    # 这里可以添加任何需要的清理代码
    sys.exit(0)

# 注册信号处理程序
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    logger.info("服务器正在启动...")
    try:
        
        logger.info("服务器正在运行，按Ctrl+C可以停止服务器...")
        # 尝试明确指定transport参数
        mcp.run(transport="stdio")  # 使用标准输入/输出作为传输方式
    except Exception as e:
        logger.error(f"服务器出错: {e}")
        import traceback
        logger.error(traceback.format_exc())
    finally:
        logger.info("服务器已关闭")