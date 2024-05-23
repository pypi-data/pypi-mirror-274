from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent, FileSystemMovedEvent
import importlib
import atexit
import os
import yaml
from typing import Optional, Any, Dict, List
import threading
import logging
from types import ModuleType
from .py_static_cfg import Cfg


class ReloadCfgHandler(FileSystemEventHandler):
    def __init__(
        self,
        module: ModuleType,
        delay: float = 3, 
        logger: Optional[logging.Logger] = None,
    ):
        """重新加载模块

        Args:
            module (ModuleType): 重新加载的模块, Cfg 类所在的模块
            delay (float, optional): 防止频繁修改的延迟，可能导致修改后还要再保存一次来触发 on_modified, 单位秒
            logger (Optional[logging.Logger], optional): 日志记录器, 否则使用 print
        """
        self.module = module
        self.delay = delay
        self.logger = logger
        self._timers: Dict[str, threading.Timer] = {}
        self._yaml_handlers: Dict[str, ReloadYamlHandler] = {}
        self._observer = Observer()
        self._observer.schedule(self, path=os.path.dirname(module.__file__), recursive=False)
        self._observer.start()
        atexit.register(self._observer.stop)

    def reset_timer(self, path, opt):
        if path in self._timers:
            self._timers[path].cancel()  # 取消已存在的定时器
        self._timers[path] = threading.Timer(self.delay, self.process_event, [path, opt])
        self._timers[path].start()

    def process_event(self, path: str, opt: str):
        try:
            importlib.reload(self.module)
            if self.logger and opt:
                self.logger.info(f"Cfg {self.module.__name__} reloaded ({opt})")
            else:
                print(f"Cfg {self.module.__name__} reloaded ({opt})")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error reloading cfg ({opt}): {e}")
            else:
                print(f"Error reloading cfg ({opt}): {e}")
        finally:
            self._timers.pop(path, None)
        for handler in self._yaml_handlers.values():
            handler.load_all('')

    def on_modified(self, event: FileSystemEvent):
        if event.src_path == self.module.__file__:
            self.reset_timer(event.src_path, 'modified')
    
    def stop(self):
        self._observer.stop()
        for timer in self._timers.values():
            timer.cancel()
        self._timers.clear()
        for handler in self._yaml_handlers.values():
            handler.stop()
        self._yaml_handlers.clear()
    
    def add_yaml(
        self, *paths: str,
        delay: Optional[float] = None,
        logger: Optional[logging.Logger] = None,
        **kwargs,
    ) -> 'ReloadCfgHandler':
        """添加监听的yaml文件夹或文件路径

        Args:
            *paths (str): 监听的yaml文件夹或文件路径
                配置文件的文件名必须以 .yaml 结尾，不能以 . 开头
                yaml 的 key 必须符合变量名的命名规范, 不能是任意的字符串, 否则转成普通对象或报错
            delay (float, optional): 延迟处理时间, 单位秒
            logger (Optional[logging.Logger], optional): 日志记录器, 否则使用 print

        Returns:
            ReloadCfgHandler: 返回自身
        """
        for p in paths:
            p = os.path.normpath(p)
            if p in self._yaml_handlers:
                continue
            self._yaml_handlers[p] = ReloadYamlHandler(
                module=self.module,
                path=p,
                delay=delay or self.delay,
                logger=logger or self.logger,
                **kwargs,
            )
        return self
    
    def del_yaml(self, *paths: str) -> 'ReloadCfgHandler':
        """删除监听的yaml文件夹或文件路径

        Args:
            *paths (str): 监听的yaml文件夹或文件路径

        Returns:
            ReloadCfgHandler: 返回自身
        """
        for p in paths:
            p = os.path.normpath(p)
            handler = self._yaml_handlers.pop(p, None)
            if handler:
                handler.stop()
        self.process_event('self.module.__name__', 'del_yaml')
        return self
    
    @property
    def yaml_paths(self) -> List[str]:
        """返回监听的yaml文件夹或文件路径"""
        return list(self._yaml_handlers)


