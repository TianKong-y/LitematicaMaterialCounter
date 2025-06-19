# -*- coding: utf-8 -*-
import litemapy
from dataclasses import dataclass, field
from nbtlib.tag import Compound, List, String, Short, Int, Byte # 添加了导入
import math # 用于在潜影盒计算中使用 math.ceil
import csv # 为CSV写入添加
import argparse
import os
import sys # 为 sys.path 操作添加
import tkinter
import  tkinter.filedialog
# 将脚本所在目录添加到 sys.path 以允许直接导入本地模块
current_script_dir = os.path.dirname(os.path.abspath(__file__))
if current_script_dir not in sys.path:
    sys.path.insert(0, current_script_dir)
from minecraft_lang_loader import load_translations # 新的导入
from id_normalization import ID_NORMALIZATION_MAP # 新增：从新文件导入ID规范化映射
from game_data import (
    SHULKER_BOX_IDS, MAX_STACK_SIZES, ITEM_BEARING_ENTITY_IDS,
    ENTITY_CONTAINER_IDS, AIR_BLOCK_IDS, BLOCKS_TO_IGNORE,
    MULTI_ITEM_BLOCKS, SPECIAL_HANDLING_BLOCKS, ENTITIES_TO_IGNORE
) # 新增：从 game_data.py 导入所有需要的数据常量
import json # 为解析JSON文本组件添加
from collections import defaultdict
from typing import Any, Dict, List, NamedTuple, Optional, Tuple, Union
from enum import Enum, auto

# --- 类型枚举 ---
class ItemType(Enum):
    BLOCK = auto()
    ITEM = auto()
    ENTITY = auto()

# --- 常量 ---
MAX_RECURSION_DEPTH = 10 # 最大递归深度
VERSION = "1.1.1" # 版本号

# --- 翻译 ---
ITEM_ID_TO_CHINESE_NAME = load_translations()
if not ITEM_ID_TO_CHINESE_NAME:
    print("[WARNING] ITEM_ID_TO_CHINESE_NAME 为空。翻译可能无法正常工作。")
    ITEM_ID_TO_CHINESE_NAME = {} # 回退到空字典以防止 NameError，尽管翻译会丢失。

# --- HOTFIX: 手动修正错误的翻译键 ---
if 'block.minecraft.chicken' in ITEM_ID_TO_CHINESE_NAME:
    # 将错误的 "block" 键的值赋给正确的 "entity" 键
    ITEM_ID_TO_CHINESE_NAME['entity.minecraft.chicken'] = ITEM_ID_TO_CHINESE_NAME['block.minecraft.chicken']
    # 删除错误的键
    del ITEM_ID_TO_CHINESE_NAME['block.minecraft.chicken']
# --- END HOTFIX ---

# --- 数据类 ---
@dataclass
class ProcessedItem:
    item_id: str
    count: int
    item_type: ItemType # 新增：物品类型
    nbt_dict: dict = field(default_factory=dict)

def _parse_properties_from_string(state_string: str) -> dict[str, str]:
    """从litemapy的BlockState字符串表示中手动解析出属性字典。"""
    properties = {}
    if '[' in state_string and state_string.endswith(']'):
        props_part = state_string[state_string.find('[') + 1:-1]
        for prop in props_part.split(','):
            if '=' in prop:
                key, value = prop.split('=', 1)
                properties[key] = value
    return properties

# --- 函数 ---
def load_schematic(filepath: str) -> litemapy.Schematic:
    """加载 .litematic 文件并返回一个 Schematic 对象。"""
    try:
        schematic = litemapy.Schematic.load(filepath)
        return schematic
    except Exception as e:
        print(f"加载投影文件 {filepath} 时出错: {e}")
        raise

