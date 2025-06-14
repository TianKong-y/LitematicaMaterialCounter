# LitematicaMaterialCounter/game_data.py

# --- NBT 标签名常量 ---
ITEM_FRAME_ITEM_TAG = "Item"
CHEST_MINECART_ITEMS_TAG = "Items"

# --- 潜影盒ID ---
SHULKER_BOX_IDS = {
    "minecraft:shulker_box", "minecraft:white_shulker_box", "minecraft:orange_shulker_box",
    "minecraft:magenta_shulker_box", "minecraft:light_blue_shulker_box", "minecraft:yellow_shulker_box",
    "minecraft:lime_shulker_box", "minecraft:pink_shulker_box", "minecraft:gray_shulker_box",
    "minecraft:light_gray_shulker_box", "minecraft:cyan_shulker_box", "minecraft:purple_shulker_box",
    "minecraft:blue_shulker_box", "minecraft:brown_shulker_box", "minecraft:green_shulker_box",
    "minecraft:red_shulker_box", "minecraft:black_shulker_box"
}

# --- 方块处理常量 ---
AIR_BLOCK_IDS = {"minecraft:air", "minecraft:cave_air", "minecraft:void_air"}

BLOCKS_TO_IGNORE = {
    "minecraft:piston_head",
    "minecraft:moving_piston",
    "minecraft:bubble_column",
    "minecraft:water",
    "minecraft:lava",
    "minecraft:end_portal",
    "minecraft:nether_portal",
}

MULTI_ITEM_BLOCKS = {
    "minecraft:sea_pickle": "pickles",
    "minecraft:candle": "candles", "minecraft:white_candle": "candles", "minecraft:orange_candle": "candles",
    "minecraft:magenta_candle": "candles", "minecraft:light_blue_candle": "candles", "minecraft:yellow_candle": "candles",
    "minecraft:lime_candle": "candles", "minecraft:pink_candle": "candles", "minecraft:gray_candle": "candles",
    "minecraft:light_gray_candle": "candles", "minecraft:cyan_candle": "candles", "minecraft:purple_candle": "candles",
    "minecraft:blue_candle": "candles", "minecraft:brown_candle": "candles", "minecraft:green_candle": "candles",
    "minecraft:red_candle": "candles", "minecraft:black_candle": "candles",
}

SPECIAL_HANDLING_BLOCKS = {
    "door": {"property": "half", "value": "lower"},
    "bed": {"property": "part", "value": "foot"},
    "snow": {"property": "layers"}
}


# --- 实体处理常量 ---
# 这些是通用的实体类别ID。代码将通过检查实体的'Type' NBT标签来确定具体的物品ID。
COUNTABLE_ENTITIES = {
    "minecraft:minecart",
    "minecraft:chest_minecart",
    "minecraft:furnace_minecart",
    "minecraft:tnt_minecart",
    "minecraft:hopper_minecart",
    "minecraft:command_block_minecart",
    "minecraft:spawner_minecart",
    "minecraft:boat",
    "minecraft:chest_boat",
    "minecraft:armor_stand",
}

# 包含单个物品的实体 (如物品展示框)
ITEM_BEARING_ENTITY_IDS = {
    "minecraft:item_frame": ITEM_FRAME_ITEM_TAG,
    "minecraft:glow_item_frame": ITEM_FRAME_ITEM_TAG,
}

# 包含物品列表的实体 (容器)
ENTITY_CONTAINER_IDS = {
    "minecraft:chest_minecart": CHEST_MINECART_ITEMS_TAG,
    "minecraft:hopper_minecart": CHEST_MINECART_ITEMS_TAG,
    "minecraft:chest_boat": CHEST_MINECART_ITEMS_TAG,
}


