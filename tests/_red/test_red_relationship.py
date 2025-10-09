import unittest

from scripts._red.io_manager import io_manager

io_manager.update_active_clan_prefix(new_active_clan_prefix="Test")
from scripts._red.cats.red_relationship import global_rels
from definitions import RelationshipAspect

# from_cat_id=8, to_cat_id=1
EXPECTED_CAT_RELATIONSHIP: dict = {
    RelationshipAspect.Romance: 0,
    RelationshipAspect.Friendship: 3,
    RelationshipAspect.Dislike: 8,
    RelationshipAspect.Respect: 6,
    RelationshipAspect.Comfort: 20,
    RelationshipAspect.Jealousy: 12,
    RelationshipAspect.Trust: 6,
    "log": [
        "Magpiepaw is jealous that Chickfoot got to go to the last Gathering. (medium negative effect)- Magpiepaw was 10 moons old"
    ]
}

class TestIOUtils(unittest.TestCase):
    # do this before running any of the tests

    def test_cat_get_relationship_return_rel(self):
        self.assertEqual(EXPECTED_CAT_RELATIONSHIP, global_rels.cat_get_relationship(holder=8, subject=1))

    def test_cat_get_relationship_raise_key_error(self):
        try:
            global_rels.cat_get_relationship(holder=-1, subject=8)
        except KeyError as err:
            if err.args == (-1, ):
                self.assertTrue(True, msg="cat_get_relationship() raises KeyError when subject doesn't exist")
            else:
                self.assertTrue(False, msg=f"Expected KeyError's arg to be -1 but instead it was: {err}")
        else:
            self.assertTrue(False, msg=f"Should have raised a KeyError but didn't")
        try:
            global_rels.cat_get_relationship(holder=8, subject=-1)
        except KeyError as err:
            if err.args == (-1, ):
                self.assertTrue(True, msg="cat_get_relationship() raises KeyError when subject doesn't exist")
            else:
                self.assertTrue(False, msg=f"Expected KeyError's arg to be -1 but instead it was: {err}")
        else:
            self.assertTrue(False, msg=f"Should have raised a KeyError but didn't")
        # self.assertRaises(expected_exception=KeyError, callable=global_rels.cat_get_relationship(holder=8, subject=-1))


if __name__ == '__main__':
    unittest.main()