def extract_nbt_info(item_stack_nbt: Compound | None) -> dict:
    """从物品的NBT数据中提取简化信息（如自定义名称，附魔）。"""
    
    extracted = {} # 存储提取出的NBT信息
    
    components_tag = item_stack_nbt.get('components') # 现代版本 (1.20.2+) 的NBT存储在 components 中
    
    if components_tag and isinstance(components_tag, Compound):
        # 提取自定义名称 (minecraft:custom_name)
        custom_name_tag_str = components_tag.get('minecraft:custom_name')
        if custom_name_tag_str and isinstance(custom_name_tag_str, String):
            name_val = str(custom_name_tag_str)
            try:
                # 尝试解析JSON结构的名称 (例如由 tellraw 命令生成的名称)
                if name_val.startswith('{') and name_val.endswith('}') or name_val.startswith('[') and name_val.endswith(']'):
                    name_data = json.loads(name_val)
                    parsed_name = None
                    if isinstance(name_data, dict):
                        # 首先尝试顶层的 'text' 字段
                        if 'text' in name_data and name_data['text']:
                            parsed_name = str(name_data['text'])
                        # 如果顶层 'text' 为空或不存在, 检查 'extra' 字段
                        elif 'extra' in name_data and isinstance(name_data['extra'], list) and name_data['extra']:
                            first_extra = name_data['extra'][0]
                            if isinstance(first_extra, dict) and 'text' in first_extra and first_extra['text']:
                                parsed_name = str(first_extra['text'])
                    elif isinstance(name_data, list) and name_data and isinstance(name_data[0], dict) and 'text' in name_data[0] and name_data[0]['text']: # 处理 [{'text':...}] 结构
                         parsed_name = str(name_data[0]['text'])
                    
                    if parsed_name is not None:
                        extracted['name'] = parsed_name
                    else: # 如果未找到合适的文本，则回退到原始JSON字符串
                        extracted['name'] = name_val 
                elif name_val.startswith('"') and name_val.endswith('"') and len(name_val) > 1: # 处理简单带引号的字符串
                    extracted['name'] = name_val[1:-1]
                else: # 其他情况直接使用原始值
                    extracted['name'] = name_val 
            except json.JSONDecodeError:
                # 如果JSON解析失败，则使用原始字符串 (如果适用，先去除基本引号)
                if name_val.startswith('"') and name_val.endswith('"') and len(name_val) > 1:
                    extracted['name'] = name_val[1:-1]
                else:
                    extracted['name'] = name_val
            except Exception as e: # 其他解析名称时的异常
                 print(f"[WARN NBT_EXTRACT_NAME_COMPONENT] 处理 custom_name 组件时出错: {e}. 原始值: {name_val}")
                 extracted['name'] = name_val # 回退到原始值

        # 提取附魔信息 (minecraft:enchantments)
        enchantments_component = components_tag.get('minecraft:enchantments')
        if enchantments_component and isinstance(enchantments_component, Compound):
            levels_tag = enchantments_component.get('levels') # 附魔等级存储在 'levels' 子Compound中
            if levels_tag and isinstance(levels_tag, Compound):
                enchants = {}
                for ench_id_str, lvl_tag in levels_tag.items(): 
                    if isinstance(lvl_tag, (Int, Short, Byte)):
                        enchants[str(ench_id_str)] = int(lvl_tag)
                if enchants:
                    extracted['enchantments'] = tuple(sorted(enchants.items())) # 转换为可哈希的元组
        
    # 如果未能从 'components' 中提取名称，尝试旧版NBT路径 ('display.Name')
    if 'name' not in extracted: 
        display_tag = item_stack_nbt.get('display') # 旧版NBT的显示信息在 'display' 标签下
        if display_tag and isinstance(display_tag, Compound):
            name_tag = display_tag.get('Name') # 名称在 'Name' 标签下
            if name_tag and isinstance(name_tag, String):
                try:
                    # 旧版名称也可能是JSON字符串
                    name_val = str(name_tag.value)
                    if name_val.startswith('{') and name_val.endswith('}') or name_val.startswith('[') and name_val.endswith(']'):
                         name_data = json.loads(name_val)
                         if isinstance(name_data, dict) and 'text' in name_data: # 提取 'text' 字段
                             extracted['name'] = str(name_data['text'])
                         elif isinstance(name_data, list) and name_data and isinstance(name_data[0], dict) and 'text' in name_data[0]: # 处理 [{'text':...}]
                             extracted['name'] = str(name_data[0]['text'])
                         else: # 回退
                             extracted['name'] = name_val
                    else: # 非JSON的简单字符串
                        extracted['name'] = name_val
                except json.JSONDecodeError:
                    extracted['name'] = str(name_tag.value) # JSON解析失败则回退
                except Exception as e: # 其他访问 .value 属性的错误
                    extracted['name'] = str(name_tag) # 使用 str() 作为最终回退
    
    # 如果未能从 'components' 中提取附魔，尝试旧版NBT路径 ('Enchantments' 或 'StoredEnchantments' 列表)
    if 'enchantments' not in extracted: 
        # 附魔书通常使用 'StoredEnchantments'，其他物品使用 'Enchantments'
        # 我们将依次尝试两者
        ench_list_tag = item_stack_nbt.get('StoredEnchantments') # 首先尝试附魔书的标签
        if not ench_list_tag: # 如果不是附魔书，或者没有这个标签，尝试普通附魔标签
            ench_list_tag = item_stack_nbt.get('Enchantments') 

        if ench_list_tag and isinstance(ench_list_tag, List) and \
           hasattr(ench_list_tag, 'subtype') and ench_list_tag.subtype == Compound: # 列表元素应为Compound
            enchants = {}
            for enchant_compound in ench_list_tag: # 遍历每个附魔Compound
                if 'id' in enchant_compound and isinstance(enchant_compound['id'], String) and \
                   'lvl' in enchant_compound and isinstance(enchant_compound['lvl'], (Short, Int, Byte)):
                    enchants[str(enchant_compound['id'])] = int(enchant_compound['lvl'])
            if enchants:
                extracted['enchantments'] = tuple(sorted(enchants.items())) # 转换为可哈希元组

    # 提取药水效果
    potion_effect_value = None
    # 优先从 components (Minecraft 1.19.4+)
    if components_tag and isinstance(components_tag, Compound): # components_tag 已在前面定义和检查过
        potion_contents_tag = components_tag.get('minecraft:potion_contents')
        if potion_contents_tag and isinstance(potion_contents_tag, Compound):
            potion_val = potion_contents_tag.get('potion')
            if potion_val and isinstance(potion_val, String):
                potion_effect_value = str(potion_val)
            else: # 处理自定义效果或更复杂的结构
                # 为了区分，可以将整个 potion_contents 转换为可哈希的表示
                # (确保这个字符串转换是稳定和可哈希的，如果未来要用作聚合键的一部分)
                potion_effect_value = f"potion_contents:{str(potion_contents_tag)}"
    
    # 如果在 components 中未找到，则回退到旧版 NBT 结构
    if potion_effect_value is None:
        # 旧版顶层 'Potion' 标签
        old_potion_tag = item_stack_nbt.get('Potion')
        if old_potion_tag and isinstance(old_potion_tag, String):
            potion_effect_value = str(old_potion_tag)
        else:
            # 旧版 'tag' -> 'Potion' 或 'tag' -> 'CustomPotionEffects'
            # 注意：item_stack_nbt 已经可能是 'tag' 内部的结构，取决于它是如何被传递的。
            # 但为了安全，我们还是检查 item_stack_nbt.get('tag')
            tag_compound_for_potion = item_stack_nbt.get('tag') # 检查顶层是否有 'tag'
            if not tag_compound_for_potion or not isinstance(tag_compound_for_potion, Compound):
                tag_compound_for_potion = item_stack_nbt # 如果顶层没有 'tag'，则假定当前 item_stack_nbt 就是包含药水标签的层级

            old_tag_potion = tag_compound_for_potion.get('Potion')
            if old_tag_potion and isinstance(old_tag_potion, String):
                potion_effect_value = str(old_tag_potion)
            elif 'CustomPotionEffects' in tag_compound_for_potion and isinstance(tag_compound_for_potion['CustomPotionEffects'], List):
                    # 简化处理：将 CustomPotionEffects 列表转为字符串
                potion_effect_value = f"custom_effects:{str(tag_compound_for_potion['CustomPotionEffects'])}"

    if potion_effect_value is not None:
        extracted['potion_effect'] = potion_effect_value # 使用 'potion_effect' 作为键

    return extracted

