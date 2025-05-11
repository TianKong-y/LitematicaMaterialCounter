# LitematicaMaterialCounter/id_normalization.py
ID_NORMALIZATION_MAP = {
    # --- 现有条目 (从 material_counter.py 迁移) ---
    "minecraft:beetroots": "minecraft:beetroot", # 将甜菜植株方块统计为甜菜根物品
    "minecraft:wheats": "minecraft:wheat", # 小麦植株统计为小麦物品 (小麦植株本身不掉落小麦物品，而是掉落小麦种子和小麦，所以这个映射可能不总是期望的，除非目标是统计"潜在小麦")
    "minecraft:potatoes": "minecraft:potato", # 马铃薯植株统计为马铃薯物品
    "minecraft:carrots": "minecraft:carrot", # 胡萝卜植株统计为胡萝卜物品
    # 注意: 对于作物，通常方块ID (如 minecraft:potatoes) 代表植株本身，而物品ID (如 minecraft:potato) 代表收获物。
    # 除非明确希望将"植株"统计为"最终产物"，否则这些可能不需要。原始脚本中有这些，暂时保留并注释。

    # --- 旗帜 (方块ID -> 物品ID) ---
    "minecraft:white_wall_banner": "minecraft:white_banner",
    "minecraft:orange_wall_banner": "minecraft:orange_banner",
    "minecraft:magenta_wall_banner": "minecraft:magenta_banner",
    "minecraft:light_blue_wall_banner": "minecraft:light_blue_banner",
    "minecraft:yellow_wall_banner": "minecraft:yellow_banner",
    "minecraft:lime_wall_banner": "minecraft:lime_banner",
    "minecraft:pink_wall_banner": "minecraft:pink_banner",
    "minecraft:gray_wall_banner": "minecraft:gray_banner",
    "minecraft:light_gray_wall_banner": "minecraft:light_gray_banner",
    "minecraft:cyan_wall_banner": "minecraft:cyan_banner",
    "minecraft:purple_wall_banner": "minecraft:purple_banner",
    "minecraft:blue_wall_banner": "minecraft:blue_banner",
    "minecraft:brown_wall_banner": "minecraft:brown_banner",
    "minecraft:green_wall_banner": "minecraft:green_banner",
    "minecraft:red_wall_banner": "minecraft:red_banner",
    "minecraft:black_wall_banner": "minecraft:black_banner",

    # --- 告示牌 (方块ID -> 物品ID) ---
    # 这些通常是方块状态变体，但如果Litematica将它们作为不同ID报告，则需要映射
    "minecraft:oak_wall_sign": "minecraft:oak_sign",
    "minecraft:spruce_wall_sign": "minecraft:spruce_sign",
    "minecraft:birch_wall_sign": "minecraft:birch_sign",
    "minecraft:jungle_wall_sign": "minecraft:jungle_sign",
    "minecraft:acacia_wall_sign": "minecraft:acacia_sign",
    "minecraft:dark_oak_wall_sign": "minecraft:dark_oak_sign",
    "minecraft:mangrove_wall_sign": "minecraft:mangrove_sign",
    "minecraft:cherry_wall_sign": "minecraft:cherry_sign",
    "minecraft:bamboo_wall_sign": "minecraft:bamboo_sign",
    "minecraft:crimson_wall_sign": "minecraft:crimson_sign",
    "minecraft:warped_wall_sign": "minecraft:warped_sign",

    # --- 悬挂式告示牌 (方块ID -> 物品ID) ---
    "minecraft:oak_wall_hanging_sign": "minecraft:oak_hanging_sign",
    "minecraft:spruce_wall_hanging_sign": "minecraft:spruce_hanging_sign",
    "minecraft:birch_wall_hanging_sign": "minecraft:birch_hanging_sign",
    "minecraft:jungle_wall_hanging_sign": "minecraft:jungle_hanging_sign",
    "minecraft:acacia_wall_hanging_sign": "minecraft:acacia_hanging_sign",
    "minecraft:dark_oak_wall_hanging_sign": "minecraft:dark_oak_hanging_sign",
    "minecraft:mangrove_wall_hanging_sign": "minecraft:mangrove_hanging_sign",
    "minecraft:cherry_wall_hanging_sign": "minecraft:cherry_hanging_sign",
    "minecraft:bamboo_wall_hanging_sign": "minecraft:bamboo_hanging_sign",
    "minecraft:crimson_wall_hanging_sign": "minecraft:crimson_hanging_sign",
    "minecraft:warped_wall_hanging_sign": "minecraft:warped_hanging_sign",

    # --- 火把 (方块ID -> 物品ID) ---
    "minecraft:wall_torch": "minecraft:torch",
    "minecraft:soul_wall_torch": "minecraft:soul_torch",
    "minecraft:redstone_wall_torch": "minecraft:redstone_torch",

    # --- 头颅/骷髅头 (方块ID -> 物品ID) ---
    "minecraft:player_wall_head": "minecraft:player_head",
    "minecraft:zombie_wall_head": "minecraft:zombie_head",
    "minecraft:skeleton_wall_skull": "minecraft:skeleton_skull",
    "minecraft:wither_skeleton_wall_skull": "minecraft:wither_skeleton_skull",
    "minecraft:creeper_wall_head": "minecraft:creeper_head",
    "minecraft:dragon_wall_head": "minecraft:dragon_head", # 通常龙首物品ID是 dragon_head
    "minecraft:piglin_wall_head": "minecraft:piglin_head",

    # --- 珊瑚扇 (方块ID -> 物品ID) ---
    "minecraft:tube_coral_wall_fan": "minecraft:tube_coral_fan",
    "minecraft:brain_coral_wall_fan": "minecraft:brain_coral_fan",
    "minecraft:bubble_coral_wall_fan": "minecraft:bubble_coral_fan",
    "minecraft:fire_coral_wall_fan": "minecraft:fire_coral_fan",
    "minecraft:horn_coral_wall_fan": "minecraft:horn_coral_fan",
    "minecraft:dead_tube_coral_wall_fan": "minecraft:dead_tube_coral_fan",
    "minecraft:dead_brain_coral_wall_fan": "minecraft:dead_brain_coral_fan",
    "minecraft:dead_bubble_coral_wall_fan": "minecraft:dead_bubble_coral_fan",
    "minecraft:dead_fire_coral_wall_fan": "minecraft:dead_fire_coral_fan",
    "minecraft:dead_horn_coral_wall_fan": "minecraft:dead_horn_coral_fan",

    # --- 其他 ---
    "minecraft:cocoa": "minecraft:cocoa_beans", # 可可豆植株 (不同生长阶段的方块) -> 可可豆物品
    "minecraft:tripwire": "minecraft:string",   # 绊线方块 -> 线物品
    "minecraft:redstone_wire": "minecraft:redstone", # 红石线方块 -> 红石粉物品 (这个也看具体需求)
    "minecraft:powered_rail_on": "minecraft:powered_rail", # 激活的动力铁轨 -> 动力铁轨物品 (通常状态变化不改ID)
    "minecraft:detector_rail_on": "minecraft:detector_rail", # 激活的探测铁轨 -> 探测铁轨物品
    "minecraft:repeater_on": "minecraft:repeater", # 激活的中继器 -> 中继器物品
    "minecraft:comparator_on": "minecraft:comparator", # 激活的比较器 -> 比较器物品
    "minecraft:furnace_lit": "minecraft:furnace", # 点燃的熔炉 -> 熔炉物品
    # 许多 'lit' 或 'on' 状态的方块在被破坏时仍掉落其非激活状态的物品形式，
    # 这些映射仅在Litematica将它们报告为完全不同的ID时才需要。
} 