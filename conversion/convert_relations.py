import os

from scripts._red.io_manager import io_manager
from scripts.housekeeping.datadir import get_save_dir

# -------------------------------------------------------------------------------- #
# ----------------------------------------

########################################################################################################################
# Constants
########################################################################################################################


########################################################################################################################
# Imports
########################################################################################################################


new_relations_cats: dict = {}
new_relations_clans: dict = {}

# ------------------------------------ convert relations files ----------------------------------- #

def convert_relations_files(clan_prefix: str):

    relations_dir_path: str = f"{get_save_dir()}/{clan_prefix}/relationships/"
    relations_dir_path = relations_dir_path.replace("//", "/")
    new_filename: str = f"relationships_{clan_prefix}.yaml"
    relations_files: list = [filename for filename in os.listdir(relations_dir_path) if '.json' in filename]

    for relation_filename in relations_files:
        old_relations: list = io_manager.read_file(filepath=relations_dir_path + relation_filename)
        from_cat_id: int = int(relation_filename.split("_")[0])
        from_cat_relations: dict = {}
        for relation in old_relations:
            from_cat_relations.update({
                int(relation["cat_to_id"]): {
                    "log": list(relation["log"]),
                    "romance": relation["romantic_love"],
                    "friendship": relation["platonic_like"],
                    "dislike": relation["dislike"],
                    "respect": relation["admiration"],
                    "comfort": relation["comfortable"],
                    "jealousy": relation["jealousy"],
                    "trust": relation["trust"],
            }})
        new_relations_cats.update({ from_cat_id: from_cat_relations })
    # write to the save file folder, not the relationships/ directory inside it
    io_manager.write_relationships_save_file(cat_relationships=new_relations_cats,
                                             clan_relationships=new_relations_clans)


io_manager.update_active_clan_token()
convert_relations_files("Test")