def process_item_nbt(item_tag_compound: Compound, material_list: list[ProcessedItem], recursion_depth=0):
    """处理单个物品的NBT数据，提取信息并添加到材料列表。支持递归处理潜影盒。"""
    
    # --- 新增：预处理 item_tag_compound ---
    # 检查传入的NBT是否是包含 'slot' 和嵌套 'item' 的结构 (常见于容器内的物品列表)
    # 如果是，则真正的物品NBT在 'item' 子标签下
    actual_item_nbt = item_tag_compound
    if 'slot' in item_tag_compound and 'item' in item_tag_compound and \
       isinstance(item_tag_compound.get('item'), Compound): # Safely get 'item'
        actual_item_nbt = item_tag_compound['item']
    # --- 结束新增的预处理 ---

    if not actual_item_nbt or not isinstance(actual_item_nbt, Compound):
        return
    try:
        item_id_tag = actual_item_nbt.get('id')
        count_tag = actual_item_nbt.get('Count') 
        if count_tag is None: 
            count_tag = actual_item_nbt.get('count')

        if not (item_id_tag and isinstance(item_id_tag, String) and \
                count_tag and isinstance(count_tag, (Byte, Int))):
            return

        item_id_str_original = str(item_id_tag) 
        item_id_str = ID_NORMALIZATION_MAP.get(item_id_str_original, item_id_str_original) # 应用ID规范化
        count_int = int(count_tag)   
        simple_nbt_dict = extract_nbt_info(actual_item_nbt) 
        material_list.append(ProcessedItem(item_id=item_id_str, count=count_int, item_type=ItemType.ITEM, nbt_dict=simple_nbt_dict))
        # 潜影盒递归处理
        # 现代潜影盒NBT在 'components' -> 'minecraft:container' -> 物品列表
        # 旧版潜影盒NBT在 item_tag_compound -> 'BlockEntityTag' -> 'Items'
        # 当潜影盒作为物品存放在容器中时, 其BlockEntity数据可能包裹在顶层的 'tag' Compound下
        if item_id_str in SHULKER_BOX_IDS and recursion_depth < MAX_RECURSION_DEPTH:
            shulker_items_list = None 
            container_nbt_source = actual_item_nbt 
            potential_tag_compound = actual_item_nbt.get('tag')
            if potential_tag_compound and isinstance(potential_tag_compound, Compound):
                container_nbt_source = potential_tag_compound
            else:
                pass
            # 现在从确定的 container_nbt_source 查找实际的物品列表
            components_tag = container_nbt_source.get('components')
            if components_tag and isinstance(components_tag, Compound):
                container_component = components_tag.get('minecraft:container') 
                if container_component and isinstance(container_component, List) and \
                   hasattr(container_component, 'subtype') and container_component.subtype == Compound:
                    shulker_items_list = container_component
            if shulker_items_list is None: 
                block_entity_tag_old = container_nbt_source.get('BlockEntityTag') 
                if block_entity_tag_old and isinstance(block_entity_tag_old, Compound):
                    items_list_old = block_entity_tag_old.get('Items') 
                    if items_list_old and isinstance(items_list_old, List) and \
                       hasattr(items_list_old, 'subtype') and items_list_old.subtype == Compound:
                        shulker_items_list = items_list_old
            if shulker_items_list: 
                for idx, sub_item_nbt in enumerate(shulker_items_list): 
                            process_item_nbt(sub_item_nbt, material_list, recursion_depth + 1)
            else:
                pass
    except Exception as e:
        print(f"处理物品NBT时出错: {e} - 物品数据: {actual_item_nbt}")

