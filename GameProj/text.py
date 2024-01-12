from ctypes import c_long, pointer
import ctypes
from sdl2 import *
from sdl2.sdlttf import *

# screen size
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FONTS = "fonts/"

def renderTexture(tex, ren, x, y):
    # create destination rectangle to be at position we want
    dst = SDL_Rect(x, y)

    # create pointers to pass width and height to.
    w = pointer(c_long(0))
    h = pointer(c_long(0))

    # Query texture to get its width and height to use
    SDL_QueryTexture(tex, None, None, w, h)
    dst.w = w.contents.value
    dst.h = h.contents.value

    SDL_RenderCopy(ren, tex, None, dst)


def renderText(message, fontFile, color, fontSize, renderer):
    # open the font, remember to encode the fontFile for Python3
    font = TTF_OpenFont(str.encode(fontFile), fontSize)
    if not font:
        # To Do: Error checking, SDL_Destroy(*)
        SDL_Quit()
    # create text surface, encode the message to byte format
    surf = TTF_RenderText_Blended(font, str.encode(message), color)

    # create texture
    texture = SDL_CreateTextureFromSurface(renderer, surf)
    if not texture:
        # To Do: Error check for problem
        print("no texture")

    # Clean up loaded font and surface
    SDL_FreeSurface(surf)
    TTF_CloseFont(font)
    return texture