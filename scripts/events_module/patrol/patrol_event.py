#!/usr/bin/env python3
# -*- coding: ascii -*-
from dataclasses import dataclass, field
from typing import List, Optional

from definitions import Biome, PatrolType, Season
from scripts.events_module.patrol.patrol_outcome import PatrolOutcome

import logging
logger = logging.getLogger(__name__)


@dataclass
class PatrolEvent:

    patrol_id: str

    weight: int
    min_cats: int
    max_cats: int
    chance_of_success: int

    camp: List[str]

    patrol_art_path: str = None
    patrol_art_clean_path: str = None
    intro_text: str = ""
    decline_text: str = ""

    # patrol constraints
    tags: List[str] = field(default_factory=list)
    biomes: List[Biome] = (Biome.NoBiome,)
    seasons: List[Season] = (Season.NoSeason,)
    patrol_types: List[PatrolType] = field(default_factory=list)
    min_max_status: dict = field(default_factory=dict)
    relationship_constraints: List = field(default_factory=list)
    success_outcomes: List[PatrolOutcome] = field(default_factory=list)
    fail_outcomes: List[PatrolOutcome] = field(default_factory=list)
    antag_success_outcomes: List[PatrolOutcome] = field(default_factory=list)
    antag_fail_outcomes: List[PatrolOutcome] = field(default_factory=list)
    pl_skill_constraints: List[str] = field(default_factory=list)
    pl_trait_constraints: List[str] = field(default_factory=list)

    @property
    def new_cat(self) -> bool:
        """Returns boolean if there are any outcomes that results in a new cat joining (not just meeting)"""

        for out in self.success_outcomes + self.fail_outcomes + self.antag_fail_outcomes + self.antag_success_outcomes:
            for sublist in out.new_cat:
                if "join" in sublist:
                    return True

        return False

    @property
    def other_clan(self) -> bool:
        """Return boolean indicating if any outcome has any reputation effect"""
        for out in self.success_outcomes + self.fail_outcomes + self.antag_fail_outcomes + self.antag_success_outcomes:
            if out.other_clan_rep is not None:
                return True

        return False

    @property
    def herbs_given(self) -> list:
        """Returns list of herbs available to get from this patrol"""
        herb_list = []
        for out in self.success_outcomes + self.fail_outcomes + self.antag_fail_outcomes + self.antag_success_outcomes:
            herb_list.extend([herb for herb in out.herbs if herb not in herb_list])

        return herb_list