def process_entity(entity_nbt: Compound, material_list: list[ProcessedItem], recursion_depth: int = 0):
    """
    递归处理单个实体及其乘客和内容物。
    """
    if recursion_depth > MAX_RECURSION_DEPTH:
        return

    entity_id_str_tag = entity_nbt.get('id')
    if not entity_id_str_tag or not isinstance(entity_id_str_tag, String):
        return
    entity_id_str = str(entity_id_str_tag)

    # a) 跳过黑名单中的实体
    if entity_id_str in ENTITIES_TO_IGNORE:
        return

    # b) 特殊处理悬浮物品实体 (minecraft:item)，只统计其内容物
    if entity_id_str == "minecraft:item":
        if 'Item' in entity_nbt and isinstance(entity_nbt.get('Item'), Compound):
            process_item_nbt(entity_nbt['Item'], material_list)
        return  # 处理完后返回，不统计 "item" 实体本身

    # c) 统计实体本身
    item_id_for_entity = entity_id_str
    if entity_id_str in {"minecraft:boat", "minecraft:chest_boat"}:
        boat_type_tag = entity_nbt.get('Type')
        if boat_type_tag and isinstance(boat_type_tag, String):
            boat_type = str(boat_type_tag)
            if boat_type == "bamboo":
                item_id_for_entity = f"minecraft:bamboo_{entity_id_str.split(':')[-1].replace('boat', 'raft')}"
            else:
                item_id_for_entity = f"minecraft:{boat_type}_{entity_id_str.split(':')[-1]}"
    material_list.append(ProcessedItem(item_id=item_id_for_entity, count=1, item_type=ItemType.ENTITY, nbt_dict={}))

    # d) 处理实体的内容物 (物品展示框、容器等)
    if entity_id_str in ITEM_BEARING_ENTITY_IDS:
        item_tag_key = ITEM_BEARING_ENTITY_IDS[entity_id_str]
        if item_tag_key in entity_nbt and isinstance(entity_nbt.get(item_tag_key), Compound):
            process_item_nbt(entity_nbt[item_tag_key], material_list)
    
    if entity_id_str in ENTITY_CONTAINER_IDS:
        items_tag_key = ENTITY_CONTAINER_IDS[entity_id_str]
        if items_tag_key in entity_nbt and isinstance(entity_nbt.get(items_tag_key), List):
            items_list = entity_nbt[items_tag_key]
            if hasattr(items_list, 'subtype') and items_list.subtype == Compound:
                for item_tag_compound in items_list:
                    process_item_nbt(item_tag_compound, material_list)

    # e) 核心修复：递归处理乘客实体
    if 'Passengers' in entity_nbt and isinstance(entity_nbt.get('Passengers'), List):
        passengers_list = entity_nbt['Passengers']
        if hasattr(passengers_list, 'subtype') and passengers_list.subtype == Compound:
            for passenger_nbt in passengers_list:
                process_entity(passenger_nbt, material_list, recursion_depth + 1)

