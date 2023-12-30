import os

abs_path = os.path.dirname(os.path.abspath(__file__))

ENTITY_SIZES = ("tiny", "small", "medium", "large", "gargantuan")

YN_CONST = ('y', 'n', 'yes', 'no')

PROFICIENCY_PATH = abs_path.replace("\\", "/") + "/Data/Sources/proficiencies.json"
TRAITS_PATH = abs_path.replace("\\", "/") + "/Data/Sources/traits.json"
RACES_PATH = abs_path.replace("\\", "/") + "/Data/Sources/races.json"
NPC_DIR = abs_path.replace("\\", "/") + "/Data/Characters/NPCs/"
PC_DIR = abs_path.replace("\\", "/") + "/Data/Characters/PCs/"

