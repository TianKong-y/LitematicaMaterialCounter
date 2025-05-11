# LitematicaMaterialCounter/game_data.py

SHULKER_BOX_IDS = {
    "minecraft:shulker_box", "minecraft:white_shulker_box", "minecraft:orange_shulker_box",
    "minecraft:magenta_shulker_box", "minecraft:light_blue_shulker_box", "minecraft:yellow_shulker_box",
    "minecraft:lime_shulker_box", "minecraft:pink_shulker_box", "minecraft:gray_shulker_box",
    "minecraft:light_gray_shulker_box", "minecraft:cyan_shulker_box", "minecraft:purple_shulker_box",
    "minecraft:blue_shulker_box", "minecraft:brown_shulker_box", "minecraft:green_shulker_box",
    "minecraft:red_shulker_box", "minecraft:black_shulker_box"
}

ITEM_FRAME_ITEM_TAG = "Item" # 物品展示框中物品的NBT标签名
CHEST_MINECART_ITEMS_TAG = "Items" #运输矿车中物品列表的NBT标签名

ITEM_BEARING_ENTITY_IDS = { # 包含物品作为NBT一部分的实体ID及其物品标签
    "minecraft:item_frame": ITEM_FRAME_ITEM_TAG,
    "minecraft:glow_item_frame": ITEM_FRAME_ITEM_TAG,
}

ENTITY_CONTAINER_IDS = { # 作为容器的实体ID及其物品列表标签
    "minecraft:chest_minecart": CHEST_MINECART_ITEMS_TAG,
    "minecraft:hopper_minecart": CHEST_MINECART_ITEMS_TAG,
}

AIR_BLOCK_IDS = {"minecraft:air", "minecraft:cave_air", "minecraft:void_air"} #空气方块ID集合

