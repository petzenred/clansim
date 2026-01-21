# sprite_utils.py - Sprite functions used by scattered modules. Used to avoid circular imports.
#                   Also used to archive functions which aren't currently used, but which might
#                   be useful again in the future.

########################################################################################################################
# Imports
########################################################################################################################

import pygame


########################################################################################################################
# Functions
########################################################################################################################

def subtract_lineart(surface, mask_surf, bg_color):
    """
    Though I doubt there will be a use-case for this in the future, this is a helper function I wrote to extract the
    semitransparent layer of sparkles from our original StarClan sprites. It requires a mask to work but could probably
    be altered to remove the need. honestly, I just want this in here so that we have it in at least one commit if
    we turn out to need something like this again lol it was AWFUL to figure out
    """
    width, height = surface.get_size()
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)

    bg_r, bg_g, bg_b = bg_color.r, bg_color.g, bg_color.b

    surface.lock()
    overlay.lock()

    for y in range(height):
        for x in range(width):
            r, g, b, a = surface.get_at((x, y))

            # If fully transparent, skip
            if a == 0 or mask_surf.get_at((x, y)).a < 120:
                overlay.set_at((x, y), (r, g, b, a))
                continue

            best_error = float("inf")
            best_color = (0, 0, 0)
            best_alpha = 0

            alpha_steps = 255
            # do a heinous process where we eyeball the alpha
            for step in range(1, alpha_steps + 1):
                alpha = step / alpha_steps

                try:
                    # Recover overlay color for this alpha
                    o_r = (r - (1 - alpha) * bg_r) / alpha
                    o_g = (g - (1 - alpha) * bg_g) / alpha
                    o_b = (b - (1 - alpha) * bg_b) / alpha
                except ZeroDivisionError:
                    continue

                # if it makes no sense, skip
                if not (0 <= o_r <= 255 and 0 <= o_g <= 255 and 0 <= o_b <= 255):
                    continue

                # Simulate the blend & compare
                sim_r = o_r * alpha + bg_r * (1 - alpha)
                sim_g = o_g * alpha + bg_g * (1 - alpha)
                sim_b = o_b * alpha + bg_b * (1 - alpha)

                error = abs(sim_r - r) + abs(sim_g - g) + abs(sim_b - b)

                if error < best_error:
                    best_error = error
                    best_color = (int(round(o_r)), int(round(o_g)), int(round(o_b)))
                    best_alpha = int(round(alpha * 255))

            # Set recovered overlay color
            overlay.set_at((x, y), (*best_color, best_alpha))

    surface.unlock()
    overlay.unlock()
    return overlay