def get_materials_from_schematic(schematic: litemapy.Schematic) -> list[ProcessedItem]:
    """从投影中提取所有材料，包括TileEntities和Entities中的材料。"""
    material_list: list[ProcessedItem] = []
    if not schematic or not hasattr(schematic, 'regions') or not schematic.regions:
        return material_list

    for region_name, region in schematic.regions.items():
        if not region: continue
        min_x, min_y, min_z = region.minx(), region.miny(), region.minz()
        max_x, max_y, max_z = region.maxx(), region.maxy(), region.maxz()

        # 1. 遍历区域中的所有方块状态 (重构后的逻辑 V3 - 独立IF块)
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                for z in range(min_z, max_z + 1):
                    try:
                        block_state = region[x, y, z]
                        bs_id = getattr(block_state, 'id', None)

                        # --- 路径 1: 忽略的方块 ---
                        if bs_id is None or bs_id in AIR_BLOCK_IDS or bs_id in BLOCKS_TO_IGNORE:
                            continue

                        # --- 最终修复：手动从字符串表示中解析属性 ---
                        properties = _parse_properties_from_string(str(block_state))
                        item_id_to_add = ID_NORMALIZATION_MAP.get(bs_id, bs_id)
                        
                        # --- 路径 2: 门 (独立处理) ---
                        if "door" in bs_id:
                            # 只统计下半部分
                            if properties.get(SPECIAL_HANDLING_BLOCKS["door"]["property"]) == SPECIAL_HANDLING_BLOCKS["door"]["value"]:
                                material_list.append(ProcessedItem(item_id=item_id_to_add, count=1, item_type=ItemType.BLOCK, nbt_dict={}))
                            continue # 无论如何都跳过，因为门已被处理 (要么计数，要么忽略上半部分)
                        
                        # --- 路径 3: 床 (独立处理) ---
                        if "bed" in bs_id:
                            # 只统计床脚部分
                            if properties.get(SPECIAL_HANDLING_BLOCKS["bed"]["property"]) == SPECIAL_HANDLING_BLOCKS["bed"]["value"]:
                                material_list.append(ProcessedItem(item_id=item_id_to_add, count=1, item_type=ItemType.BLOCK, nbt_dict={}))
                            continue # 无论如何都跳过
                        
                        # --- 路径 4: 雪 (独立处理) ---
                        if bs_id == "minecraft:snow":
                            layers = 1
                            try:
                                # 假设属性值是字符串 '1' 到 '8'
                                layers = int(properties.get(SPECIAL_HANDLING_BLOCKS["snow"]["property"], '1'))
                            except (ValueError, TypeError):
                                pass # 如果转换失败，则保持为1
                            
                            if layers >= 8:
                                material_list.append(ProcessedItem(item_id="minecraft:snow_block", count=1, item_type=ItemType.BLOCK, nbt_dict={}))
                            else:
                                material_list.append(ProcessedItem(item_id="minecraft:snow", count=layers, item_type=ItemType.BLOCK, nbt_dict={}))
                            continue # 跳过
                        
                        # --- 路径 5: 多物品方块 (蜡烛, 海泡菜) (独立处理) ---
                        if bs_id in MULTI_ITEM_BLOCKS:
                            count = 1
                            try:
                                prop_name = MULTI_ITEM_BLOCKS[bs_id]
                                # 假设属性值是字符串 '1' 到 '4'
                                count = int(properties.get(prop_name, '1'))
                            except (ValueError, TypeError):
                                pass # 转换失败则保持为1
                            material_list.append(ProcessedItem(item_id=item_id_to_add, count=count, item_type=ItemType.BLOCK, nbt_dict={}))
                            continue # 跳过

                        # --- 路径 6: 标准方块 ---
                        # (只有未被前面任何 continue 语句跳过的方块才会到达这里)
                        material_list.append(ProcessedItem(item_id=item_id_to_add, count=1, item_type=ItemType.BLOCK, nbt_dict={}))

                    except (IndexError, ValueError, TypeError) as e:
                        pass
        
        # 2. 处理区域中的TileEntities (逻辑不变)
        if hasattr(region, 'tile_entities') and region.tile_entities:
            for tile_entity in region.tile_entities:
                if not tile_entity or not hasattr(tile_entity, 'data') or not isinstance(getattr(tile_entity, 'data', None), Compound):
                    continue
                te_nbt: Compound = tile_entity.data
                if 'Items' in te_nbt and isinstance(te_nbt['Items'], List):
                    if hasattr(te_nbt['Items'], 'subtype') and te_nbt['Items'].subtype == Compound:
                        for item_tag_compound in te_nbt['Items']:
                            process_item_nbt(item_tag_compound, material_list)
                elif 'RecordItem' in te_nbt and isinstance(te_nbt['RecordItem'], Compound):
                    process_item_nbt(te_nbt['RecordItem'], material_list)

        # 3. 处理区域中的Entities (重构为调用新的递归函数)
        if hasattr(region, '_Region__entities'):
            for entity in region._Region__entities:
                if hasattr(entity, 'data') and isinstance(entity.data, Compound):
                    process_entity(entity.data, material_list)
                                
    return material_list