class ReloadYamlHandler(FileSystemEventHandler):
    def __init__(
        self,
        module: ModuleType,
        path: str,
        delay: float = 3, 
        logger: Optional[logging.Logger] = None,
        create_path: bool = True,
        limit_value_type: bool = True,
    ):
        """延迟处理文件变化事件，使用多线程实现延迟，不适合大量文件变化

        Args:
            module (ModuleType): 重新加载的模块, Cfg 类所在的模块
            path (str): 监听的yaml文件夹或文件路径
                配置文件的文件名必须以 .yaml 结尾，不能以 . 开头
                yaml 的 key 必须符合变量名的命名规范, 不能是任意的字符串, 否则转成普通对象或报错
            delay (float, optional): 延迟处理时间, 单位秒
            logger (Optional[logging.Logger], optional): 日志记录器, 否则使用 print
            create_path (bool, optional): 是否创建不存在的路径, 防止文件不存在报错
                后缀名为 .yaml 则创建文件，否则创建文件夹
            limit_value_type (bool, optional): 限制值的类型, 除 None 以外不允许 yaml 的 value 类型和配置类不同
        """
        if create_path and not os.path.exists(path):
            if path.endswith('.yaml'):
                if os.path.sep in path:
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write('')
            else:
                os.makedirs(path, exist_ok=True)
        self.module = module
        self.logger = logger
        self.path = path
        self.delay = delay
        self.limit_value_type = limit_value_type
        self._timers: Dict[str, threading.Timer] = {}  # 用字典存储文件和对应的定时器
        self.load_all()
        self._observer = Observer()
        self._observer.schedule(self, path=self.path, recursive=True)
        self._observer.start()
        atexit.register(self._observer.stop)

    def reset_timer(self, path, opt):
        if path in self._timers:
            self._timers[path].cancel()  # 取消已存在的定时器
        self._timers[path] = threading.Timer(self.delay, self.process_event, [path, opt])
        self._timers[path].start()
    
    @staticmethod
    def old_define(old: Any, new: Any) -> bool:
        if (  # 要求 old 和 new 都是 None 或者类型相同, 不然可能改变类型
            old is None or
            new is None or
            type(old) == type(new)
        ):
            return True
        raise TypeError(f"Cfg type mismatch: {type(old)} != {type(new)}, old={str(old)}, new={str(new)}")
    
    def load_all(self, opt: str = 'init'):
        if os.path.isdir(self.path):
            for root, dirs, files in os.walk(self.path):
                for file in files:
                    if not self.yaml_check(file):
                        continue
                    path = os.path.join(root, file)
                    self.process_event(path, opt)
        else:
            assert self.yaml_check(self.path), f"Path must be a yaml file, but got {self.path}"
            self.process_event(self.path, opt)

    def process_event(self, path: str, opt: str):
        try:
            with open(path, 'r',encoding='utf-8') as f:
                config = yaml.safe_load(f.read())
                assert isinstance(config, dict), f"Config must be a dict, but got {type(config)}"
            update_flag = False
            for k, v in config.items():
                if not hasattr(self.module, k):
                    continue
                vv = getattr(self.module, k)
                if hasattr(vv, '_set_'):
                    vv: Cfg
                    vv._set_(
                        key=None,
                        value=v,
                        cover_old=not self.limit_value_type,
                        old_define=self.old_define,
                    )
                setattr(self.module, k, vv)
                update_flag = True
            if update_flag and opt:
                if self.logger:
                    self.logger.info(f"Reloaded cfg yaml ({opt}) {path}")
                else:
                    print(f"Reloaded cfg yaml ({opt}) {path}")
        except BaseException as e:
            if self.logger:
                self.logger.error(f"ReloadYamlHandler error {opt} ({path}): {e}")
            else:
                print(f"ReloadYamlHandler error {opt} ({path}): {e}")
        finally:
            self._timers.pop(path, None)

    def on_modified(self, event: FileSystemEvent):
        if event.is_directory or not self.yaml_check(event.src_path):
            return
        self.reset_timer(event.src_path, 'modified')

    def on_created(self, event: FileSystemEvent):
        if event.is_directory or not self.yaml_check(event.src_path):
            return
        self.reset_timer(event.src_path, 'created')

    def on_moved(self, event: FileSystemMovedEvent):
        if event.is_directory or not self.yaml_check(event.dest_path):
            return
        self.reset_timer(event.dest_path, 'created')
    
    @staticmethod
    def yaml_check(path: str) -> bool:
        if not path.endswith('.yaml') or path[0] == '.':
            return False
        return True
    
    def stop(self):
        self._observer.stop()
        for timer in self._timers.values():
            timer.cancel()
        self._timers.clear()
