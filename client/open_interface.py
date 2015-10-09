#!/usr/bin/env python3

import sys
import ctypes
from sdl2 import *

def demo():
	SDL_Init(SDL_INIT_VIDEO)
	window = SDL_CreateWindow(b"Hello Mine",
		SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
		592, 460, SDL_WINDOW_SHOWN)
	windowsurface = SDL_GetWindowSurface(window)

	running = True
	event  = SDL_Event()
	while running:
		while SDL_PollEvent(ctypes.byref(event)) != 0:
			if event.type == SDL_QUIT:
				running = False
				break

	SDL_DestroyWindow(window)
	SDL_Quit()
	return 0



if __name__ == "__main__":
	demo()
