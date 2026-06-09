# test_cat_tracker.py - Test the functions in the CatTracker class.
import logging
########################################################################################################################
# Imports
########################################################################################################################

import unittest
from typing import Union

from scripts._red.cat_tracker import CatTracker
from definitions import LONER_CLAN_TOKEN, Rank, Location

########################################################################################################################
# Fake classes
########################################################################################################################

class FakeName:
    """ Shell RedName class that exists to test CatTracker functions. """

    prefix: str
    suffix: str

    def __init__(self, prefix: str, suffix: str):
        self.prefix = prefix
        self.suffix = suffix

    def __repr__(self):
        return f"{self.prefix}{self.suffix}"

class FakeCat:
    """ Shell RedCat class that exists to test CatTracker functions. """

    cat_id: int
    name: Union[str, FakeName]
    clan_token: str
    alive: bool
    rank: Rank
    moons: int
    faded: bool

    def __init__(self, name: Union[str, FakeName], clan_token: str, alive: bool, rank: Rank, moons: int,
                 faded: bool = False):
        self.name = name
        self.clan_token = clan_token
        self.alive = alive
        self.rank = rank
        self.moons = moons
        self.faded = faded

class FakeClan:
    """ Shell RedClan class that exists to test CatTracker functions. """

    clan_token: str
    clan_name: str
    clan_cats: dict[int, FakeCat]

    def __init__(self, clan_token: str,):
        self.clan_token = clan_token
        if self.clan_token == LONER_CLAN_TOKEN:
            self.clan_name = "LONERS"
        else:
            self.clan_name = self.clan_token + "Clan"
        self.clan_cats = {}

    def add_cat_to_clan(self, cat_obj: FakeCat):
        print(f"Adding {cat_obj.name} to {self.clan_name}")
        self.clan_cats[cat_obj.cat_id] = cat_obj
        cat_obj.clan_token = self.clan_token

    def remove_cat_from_clan(self, cat_obj: FakeCat):
        print(f"Removing {cat_obj.name} from {self.clan_name}")
        self.clan_cats.pop(cat_obj.cat_id)


########################################################################################################################
# Constants
########################################################################################################################

SKY_PREFIX: str = "Sky"
SHADOW_PREFIX: str = "Shadow"
THUNDER_PREFIX: str = "Thunder"


########################################################################################################################
# Test cases
########################################################################################################################