def aggregate_materials(processed_items: list[ProcessedItem]) -> tuple[dict[tuple[str, frozenset, ItemType], int], dict[tuple[str, frozenset, ItemType], dict]]:
    """聚合处理过的物品列表，统计具有相同ID、NBT和物品类型的物品数量。"""
    aggregated_counts: dict[tuple[str, frozenset, ItemType], int] = {}
    nbt_originals: dict[tuple[str, frozenset, ItemType], dict] = {}

    for item in processed_items:
        try:
            nbt_summary_key_items = frozenset(sorted(item.nbt_dict.items()))
        except TypeError as te:
            print(f"[ERROR AGGREGATE] 创建NBT的frozenset时发生TypeError: {item.nbt_dict}. 物品ID: {item.item_id}. 错误: {te}")
            nbt_summary_key_items = frozenset(("_problematic_nbt_", str(item.nbt_dict)))
        
        # 核心修复：将 item.item_type 添加到聚合键中
        key = (item.item_id, nbt_summary_key_items, item.item_type)
        
        aggregated_counts[key] = aggregated_counts.get(key, 0) + item.count
        
        if key not in nbt_originals:
            nbt_originals[key] = item.nbt_dict
            
    return aggregated_counts, nbt_originals

def format_nbt_for_display(item_id: str, nbt_dict: dict) -> str:
    """将提取的NBT信息格式化为人类可读的字符串，用于CSV输出。"""
    if not nbt_dict: # 如果NBT字典为空
        return "标准" # 返回"标准"
    parts = [] # 用于存储NBT信息的各个部分
    # 自定义名称
    if 'name' in nbt_dict:
        # 名称可能是现代Minecraft文本组件的JSON字符串。
        # 理想的解决方案是解析此JSON，但目前我们直接显示它。
        # 如果是简单文本，它看起来会很好。如果是JSON，它会可读但冗长。
        parts.append(f"名称: {nbt_dict['name']}")
    # 附魔
    # 期望附魔为元组的元组, 例如 (('minecraft:sharpness', 5), ('minecraft:unbreaking', 3))
    if 'enchantments' in nbt_dict and isinstance(nbt_dict['enchantments'], tuple) and nbt_dict['enchantments']:
        enchant_strings = []
        # nbt_dict['enchantments'] 如果来自 extract_nbt_info，则已经排序
        for ench_id, lvl in nbt_dict['enchantments']: 
            simple_ench_name = ench_id.split(':')[-1].replace('_', ' ').capitalize() # 简化附魔名称 (例如 "minecraft:sharpness" -> "Sharpness")
            # 将等级转换为罗马数字 (基础版)
            roman_lvl = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V'}.get(lvl, str(lvl))
            enchant_strings.append(f"{simple_ench_name} {roman_lvl}")
        if enchant_strings:
            parts.append(f"附魔: {', '.join(enchant_strings)}")
    # 药水 (示例结构 - 需要更多数据来获取药水名称/效果)
    # 这是一个占位符，实际的药水逻辑将涉及将药水ID映射到名称/效果。
    if 'potion_effect' in nbt_dict:
        potion_effect_val = nbt_dict['potion_effect']
        display_potion_name = potion_effect_val # 默认直接显示
        
        # 尝试从 'minecraft:potion_type' 格式的值中提取并翻译
        if isinstance(potion_effect_val, str) and potion_effect_val.startswith("minecraft:"):
            # 尝试获取翻译
            potion_key_id_part = potion_effect_val.split(':')[-1]
            # 常见的翻译键格式
            translation_keys_to_try = [
                f"item.minecraft.potion.effect.{potion_key_id_part}",
                f"potion.effect.{potion_effect_val.replace(':', '.')}",
                f"effect.minecraft.{potion_key_id_part}",
                potion_effect_val # 直接用ID作为键
            ]
            translated_name = None
            for t_key in translation_keys_to_try:
                translated_name = ITEM_ID_TO_CHINESE_NAME.get(t_key)
                if translated_name:
                    break
            
            if translated_name:
                display_potion_name = translated_name
            else: # 如果翻译不到，就用简化后的ID
                display_potion_name = potion_key_id_part.replace('_', ' ').capitalize()

        elif isinstance(potion_effect_val, str) and potion_effect_val.startswith("potion_contents:"):
            display_potion_name = f"内容: {potion_effect_val.split(':', 1)[1]}"
        elif isinstance(potion_effect_val, str) and potion_effect_val.startswith("custom_effects:"):
            display_potion_name = f"自定义: {potion_effect_val.split(':', 1)[1]}"
        
        parts.append(f"药水: {display_potion_name}")

    if 'custom_potion_effects' in nbt_dict: # 在 extract_nbt_info 示例中这被简化为 True
        parts.append("自定义效果") # 这是一个非常简化的表示
    # 在此添加更多NBT格式化，随着 extract_nbt_info 中提取新类型 (例如，头颅所有者，书本内容等)
    if not parts: # 如果NBT字典有键但没有一个被格式化
        return "标准" 
    return "; ".join(parts) # 用分号连接所有NBT信息部分

