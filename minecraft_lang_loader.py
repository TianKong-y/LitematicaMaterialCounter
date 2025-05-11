import json
import os

def load_translations(lang_file_relative_path='./lang/zh_cn.json'):
    translations = {}
    # Construct absolute path to lang file based on this script's location
    loader_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_lang_file_path = os.path.normpath(os.path.join(loader_dir, lang_file_relative_path))

    try:
        with open(absolute_lang_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Process Blocks
        if 'Blocks' in data and isinstance(data['Blocks'], dict):
            for key, value in data['Blocks'].items():
                translations[f"minecraft:{key}"] = value
        
        # Process Items
        if 'Items' in data and isinstance(data['Items'], dict):
            for key, value in data['Items'].items():
                # Items might overwrite Blocks if keys are identical after prefixing,
                # which is usually fine as item names are often preferred.
                translations[f"minecraft:{key}"] = value
        
        # Optionally, process other categories if needed in the future
        # e.g., Entities, Biomes etc.

    except FileNotFoundError:
        print(f"[ERROR] Minecraft language file not found at: {absolute_lang_file_path}")
        print("[INFO] Please ensure 'lang/zh_cn.json' exists at the workspace root relative to the 'LitematicaMaterialCounter' directory.")
    except json.JSONDecodeError:
        print(f"[ERROR] Could not decode JSON from language file: {absolute_lang_file_path}")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred while loading translations: {e}")
            
    return translations

if __name__ == '__main__':
    # Test the loader
    # This assumes you run this script directly from the LitematicaMaterialCounter directory
    # and the lang folder is one level up.
    test_translations = load_translations()
    if test_translations:
        print(f"Successfully loaded {len(test_translations)} translations from '{test_translations.get('_source_path', '../lang/zh_cn.json')}'.")
        # Print a few examples
        examples = {
            "minecraft:stone": "石头",
            "minecraft:stick": "木棍",
            "minecraft:apple": "苹果",
            "minecraft:dirt": "泥土",
            "minecraft:air": "空气" # From Blocks
        }
        for item_id, expected_name in examples.items():
            if item_id in test_translations:
                print(f"Translation for '{item_id}': '{test_translations[item_id]}' (Expected: '{expected_name}')")
            else:
                print(f"Translation for '{item_id}' NOT FOUND.")
    else:
        print("Failed to load translations or translations are empty.") 