# --- 物品堆叠大小 ---
MAX_STACK_SIZES = {
    "DEFAULT": 64,
    "minecraft:ender_pearl": 16, "minecraft:snowball": 16, "minecraft:egg": 16, "minecraft:sign": 16,
    "minecraft:hanging_sign": 16, "minecraft:bucket": 16,
    "minecraft:written_book": 1, "minecraft:writable_book": 1, "minecraft:enchanted_book": 1,
    "minecraft:lava_bucket": 1, "minecraft:water_bucket": 1, "minecraft:milk_bucket": 1,
    "minecraft:powder_snow_bucket": 1, "minecraft:axolotl_bucket": 1, "minecraft:cod_bucket": 1,
    "minecraft:pufferfish_bucket": 1, "minecraft:salmon_bucket": 1, "minecraft:tadpole_bucket": 1,
    "minecraft:tropical_fish_bucket": 1,
    "minecraft:minecart": 1, "minecraft:chest_minecart": 1, "minecraft:furnace_minecart": 1,
    "minecraft:hopper_minecart": 1, "minecraft:tnt_minecart": 1,
    "minecraft:saddle": 1, "minecraft:potion": 1, "minecraft:splash_potion": 1, "minecraft:lingering_potion": 1,
    "minecraft:shield": 1, "minecraft:flint_and_steel": 1, "minecraft:shears": 1, "minecraft:bow": 1,
    "minecraft:crossbow": 1, "minecraft:fishing_rod": 1, "minecraft:trident": 1, "minecraft:elytra": 1,
    "minecraft:spyglass": 1, "minecraft:goat_horn": 1, "minecraft:recovery_compass": 1,
    "minecraft:lodestone_compass": 1, "minecraft:bundle": 1, "minecraft:armor_stand": 1,
    "minecraft:turtle_helmet": 1,
    "minecraft:iron_horse_armor": 1, "minecraft:golden_horse_armor": 1, "minecraft:diamond_horse_armor": 1,
    "minecraft:leather_horse_armor": 1, "minecraft:lead": 1, "minecraft:name_tag": 1,
    "minecraft:wooden_sword": 1, "minecraft:stone_sword": 1, "minecraft:iron_sword": 1, "minecraft:golden_sword": 1, "minecraft:diamond_sword": 1, "minecraft:netherite_sword": 1,
    "minecraft:wooden_pickaxe": 1, "minecraft:stone_pickaxe": 1, "minecraft:iron_pickaxe": 1, "minecraft:golden_pickaxe": 1, "minecraft:diamond_pickaxe": 1, "minecraft:netherite_pickaxe": 1,
    "minecraft:wooden_axe": 1, "minecraft:stone_axe": 1, "minecraft:iron_axe": 1, "minecraft:golden_axe": 1, "minecraft:diamond_axe": 1, "minecraft:netherite_axe": 1,
    "minecraft:wooden_shovel": 1, "minecraft:stone_shovel": 1, "minecraft:iron_shovel": 1, "minecraft:golden_shovel": 1, "minecraft:diamond_shovel": 1, "minecraft:netherite_shovel": 1,
    "minecraft:wooden_hoe": 1, "minecraft:stone_hoe": 1, "minecraft:iron_hoe": 1, "minecraft:golden_hoe": 1, "minecraft:diamond_hoe": 1, "minecraft:netherite_hoe": 1,
    "minecraft:leather_helmet": 1, "minecraft:chainmail_helmet": 1, "minecraft:iron_helmet": 1, "minecraft:golden_helmet": 1, "minecraft:diamond_helmet": 1, "minecraft:netherite_helmet": 1,
    "minecraft:leather_chestplate": 1, "minecraft:chainmail_chestplate": 1, "minecraft:iron_chestplate": 1, "minecraft:golden_chestplate": 1, "minecraft:diamond_chestplate": 1, "minecraft:netherite_chestplate": 1,
    "minecraft:leather_leggings": 1, "minecraft:chainmail_leggings": 1, "minecraft:iron_leggings": 1, "minecraft:golden_leggings": 1, "minecraft:diamond_leggings": 1, "minecraft:netherite_leggings": 1,
    "minecraft:leather_boots": 1, "minecraft:chainmail_boots": 1, "minecraft:iron_boots": 1, "minecraft:golden_boots": 1, "minecraft:diamond_boots": 1, "minecraft:netherite_boots": 1,
    "minecraft:totem_of_undying": 1,
    "minecraft:cake": 1,
    "minecraft:white_bed": 1, "minecraft:orange_bed": 1, "minecraft:magenta_bed": 1, "minecraft:light_blue_bed": 1, "minecraft:yellow_bed": 1, "minecraft:lime_bed": 1, "minecraft:pink_bed": 1, "minecraft:gray_bed": 1, "minecraft:light_gray_bed": 1, "minecraft:cyan_bed": 1, "minecraft:purple_bed": 1, "minecraft:blue_bed": 1, "minecraft:brown_bed": 1, "minecraft:green_bed": 1, "minecraft:red_bed": 1, "minecraft:black_bed": 1,
    "minecraft:music_disc_13": 1, "minecraft:music_disc_cat": 1, "minecraft:music_disc_blocks": 1, "minecraft:music_disc_chirp": 1, "minecraft:music_disc_far": 1, "minecraft:music_disc_mall": 1, "minecraft:music_disc_mellohi": 1, "minecraft:music_disc_stal": 1, "minecraft:music_disc_strad": 1, "minecraft:music_disc_ward": 1, "minecraft:music_disc_11": 1, "minecraft:music_disc_wait": 1, "minecraft:music_disc_otherside": 1, "minecraft:music_disc_5": 1, "minecraft:music_disc_pigstep": 1, "minecraft:music_disc_relic": 1,
    "minecraft:flower_banner_pattern": 1, "minecraft:creeper_banner_pattern": 1, "minecraft:skull_banner_pattern": 1, "minecraft:mojang_banner_pattern": 1, "minecraft:globe_banner_pattern": 1, "minecraft:piglin_banner_pattern": 1,
} 