class TestCatTracker(unittest.TestCase):

    def test__get_new_id(self):
        print(f"\nSetting up _get_new_id...")
        print(f"No setup required\n")

        print(f"Testing CatTracker's ability to generate IDs after starting a new save file")
        ct1 = CatTracker()
        self.assertEqual(1, ct1._get_new_id())
        self.assertEqual(2, ct1._get_new_id())
        del ct1
        print(f"Test case passed!\n")

        print(f"Testing CatTracker's ability to generate IDs after loading a save file")
        ct2 = CatTracker(3)
        self.assertEqual(4, ct2._get_new_id())
        del ct2
        print(f"Test case passed!\n")

        print(f"Tests for CatTracker._get_new_id\n")

    def test_add_new_clan(self):
        print(f"\nSetting up add_new_clan...")
        ct = CatTracker()
        skyclan = FakeClan(clan_token=SKY_PREFIX)
        print(f"Set up complete\n")

        print(f"Testing CatTracker's ability to add a new Clan object")
        ct.add_new_clan(clan_obj=skyclan)
        self.assertIs(skyclan, ct.all_clans[SKY_PREFIX])
        print(f"Test case passed!\n")

        print(f"Testing CatTracker's response to adding a Clan with a prefix that's taken")
        with self.assertRaises(ValueError):
            ct.add_new_clan(clan_obj=skyclan)
        print(f"Test case passed!\n")

        del ct
        print(f"Tests for CatTracker.add_new_clan passed\n")

    def test_get_clan_object(self):
        print(f"\nSetting up get_clan_object...")
        ct = CatTracker()
        skyclan = FakeClan(clan_token=SKY_PREFIX)
        shadowclan = FakeClan(clan_token=SHADOW_PREFIX)
        print(f"Set up complete\n")

        print(f"Testing getting an existing Clan from the CatTracker")
        ct.add_new_clan(clan_obj=skyclan)
        self.assertIs(skyclan, ct.get_clan_object(clan_token=skyclan.clan_token))
        print(f"Test case passed!\n")

        print(f"Testing getting a Clan which doesn't exist from the CatTracker")
        with self.assertRaises(KeyError):
            ct.get_clan_object(clan_token=shadowclan.clan_token)
        print(f"Test case passed!\n")

        del ct
        print(f"Tests for CatTracker.get_clan_object passed\n")

    def test_add_new_cat(self):
        print(f"\nSetting up test_add_new_cat...")
        ct = CatTracker()
        leafdapple = FakeCat(name=FakeName(prefix="Leaf", suffix="dapple"), clan_token=SKY_PREFIX, alive=True,
                             rank=Rank.Warrior, moons=36)
        echosong = FakeCat(name=FakeName(prefix="Echo", suffix="song"), clan_token=SKY_PREFIX, alive=True,
                           rank=Rank.Healer, moons=50)
        sharpclaw = FakeCat(name=FakeName(prefix="Sharp", suffix="claw"), clan_token=SKY_PREFIX, alive=True,
                            rank=Rank.Warrior, moons=81)
        harrybrook = FakeCat(name=FakeName(prefix="Harry", suffix="brook"), clan_token=SKY_PREFIX, alive=True,
                             rank=Rank.Warrior, moons=81)
        print(f"Set up complete\n")

        print(f"Testing finding the first cat added to CatTracker")
        self.assertEqual(1, ct.add_cat_to_tracker(leafdapple))
        leafdapple.cat_id = 1
        self.assertEqual(leafdapple, ct.living_cats[1])
        print(f"Test case passed!\n")

        print(f"Testing finding a further cat added to CatTracker")
        self.assertEqual(2, ct.add_cat_to_tracker(echosong))
        echosong.cat_id = 2
        self.assertEqual(echosong, ct.living_cats[2])
        print(f"Test case passed!\n")

        print(f"Testing adding a cat with a pre-determined ID number to CatTracker")
        self.assertEqual(3, ct.add_cat_to_tracker(cat_obj=sharpclaw, cat_id=3))
        sharpclaw.cat_id = 3
        self.assertEqual(sharpclaw, ct.living_cats[3])
        print(f"Test case passed!\n")

        print(f"Testing adding another cat without a pre-determined ID number to CatTracker")
        self.assertEqual(4, ct.add_cat_to_tracker(cat_obj=harrybrook))
        harrybrook.cat_id = 4
        self.assertEqual(harrybrook, ct.living_cats[4])
        print(f"Test case passed!\n")

        del ct
        print(f"Tests for CatTracker.get_clan_object passed\n")

    def test_get_cat_object(self):
        print(f"\nSetting up test_get_cat_object...")
        ct = CatTracker()
        leafdapple = FakeCat(name=FakeName(prefix="Leaf", suffix="dapple"), clan_token=SKY_PREFIX, alive=True,
                             rank=Rank.Warrior, moons=36)
        cat_id = ct.add_cat_to_tracker(leafdapple)
        echosong = FakeCat(name=FakeName(prefix="Echo", suffix="song"), clan_token=SKY_PREFIX, alive=True,
                           rank=Rank.Healer, moons=50)
        print(f"Set up complete\n")

        print(f"Testing getting an existing cat from CatTracker")
        self.assertEqual(leafdapple, ct.get_cat_objects(cat_id=cat_id)[0])
        print(f"Test case passed!\n")

        print(f"Testing getting a cat which doesn't exist from CatTracker")
        with self.assertRaises(AttributeError):
            _ = ct.get_cat_objects(echosong.cat_id)[0]
        print(f"Test case passed!\n")

        del ct
        print(f"Tests for CatTracker.get_cat_object passed\n")

    def test_destroy_clan(self):
        print(f"\nSetting up test_destroy_clan...")
        ct = CatTracker()
        leafdapple = FakeCat(name=FakeName(prefix="Leaf", suffix="dapple"), clan_token=SKY_PREFIX, alive=True,
                             rank=Rank.Warrior, moons=36)
        leafdapple.cat_id = ct.add_cat_to_tracker(leafdapple)
        echosong = FakeCat(name=FakeName(prefix="Echo", suffix="song"), clan_token=SKY_PREFIX, alive=True,
                           rank=Rank.Healer, moons=50)
        echosong.cat_id = ct.add_cat_to_tracker(echosong)
        outsiders = FakeClan(clan_token=LONER_CLAN_TOKEN)
        skyclan = FakeClan(clan_token=SKY_PREFIX)
        ct.add_new_clan(outsiders)
        ct.add_new_clan(skyclan)
        skyclan.add_cat_to_clan(leafdapple)
        skyclan.add_cat_to_clan(echosong)
        print(f"Set up complete\n")

        print(f"Testing destroying an existing Clan in CatTracker")
        ct.destroy_clan(clan_obj=skyclan)
        self.assertIn(SKY_PREFIX, ct.destroyed_clans)
        self.assertNotIn(SKY_PREFIX, ct.all_clans)
        self.assertIs(skyclan, ct.get_clan_object(clan_token=SKY_PREFIX))
        print(f"Test case passed!\n")

        del ct
        print(f"Tests for CatTracker.destroy_clan passed\n")

    def test_kill_cat(self):
        print(f"\nSetting up test_kill_cat...")
        ct = CatTracker()
        leafdapple = FakeCat(name=FakeName(prefix="Leaf", suffix="dapple"), clan_token=SKY_PREFIX, alive=True,
                             rank=Rank.Warrior, moons=36)
        leafdapple.cat_id = ct.add_cat_to_tracker(leafdapple)
        echosong = FakeCat(name=FakeName(prefix="Echo", suffix="song"), clan_token=SKY_PREFIX, alive=True,
                           rank=Rank.Healer, moons=50)
        echosong.cat_id = ct.add_cat_to_tracker(echosong)
        skyclan = FakeClan(clan_token=SKY_PREFIX)
        ct.add_new_clan(skyclan)
        skyclan.add_cat_to_clan(leafdapple)
        skyclan.add_cat_to_clan(echosong)
        print(f"Set up complete\n")

        print(f"Testing sending a dead cat to a afterlife (StarClan) location in CatTracker")
        ct.kill_cat(cat_obj=leafdapple, afterlife=Location.StarClan)
        self.assertIn((leafdapple.cat_id, leafdapple), ct.dead_cats_by_location[Location.StarClan])
        print(f"Test case passed!\n")

        print(f"Testing sending a dead cat to a non-afterlife location in CatTracker")
        msg = (f"Trying to send a dead cat to a non-afterlife location should raise a "
               f"ValueError in CatTracker.kill_cat() but didn't")
        with self.assertRaises(ValueError, msg=msg):
            ct.kill_cat(cat_obj=echosong, afterlife=Location.ClanHealer)
        print(f"Test case passed!\n")

        del ct
        print(f"Tests for CatTracker.kill_cat passed\n")

    def test_get_name_prefixes_of_clan(self):
        print(f"\nSetting up test_get_name_prefixes_of_clan...")
        ct = CatTracker()
        leafdapple = FakeCat(name=FakeName(prefix="Leaf", suffix="dapple"), clan_token=SKY_PREFIX, alive=True,
                             rank=Rank.Warrior, moons=36)
        leafdapple.cat_id = ct.add_cat_to_tracker(leafdapple)
        echosong = FakeCat(name=FakeName(prefix="Echo", suffix="song"), clan_token=SKY_PREFIX, alive=True,
                           rank=Rank.Healer, moons=50)
        echosong.cat_id = ct.add_cat_to_tracker(echosong)
        skyclan = FakeClan(clan_token=SKY_PREFIX)
        ct.add_new_clan(skyclan)
        print(f"Set up complete\n")

        print(f"Testing name prefixes of an empty Clan")
        self.assertEqual([], ct.get_name_prefixes_of_clan(clan_token=SKY_PREFIX))
        print(f"Test case passed!\n")

        print(f"Testing name prefixes of a non-empty Clan")
        skyclan.add_cat_to_clan(leafdapple)
        skyclan.add_cat_to_clan(echosong)
        self.assertEqual(["Leaf", "Echo"], ct.get_name_prefixes_of_clan(clan_token=SKY_PREFIX))
        print(f"Test case passed!\n")

        del ct
        print(f"Tests for CatTracker.get_name_prefixes_of_clan\n")

    def test_healers(self):
        print(f"\nSetting up tests for tracking healer cats...")
        ct = CatTracker()
        echosong = FakeCat(name=FakeName(prefix="Echo", suffix="song"), clan_token=SKY_PREFIX, alive=True,
                           rank=Rank.Healer, moons=50)
        echosong.cat_id = ct.add_cat_to_tracker(cat_obj=echosong)
        print(f"Set up complete\n")

        print(f"Testing adding a healer cat to CatTracker")
        ct.add_healer_cat(cat_obj=echosong)
        print(f"Test case passed!\n")

        print(f"Testing removing an existing healer cat from CatTracker")
        ct.remove_healer_cat(cat_obj=echosong)
        print(f"Test case passed!\n")

        print(f"Testing removing a non-extant healer cat from CatTracker")
        ct.remove_healer_cat(cat_obj=echosong)
        print(f"Test case passed!\n")

        del ct
        print(f"All tests for tracking healer cats passed!\n")

    def test_queens_and_changing_clans(self):
        print(f"\nSetting up tests for queens and cats changing clans...")
        ct = CatTracker()
        outsiders = FakeClan(clan_token=LONER_CLAN_TOKEN)
        ct.add_new_clan(clan_obj=outsiders)
        shadowclan = FakeClan(clan_token=SHADOW_PREFIX)
        ct.add_new_clan(clan_obj=shadowclan)
        skyclan = FakeClan(clan_token=SKY_PREFIX)
        ct.add_new_clan(clan_obj=skyclan)

        violetshine = FakeCat(name=FakeName(prefix="Violet", suffix="shine"), clan_token=SHADOW_PREFIX, alive=True,
                              rank=Rank.Warrior, moons=12)
        violetshine.cat_id = ct.add_cat_to_tracker(violetshine)
        shadowclan.add_cat_to_clan(violetshine)
        rootkit = FakeCat(name=FakeName(prefix="Root", suffix="kit"), clan_token=SHADOW_PREFIX, alive=True,
                          rank=Rank.Kit, moons=0)
        rootkit.cat_id = ct.add_cat_to_tracker(rootkit)
        shadowclan.add_cat_to_clan(rootkit)
        print(f"Set up complete\n")

        print(f"Testing switching a warrior from one Clan to another Clan in CatTracker")
        self.assertIn(member=violetshine.cat_id, container=shadowclan.clan_cats)
        ct.change_cat_clan(new_clan_token=SKY_PREFIX, cat_obj=violetshine, new_rank=violetshine.rank)
        self.assertIn(member=violetshine.cat_id, container=skyclan.clan_cats)
        print(f"Test case passed!\n")

        print(f"Testing making a Clan cat a loner in CatTracker")
        ct.change_cat_clan(new_clan_token=LONER_CLAN_TOKEN, cat_obj=violetshine, new_rank=Rank.Loner)
        self.assertIn(member=violetshine.cat_id, container=outsiders.clan_cats)
        print(f"Test case passed!\n")

        print(f"Testing adding a loner to a warrior Clan in CatTracker")
        ct.change_cat_clan(new_clan_token=SKY_PREFIX, cat_obj=violetshine, new_rank=Rank.Warrior)
        self.assertIn(member=violetshine.cat_id, container=skyclan.clan_cats)
        print(f"Test case passed!\n")

        print(f"Testing a professional queen switching Clans in CatTracker")
        violetshine.rank = Rank.Queen
        ct.add_queen(cat_obj=violetshine, clan_token=SKY_PREFIX, professional=True)
        ct.change_cat_clan(new_clan_token=SHADOW_PREFIX, cat_obj=violetshine, new_rank=Rank.Queen)
        self.assertIn(member=violetshine.cat_id, container=shadowclan.clan_cats)
        ct.old_remove_nursing_queen(clan_token=SHADOW_PREFIX, cat_obj=violetshine)
        violetshine.rank = Rank.Warrior
        print(f"Test case passed!\n")

        print(f"Testing a nursing queen switching Clans in CatTracker")
        ct.add_queen(cat_obj=violetshine, clan_token=SHADOW_PREFIX, professional=False)
        ct.give_kit_to_queen(clan_token=SHADOW_PREFIX, kit_obj=rootkit, new_queen_obj=violetshine)
        # check that queen and kit are correctly listed in their original Clan
        self.assertIn(member=violetshine.cat_id, container=shadowclan.clan_cats,
                      msg=f"{violetshine.name} isn't listed as a member of {shadowclan.clan_name}")
        self.assertIn(member=rootkit.cat_id, container=shadowclan.clan_cats,
                      msg=f"{rootkit.name} isn't listed as a member of {shadowclan.clan_name}")
        self.assertIn(member=violetshine, container=ct.living_nursing_queens_and_kits_by_clan_token[SHADOW_PREFIX],
                      msg=f"{violetshine.name} isn't listed as a {shadowclan.clan_name} nursing queen")
        self.assertIn(member=rootkit, container=ct.living_nursing_queens_and_kits_by_clan_token[SHADOW_PREFIX][violetshine],
                      msg=f"{rootkit.name} isn't listed as one of the kits {violetshine.name} is looking after")
        # move the queen and kit to a different Clan
        ct.change_cat_clan(new_clan_token=SKY_PREFIX, cat_obj=violetshine, new_rank=violetshine.rank)
        # check that queen and kit have been correctly moved to their new Clan
        self.assertIn(member=violetshine.cat_id, container=skyclan.clan_cats,
                      msg=f"{violetshine.name} isn't listed as a member of {skyclan.clan_name}")
        self.assertIn(member=violetshine, container=ct.living_nursing_queens_and_kits_by_clan_token[SKY_PREFIX],
                      msg=f"{violetshine.name} isn't listed as a {skyclan.clan_name} nursing queen")
        self.assertIn(member=rootkit.cat_id, container=skyclan.clan_cats,
                      msg=f"{rootkit.name} isn't listed as a member of {skyclan.clan_name}")
        self.assertIn(member=rootkit, container=ct.living_nursing_queens_and_kits_by_clan_token[SKY_PREFIX][violetshine])
        print(f"Test case passed!\n")

        print(f"Testing a kit independently switching Clans in CatTracker")
        with self.assertRaises(ValueError, msg=f"{rootkit.name} shouldn't have been allowed to switch Clans alone"):
            ct.change_cat_clan(new_clan_token=SHADOW_PREFIX, cat_obj=rootkit, new_rank=rootkit.rank)
        print(f"Test case passed!\n")

        print(f"Testing how the kits of a dead nursing queen are handled")
        # sorry Violetshine! In my defense, you are a sick and dying baby boy
        ct.kill_cat(cat_obj=violetshine, afterlife=Location.StarClan)
        self.assertIn(member=rootkit, container=ct.living_nursing_queens_and_kits_by_clan_token[SKY_PREFIX][None])
        print(f"Test case passed!\n")

        del ct
        print(f"Tests for CatTracker.change_cat_clan\n")

    def test_foundlings(self):
        print(f"\nSetting up tests for tracking foundling kits...")
        ct = CatTracker()
        thunderclan = FakeClan(clan_token=THUNDER_PREFIX)
        ct.add_new_clan(clan_obj=thunderclan)
        twigkit = FakeCat(name=FakeName(prefix="Twig", suffix="kit"), clan_token=LONER_CLAN_TOKEN, alive=True, rank=Rank.Kit,
                          moons=12)
        print(f"Set up complete\n")

        print(f"Adding foundling kit to Clan")
        twigkit.cat_id = ct.add_cat_to_tracker(cat_obj=twigkit)
        print(f"Test case passed!\n")

        del ct
        print(f"All tests for tracking foundling kits passed!\t")


if __name__ == '__main__':
    unittest.main()