def format_quantity_detailed(quantity: int, item_id: str, item_type: ItemType) -> str:
    """将总数量格式化为"n盒 + n组 + n个"的字符串。"""
    if quantity == 0:
        return "0个"
    
    # 核心修复：如果物品是实体，则直接返回数量，不进行堆叠计算
    if item_type == ItemType.ENTITY:
        return f"{quantity}个"

    stack_size = MAX_STACK_SIZES.get(item_id, MAX_STACK_SIZES.get("DEFAULT", 64))
    if stack_size <= 0: # 不应发生，但作为安全措施
        stack_size = 1 

    # --- 新增：为不可堆叠物品提供特殊处理逻辑 ---
    if stack_size == 1:
        # 对于不可堆叠的物品，"组"的概念没有意义，直接计算盒和个
        shulker_capacity = 27  # 1个潜影盒能装27个不可堆叠物品
        num_boxes = quantity // shulker_capacity
        num_individual_items = quantity % shulker_capacity
        num_stacks = 0  # 不可堆叠物品没有"组"
    else:
        # --- 原有逻辑保持不变 ---
        shulker_capacity = 27 * stack_size
        num_boxes = quantity // shulker_capacity
        remainder_after_boxes = quantity % shulker_capacity
        num_stacks = remainder_after_boxes // stack_size
        num_individual_items = remainder_after_boxes % stack_size

    parts = []
    if num_boxes > 0:
        parts.append(f"{num_boxes}盒")
    if num_stacks > 0:
        parts.append(f"{num_stacks}组")
    if num_individual_items > 0:
        parts.append(f"{num_individual_items}个")

    if not parts:
        return "0个"
        
    return " + ".join(parts)

def get_item_display_name(item_id: str, item_type: ItemType) -> str:
    """根据物品ID和类型生成显示名称，优先使用中文名称。"""
    
    # 根据物品类型构建优先的翻译键列表
    base_id_part = item_id.split(':')[-1]
    keys_to_try = []
    
    if item_type == ItemType.ENTITY:
        keys_to_try.extend([
            f"entity.minecraft.{base_id_part}",
            f"item.minecraft.{base_id_part}",
            f"block.minecraft.{base_id_part}"
        ])
    elif item_type == ItemType.BLOCK:
        keys_to_try.extend([
            f"block.minecraft.{base_id_part}",
            f"item.minecraft.{base_id_part}",
            f"entity.minecraft.{base_id_part}"
        ])
    else: # ItemType.ITEM 或其他
        keys_to_try.extend([
            f"item.minecraft.{base_id_part}",
            f"block.minecraft.{base_id_part}",
            f"entity.minecraft.{base_id_part}"
        ])
    
    # 尝试所有可能的键
    for key in keys_to_try:
        if key in ITEM_ID_TO_CHINESE_NAME:
            retrieved_name = ITEM_ID_TO_CHINESE_NAME.get(key)
            if retrieved_name:
                return retrieved_name

    # 回退到处理英文ID的逻辑
    return item_id.split(':')[-1].replace('_', ' ').capitalize() # 将 "minecraft:some_item" 转为 "Some item"

