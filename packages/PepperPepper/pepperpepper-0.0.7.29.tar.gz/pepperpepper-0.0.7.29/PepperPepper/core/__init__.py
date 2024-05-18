"""
core 模块
功能：包含包的核心功能和基础类。
子模块/文件：
base_model.py：定义基础模型类，提供模型初始化、保存、加载等基础功能。
utils.py：包含一些通用的工具函数，如数据处理、模型评估等。
text.utils: 负责处理文本数据相关的功能，例如词表构建、词频统计等。
"""
# core/__init__.py

# 导入 core 子包中的关键模块
# from . import data_structures
# from . import utils
# from . import model_builder
#
# 如果需要，可以直接导入这些模块中的特定类或函数

from .utils import evaluate_accuracy_gpu
from .utils import train_custom
from .utils import try_gpu
from .utils import try_all_gpus

from .text_utils import tokenize
from .text_utils import Vocab
from .text_utils import seq_data_iter_random
from .text_utils import seq_data_iter_sequential
from .text_utils import SeqDataLoader

from .image_utils import visualize_grid_cells
from .image_utils import show_images
from .image_utils import show_boxes
from .image_utils import bbox_to_rect
from .image_utils import box_corner_to_center
from .image_utils import visualize_bounding_boxes
from .image_utils import box_iou_xyxy
from .image_utils import box_iou_xywh
from .image_utils import draw_anchor_boxes
from .image_utils import get_objectness_label
from .image_utils import nms
from .image_utils import multiclass_nms

from . import transforms




# from .data_structures import CustomDataStructure
# from .utils import some_utility_function
# from .model_builder import build_model
#
# __all__ 变量定义了当使用 from core import * 时导入哪些对象
# 注意：通常不推荐使用 from package import *
__all__ = [
    'evaluate_accuracy_gpu',
    'train_custom',
    'try_gpu',
    'try_all_gpus',

    'tokenize',
    'Vocab',
    'seq_data_iter_random',
    'seq_data_iter_sequential',
    'SeqDataLoader',

    'visualize_grid_cells',
    'show_images',
    'show_boxes',
    'bbox_to_rect',
    'box_corner_to_center',
    'visualize_bounding_boxes',
    'box_iou_xyxy',
    'box_iou_xywh',
    'draw_anchor_boxes',
    'get_objectness_label',
    'nms',
    'multiclass_nms',

    'transforms'
]