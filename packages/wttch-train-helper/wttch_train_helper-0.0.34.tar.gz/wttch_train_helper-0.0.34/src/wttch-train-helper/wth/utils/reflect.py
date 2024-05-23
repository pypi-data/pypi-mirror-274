from typing import Any

import importlib


class ReflectUtil:

    @staticmethod
    def try_init_class(params: dict) -> Any:
        """
        尝试通过给定的模块位置, 类名, 初始化构造参数来生成对象。

        例如:
        {
            'module': 'wth.utils.reflect',
            'class': 'ReflectUtil',
            'init-kwargs': {}
        }

        `module` 指定要获取的模块位置,
        `class` 要获取的类名字
        `init-kwargs` 初始化构造参数, 该参数一定要和 指定的类的构造函数参数一致, 否则会初始化失败.
        """
        module_name = params['module']
        class_name = params['class']
        init_args = params['init-kwargs'] if 'init-kwargs' in params else {}

        module = importlib.import_module(module_name)
        class_ = getattr(module, class_name)
        return class_(**init_args)