def write_to_csv(aggregated_counts: dict[tuple[str, frozenset, ItemType], int], 
                 nbt_originals: dict[tuple[str, frozenset, ItemType], dict], 
                 output_filepath: str):
    """将聚合后的材料列表写入CSV文件。"""
    fieldnames = ["物品名称", "物品ID", "NBT信息", "数量 (个)", "数量 (盒-组-个)"] # CSV表头
    
    try:
        with open(output_filepath, 'w', newline='', encoding='utf-8-sig') as csvfile: # 使用 utf-8-sig 以支持Excel中的中文
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader() # 写入表头
            
            # 更新排序逻辑以使用新的键结构 (item[0] 是 (id, nbt, type))
            sorted_items = sorted(
                aggregated_counts.items(), 
                key=lambda item: (-item[1], get_item_display_name(item[0][0], item[0][2]), item[0][0])
            )
            
            # 更新循环以解包新的三元组键
            for (item_id_str, nbt_summary_key, item_type), quantity_count in sorted_items:
                original_nbt_dict = nbt_originals.get((item_id_str, nbt_summary_key, item_type), {})
                
                item_name_display = get_item_display_name(item_id_str, item_type)
                nbt_info_display = format_nbt_for_display(item_id_str, original_nbt_dict)
                quantity_detailed = format_quantity_detailed(quantity_count, item_id_str, item_type)
                writer.writerow({
                    "物品名称": item_name_display,
                    "物品ID": item_id_str,
                    "NBT信息": nbt_info_display,
                    "数量 (个)": quantity_count,
                    "数量 (盒-组-个)": quantity_detailed
                })
        print(f"成功将材料列表写入 {output_filepath}")
    except IOError as e:
        print(f"写入CSV文件 {output_filepath} 时发生IO错误: {e}")
    except Exception as e:
        print(f"写入CSV时发生意外错误: {e}")

def main():
    """主函数，用于选择文件输入输出并运行材料计数过程。"""
<<<<<< main
    output_filepath = None
    print("请在新窗口选择文件")
    input_filepath = tkinter.filedialog.askopenfilename(title='打开投影文件',
                                           filetypes=[('投影文件', '*.litematic'),('All files', '*')])
    output_filepath = tkinter.filedialog.asksaveasfilename(title='保存投影文件',
                                           defaultextension=".txt",
                                           filetypes=[('元数据格式文件', '*.csv')])
    print("已选择文件:" + input_filepath)
    if not os.path.exists(input_filepath): # 检查输入文件是否存在
        print(f"错误: 输入文件未找到: {input_filepath}")
        return
    if not input_filepath.lower().endswith('.litematic'): # 检查文件扩展名
        print(f"警告: 输入文件 '{input_filepath}' 没有 .litematic 扩展名。")
    if output_filepath is None: # 如果未指定输出路径，则根据输入文件名生成
        base, ext = os.path.splitext(input_filepath)
        output_filepath = f"{base}_materials.csv"
    print(f"正在处理投影: {input_filepath}")
    print(f"输出将保存至: {output_filepath}")
    try:
        schematic = load_schematic(input_filepath) # 加载投影
        if not schematic:
            print("加载投影失败。正在退出。")
            return
        print("投影加载完毕。正在提取材料...")
        processed_items = get_materials_from_schematic(schematic) # 提取材料
        if not processed_items: # 如果没有提取到物品
            print("未从投影中找到或提取到材料。")
        print(f"已提取 {len(processed_items)} 个原始物品条目。正在聚合...")
        aggregated_counts, nbt_originals = aggregate_materials(processed_items) # 聚合材料
        print(f"已聚合为 {len(aggregated_counts)} 种独特的材料类型。正在写入CSV...")
        write_to_csv(aggregated_counts, nbt_originals, output_filepath) # 写入CSV
    except Exception as e:
        print(f"在材料计数过程中发生错误: {e}")

if __name__ == "__main__":
    main()
