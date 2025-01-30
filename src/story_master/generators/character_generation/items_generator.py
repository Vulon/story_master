import re
from difflib import get_close_matches

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
import random
from story_master.entities.items.equipment import EquipmentType, EQUIPMENT
from story_master.entities.items.weapons import WeaponType, WEAPONS
from story_master.entities.items.armor import ArmorType, ARMORS
from story_master.entities.items.instruments import InstrumentType, INSTRUMENTS
from story_master.entities.items.items import Item
from story_master.utils.selection import get_batched
from story_master.log import logger

ITEMS_BATCH_SIZE = 10


class MerchantStockGenerator:
    PROMPT = """
    You are a Dungeons and Dragons agent.

    -Goal-
    Generate a list of items that the merchant has in stock.
    
    -Steps-
    1. Read the description of the merchant.
    2. Read the location description.
    3. Read the list of items that you can pick from.
    4. Read the list of items, that the merchant already has in stock.    
    5. Pick item names that fit the merchant's description.
        If the merchant already has enough items, you can output the empty list. 
        If the items presented to you don't match the merchant's description, you can also output the empty list.
    6. Output the names of the items in XML format.
        Format: <Item>Item name</Item>
        Output every item in a separate line.
    You can output the same item multiple times. 
    You can do it in the following format:
        Format: <Item>Item name * 3</Item> 
        This means that the merchant has 3 copies of the item.
        
    -Merchant description-
    {merchant_description}
    
    -Location description-
    {location_description}
    
    -Available items-
    {available_items}
    
    -Existing items-
    {items}
    
    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.llm_model = llm_model
        prompt = PromptTemplate.from_template(self.PROMPT)
        self.pattern = re.compile(r"<Item>(.*?)</Item>")
        self.chain = prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str) -> list[str]:
        try:
            output = output.replace("\n", " ").strip()
            matches = self.pattern.findall(output)
            item_names = []
            for match in matches:
                parts = match.split("*")
                if len(parts) == 1:
                    item_names.append(parts[0].strip())
                else:
                    item_name = parts[0].strip()
                    count = int(parts[1].strip())
                    item_names.extend([item_name] * count)
            return item_names
        except Exception:
            logger.error(f"MerchantStockGenerator. Failed to parse output: {output}")
            return []

    def get_equipment_names(self) -> list[str]:
        equipment_names = [item.value for item in EQUIPMENT.keys()]
        return equipment_names

    def get_weapon_names(self) -> list[str]:
        weapon_names = [item.value for item in WEAPONS.keys()]
        return weapon_names

    def get_armor_names(self) -> list[str]:
        armor_names = [item.value for item in ARMORS.keys()]
        return armor_names

    def get_instrument_names(self) -> list[str]:
        instrument_names = [item.value for item in INSTRUMENTS.keys()]
        return instrument_names

    def generate(
        self, merchant_description: str, location_description: str
    ) -> list[Item]:
        equipment_names = self.get_equipment_names()
        weapon_names = self.get_weapon_names()
        armor_names = self.get_armor_names()
        instrument_names = self.get_instrument_names()
        available_items = (
            equipment_names + weapon_names + armor_names + instrument_names
        )
        random.shuffle(available_items)

        all_items = []
        all_generated_strings = []
        for items_batch in get_batched(available_items, ITEMS_BATCH_SIZE):
            available_items_string = (
                "<AvailableItems>" + " ; ".join(items_batch) + "</AvailableItems>"
            )
            generated_item_names = self.chain.invoke(
                {
                    "merchant_description": f"<Merchant>{merchant_description}</Merchant>",
                    "location_description": location_description,
                    "available_items": available_items_string,
                    "items": " ; ".join(all_generated_strings),
                }
            )
            all_generated_strings.extend(generated_item_names)
            for raw_item_name in generated_item_names:
                try:
                    match = get_close_matches(available_items, items_batch)[0]
                    if match in equipment_names:
                        item = EQUIPMENT[EquipmentType(match)]
                    elif match in weapon_names:
                        item = WEAPONS[WeaponType(match)]
                    elif match in armor_names:
                        item = ARMORS[ArmorType(match)]
                    else:
                        item = INSTRUMENTS[InstrumentType(match)]
                    all_items.append(item)
                except Exception:
                    logger.error(f"Failed to generate item: {raw_item_name}")

        return all_items
