# -*- coding: utf-8 -*-
import pygame
import sys
import datetime
import json
import os
import glob

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 30
CONFIG_FILE = "RHCompletionMMP_config.json"

#-------------------------------------------------------------------------------

# Get a parameter in the config file
def get_config_param(key, default=None):
    # Check config file existence
    if not os.path.exists(CONFIG_FILE):
        print("Warning: Config file not found: %s" % CONFIG_FILE)
        return default
    # Read config parameter
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            print("Error: Config is not a JSON object.")
            return default
        return data.get(key, default)
    except Exception as e:
        print("Error reading config file '%s': %s" % (CONFIG_FILE, e))
        return default

#-------------------------------------------------------------------------------

def load_screenshot(screenshot_path, screen_size, keep_aspect_ratio):
    """
    Loads a PNG screenshot, scales it to fit the screen size, and returns:
    - the scaled image (as a Surface)
    - its position (as a Rect) to center it on the screen

    Args:
        screenshot_path (str): Path to the PNG file
        screen_size (tuple): (width, height) of the screen
        keep_aspect_ratio (bool): If True, preserve image aspect ratio

    Returns:
        (Surface, Rect): Scaled image and its blit position
    """
    # Load the image
    image = pygame.image.load(screenshot_path)
    img_w, img_h = image.get_size()
    screen_w, screen_h = screen_size

    if keep_aspect_ratio:
        # Compute scale factor while maintaining aspect ratio
        scale = min(float(screen_w) / img_w, float(screen_h) / img_h)
        scale_w = int(img_w * scale)
        scale_h = int(img_h * scale)
    else:
        # Stretch to screen size
        scale_w = screen_w
        scale_h = screen_h

    # Scale the image
    scaled_image = pygame.transform.smoothscale(image, (scale_w, scale_h))

    # Center the image
    pos_x = (screen_w - scale_w) // 2
    pos_y = (screen_h - scale_h) // 2

    return scaled_image, (pos_x, pos_y)

#-------------------------------------------------------------------------------

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()

    # Font setup
    font_size = int(get_config_param("font_size", 42))
    font = pygame.font.Font(None, font_size)

    # List screenshots
    screenshot_keep_aspect_ratio = False
    screenshots_directory = get_config_param("screenshots_directory", "/mnt/SDCARD/Screenshots")
    screenshots_pattern = get_config_param("screenshots_pattern", "*.png")
    screenshots_list = glob.glob(os.path.join(screenshots_directory, screenshots_pattern))
    if not screenshots_list:
        screenshots_list = ["no_screenshots.png"]
    else:
        # Sort files by creation time, newest -> oldest
        screenshots_list.sort(key=lambda f: os.path.getctime(f), reverse=True)
    screenshot_index = 0

    # Load newest screenshot
    screenshot_surf, screenshot_position = load_screenshot(screenshots_list[screenshot_index], screen.get_size(), screenshot_keep_aspect_ratio)

    # Parameters of the note
    note_x = int(get_config_param("note_x", 0))
    note_y = int(get_config_param("note_y", 0))
    note_padding = int(get_config_param("note_padding", 24))
    note_bg_color = tuple(get_config_param("note_background_color", (255, 255, 64)))
    note_text_color = tuple(get_config_param("note_text_color", (0, 0, 0)))

    # RH Logo
    logo_surf = pygame.image.load("rh_logo_black.png")
    logo_w, logo_h = logo_surf.get_size()
    logo_x = note_x + note_padding
    logo_y = note_y + note_padding

    # Render nickname
    nickname = get_config_param("nickname", "My Nickname")
    nickname_surf = font.render(nickname, True, note_text_color)
    nickname_w, nickname_h = nickname_surf.get_size()
    nickname_x = logo_x + logo_w + note_padding
    nickname_y = logo_y

    # Render current date as 'Jul 3, 2025'
    today = datetime.datetime.now()
    formatted_date = today.strftime("%b %d, %Y").replace(" 0", " ")
    date_surf = font.render(formatted_date, True, note_text_color)
    date_w, date_h = date_surf.get_size()
    date_x = nickname_x
    date_y = logo_y + logo_h - date_h

    # Note dimensions depend on the other surfaces
    note_height = logo_h + 2 * note_padding
    note_width = logo_w + max(nickname_w, date_w) + 3 * note_padding
    note_rect = pygame.Rect(note_x, note_y, note_width, note_height)

    # Main loop
    running = True
    while running:
        # Handle events
        # L1=K_e, L2=K_TAB, R1=K_t, R2=K_BACKSPACE, X=K_LSHIFT, Y=K_LALT, B=K_LCTRL, A=K_SPACE, SELECT=K_RCTRL, START=K_RETURN, DPADUP=K_UP, DPADDOWN=K_DOWN, DPAFLEFT=K_LEFT, DPADRIGHT=K_RIGHT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # B button => quit
                if event.key == pygame.K_LCTRL:
                    running = False
                # Down => load next screenshot
                elif event.key == pygame.K_DOWN:
                    if screenshot_index < len(screenshots_list) - 1:
                        screenshot_index += 1
                        screenshot_surf, screenshot_position = load_screenshot(screenshots_list[screenshot_index], screen.get_size(), screenshot_keep_aspect_ratio)
                # Up => load previous screenshot
                elif event.key == pygame.K_UP:
                    if screenshot_index > 0:
                        screenshot_index -= 1
                        screenshot_surf, screenshot_position = load_screenshot(screenshots_list[screenshot_index], screen.get_size(), screenshot_keep_aspect_ratio)
                # A => toggle screenshot_keep_aspect_ratio
                elif event.key == pygame.K_SPACE:
                    screenshot_keep_aspect_ratio = not screenshot_keep_aspect_ratio
                    screenshot_surf, screenshot_position = load_screenshot(screenshots_list[screenshot_index], screen.get_size(), screenshot_keep_aspect_ratio)

        # Clear screen
        screen.fill((0, 0, 0))
        # Draw the screenshot
        screen.blit(screenshot_surf, screenshot_position)
        # Draw the note
        pygame.draw.rect(screen, note_bg_color, note_rect)
        # Draw logo
        screen.blit(logo_surf, (logo_x, logo_y))
        # Draw nickname
        screen.blit(nickname_surf, (nickname_x, nickname_y))
        # Draw date
        screen.blit(date_surf, (date_x, date_y))
        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
