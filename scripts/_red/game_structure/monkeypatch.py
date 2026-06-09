# monkeypatch.py - Functions that overwrite functions from libraries.

########################################################################################################################
# Imports
########################################################################################################################

import i18n

from scripts._red.text_handler import TextHandler


########################################################################################################################
# Instances
########################################################################################################################

text_handler: TextHandler = TextHandler()


########################################################################################################################
# Functions
########################################################################################################################

def translate(text: str, **kwargs):
    """ Translate text and replace proper nouns. """
    if text == "":
        return ""
    output = i18n.t(text, **kwargs)

    if "cats_dict" in kwargs:
        output = text_handler.handle_text(text=text, cats_dict=kwargs["cats_dict"])
    return output
