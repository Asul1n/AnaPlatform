from core.dif import Difference 
from .registry import NodeRegistry
from typing import Callable, Dict, Any, List
import logging


class NodeDispatcher:
    """ 
    自动根据节点类型调度对应的差分解析函数。
    支持 register 注册新类型。
    传入 Difference 类的对象
    """
    # 类级注册表（所有实例共享）
    global_handlers: Dict[str, Callable[[Any], str]] = {}
    
    def __init__(self, dif_parser, log_level=logging.INFO, log_file=None):
      self.dif_parser = dif_parser
      self.logger = self._setup_logger(log_level, log_file)
      
    # 日志配置
    def _setup_logger(self, log_level, log_file):
      logger = logging.getLogger("NodeDispatcher")
      logger.setLevel(log_level)

      if not logger.handlers:  # 避免重复添加 handler
          formatter = logging.Formatter(
              fmt="[%(asctime)s] [%(levelname)s] %(message)s",
              datefmt="%H:%M:%S"
          )
          console_handler = logging.StreamHandler()
          console_handler.setFormatter(formatter)
          logger.addHandler(console_handler)

          if log_file:
              file_handler = logging.FileHandler(log_file, encoding="utf-8")
              file_handler.setFormatter(formatter)
              logger.addHandler(file_handler)

      return logger
      
    # 注册新的节点处理函数
    @classmethod
    def register(cls, node_type: str):
      # 注册节点类型（全局共享）
      def decorator(func: Callable):
        cls.global_handlers[node_type] = func
        return func
      return decorator
    
    # 调度单个节点
    def dispatch(self, node):
      handler = self.global_handlers.get(node.type)
      if not handler:
        self.logger.warning(f"未处理的节点类型: {node.type}")
        return None
      
      try:
          constraint = handler(self.dif_parser, node)
          self.logger.info(f"[{node.type}] {node.id} => {constraint}")
          return constraint
      except Exception as e:
          self.logger.error(f"节点 {node.id} ({node.type}) 处理失败: {e}", exc_info=True)
          return None

    
    # 批量运行节点
    def run(self, registry):
        nodes = list(registry)
        self.logger.info(f"开始执行节点调度，共 {len(registry)} 个节点")
        constraints = []
        
        for node in nodes:
            result = self.dispatch(node)
            if result is not None:
                constraints.append(result)
        self.logger.info("节点调度完成")
        return constraints
        
    
    