MAX_STACK_SIZES = { # 定义各种物品的最大堆叠数量
    "DEFAULT": 64, # 默认堆叠大小
    "minecraft:ender_pearl": 16,
    "minecraft:snowball": 16,
    "minecraft:egg": 16,
    "minecraft:sign": 16, # 木牌 (所有类型，因为它们都掉落为物品形式的木牌，除非特定木材的木牌有不同堆叠)
    "minecraft:hanging_sign": 16, # 悬挂式木牌 (假设类似普通木牌)
    "minecraft:written_book": 1, # 成书
    "minecraft:writable_book": 1, # 书与笔
    "minecraft:enchanted_book": 1, # 附魔书
    "minecraft:bucket": 16, # 空桶堆叠16
    "minecraft:lava_bucket": 1,
    "minecraft:water_bucket": 1,
    "minecraft:milk_bucket": 1,
    "minecraft:powder_snow_bucket": 1,
    "minecraft:axolotl_bucket": 1,
    "minecraft:cod_bucket": 1,
    "minecraft:pufferfish_bucket": 1,
    "minecraft:salmon_bucket": 1,
    "minecraft:tadpole_bucket": 1,
    "minecraft:tropical_fish_bucket": 1,
    "minecraft:minecart": 1, # 矿车
    "minecraft:chest_minecart": 1, # 运输矿车
    "minecraft:furnace_minecart": 1, # 动力矿车
    "minecraft:hopper_minecart": 1, # 漏斗矿车
    "minecraft:tnt_minecart": 1, # TNT矿车
    "minecraft:saddle": 1, # 鞍
    "minecraft:potion": 1, # 药水
    "minecraft:splash_potion": 1, # 喷溅药水
    "minecraft:lingering_potion": 1, # 滞留药水
    "minecraft:shield": 1, # 盾牌
    "minecraft:flint_and_steel": 1, # 打火石
    "minecraft:shears": 1, # 剪刀
    "minecraft:bow": 1, # 弓
    "minecraft:crossbow": 1, # 弩
    "minecraft:fishing_rod": 1, # 钓鱼竿
    "minecraft:trident": 1, # 三叉戟
    "minecraft:elytra": 1, # 鞘翅
    "minecraft:spyglass": 1, # 望远镜
    "minecraft:goat_horn": 1, # 山羊角
    "minecraft:recovery_compass": 1, # 回响指南针
    "minecraft:lodestone_compass": 1, # 磁石指针
    "minecraft:bundle": 1, # 收纳袋
    "minecraft:armor_stand": 1, # 盔甲架 (物品形式)
    "minecraft:turtle_helmet": 1, # 海龟壳
    "minecraft:horse_armor": 1, # (所有类型的马铠)
    "minecraft:iron_horse_armor": 1,
    "minecraft:golden_horse_armor": 1,
    "minecraft:diamond_horse_armor": 1,
    "minecraft:leather_horse_armor": 1,
    "minecraft:lead": 1, # 拴绳
    "minecraft:name_tag": 1, # 命名牌
    # 工具 (所有材质) - 1
    "minecraft:wooden_sword": 1, "minecraft:stone_sword": 1, "minecraft:iron_sword": 1, "minecraft:golden_sword": 1, "minecraft:diamond_sword": 1, "minecraft:netherite_sword": 1,
    "minecraft:wooden_pickaxe": 1, "minecraft:stone_pickaxe": 1, "minecraft:iron_pickaxe": 1, "minecraft:golden_pickaxe": 1, "minecraft:diamond_pickaxe": 1, "minecraft:netherite_pickaxe": 1,
    "minecraft:wooden_axe": 1, "minecraft:stone_axe": 1, "minecraft:iron_axe": 1, "minecraft:golden_axe": 1, "minecraft:diamond_axe": 1, "minecraft:netherite_axe": 1,
    "minecraft:wooden_shovel": 1, "minecraft:stone_shovel": 1, "minecraft:iron_shovel": 1, "minecraft:golden_shovel": 1, "minecraft:diamond_shovel": 1, "minecraft:netherite_shovel": 1,
    "minecraft:wooden_hoe": 1, "minecraft:stone_hoe": 1, "minecraft:iron_hoe": 1, "minecraft:golden_hoe": 1, "minecraft:diamond_hoe": 1, "minecraft:netherite_hoe": 1,
    # 盔甲 (所有材质) - 1
    "minecraft:leather_helmet": 1, "minecraft:chainmail_helmet": 1, "minecraft:iron_helmet": 1, "minecraft:golden_helmet": 1, "minecraft:diamond_helmet": 1, "minecraft:netherite_helmet": 1,
    "minecraft:leather_chestplate": 1, "minecraft:chainmail_chestplate": 1, "minecraft:iron_chestplate": 1, "minecraft:golden_chestplate": 1, "minecraft:diamond_chestplate": 1, "minecraft:netherite_chestplate": 1,
    "minecraft:leather_leggings": 1, "minecraft:chainmail_leggings": 1, "minecraft:iron_leggings": 1, "minecraft:golden_leggings": 1, "minecraft:diamond_leggings": 1, "minecraft:netherite_leggings": 1,
    "minecraft:leather_boots": 1, "minecraft:chainmail_boots": 1, "minecraft:iron_boots": 1, "minecraft:golden_boots": 1, "minecraft:diamond_boots": 1, "minecraft:netherite_boots": 1,
    "minecraft:totem_of_undying": 1, # 图腾
    "minecraft:cake": 1, # 蛋糕 (作为物品时)
    # 床 (所有颜色，作为物品时) - 1
    "minecraft:white_bed": 1, "minecraft:orange_bed": 1, "minecraft:magenta_bed": 1, "minecraft:light_blue_bed": 1, "minecraft:yellow_bed": 1, "minecraft:lime_bed": 1, "minecraft:pink_bed": 1, "minecraft:gray_bed": 1, "minecraft:light_gray_bed": 1, "minecraft:cyan_bed": 1, "minecraft:purple_bed": 1, "minecraft:blue_bed": 1, "minecraft:brown_bed": 1, "minecraft:green_bed": 1, "minecraft:red_bed": 1, "minecraft:black_bed": 1,
    # 音乐唱片 (所有类型) - 1
    "minecraft:music_disc_13": 1, "minecraft:music_disc_cat": 1, "minecraft:music_disc_blocks": 1, "minecraft:music_disc_chirp": 1, "minecraft:music_disc_far": 1, "minecraft:music_disc_mall": 1, "minecraft:music_disc_mellohi": 1, "minecraft:music_disc_stal": 1, "minecraft:music_disc_strad": 1, "minecraft:music_disc_ward": 1, "minecraft:music_disc_11": 1, "minecraft:music_disc_wait": 1, "minecraft:music_disc_otherside": 1, "minecraft:music_disc_5": 1, "minecraft:music_disc_pigstep": 1, "minecraft:music_disc_relic": 1,
    # 旗帜图案 - 1
    "minecraft:flower_banner_pattern": 1, "minecraft:creeper_banner_pattern": 1, "minecraft:skull_banner_pattern": 1, "minecraft:mojang_banner_pattern": 1, "minecraft:globe_banner_pattern": 1, "minecraft:piglin_banner_pattern": 1,
    # 根据需要添加更多，特别是工具、盔甲、独特物品
} 