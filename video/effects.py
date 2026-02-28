import pygame


class Effect:
    def __init__(self, duration: int = 0): 
        self.duration = duration # 0 means infinite
        self.elapsed_time = 0

    def update(self, delta_time: int):
        self.elapsed_time += delta_time

    def is_active(self) -> bool:
        return not self.duration or self.elapsed_time < self.duration

    def apply(self, surface: pygame.Surface):
        pass


class ScanlineEffect(Effect):
    def __init__(self, duration: int = 0, speed: int = 24, offset: int = 3, colour: tuple = (255, 255, 255), alpha: int = 255, thickness: int = 2):
        super().__init__(duration)
        self.speed = speed # Pixels per second
        self.offset = offset # Amount of pixels to move frame above scanline
        self.colour = colour
        self.alpha = alpha
        self.thickness = thickness
        self._surface = None

    def apply(self, surface: pygame.Surface):
        width, height = surface.get_size()
        scanline_y = (self.elapsed_time * self.speed / 1000) % height

        # Move the part of the frame above the scanline offset pixels to the right
        if scanline_y > 0 and scanline_y < height - self.thickness / 2:
            section_height = int(scanline_y + self.thickness / 2)
            rect_to_move = pygame.Rect(0, 0, width - self.offset, section_height)

            surface.blit(surface, (self.offset, 0), rect_to_move)
            surface.fill((0, 0, 0), (0, 0, self.offset, section_height))

        # Draw the scanline
        if self._surface is None or self._surface.get_width() != width:
            self._surface = pygame.Surface((width, self.thickness), pygame.SRCALPHA)
            self._surface.fill((*self.colour, self.alpha))
            
        surface.blit(self._surface, (0, scanline_y))

class ColourShiftEffect(Effect):
    def __init__(self, duration: int = 0, red_shift: int = 2, blue_shift: int = -2):
        super().__init__(duration)
        self.red_shift = red_shift
        self.blue_shift = blue_shift
        self._surface = None
        self._red_surface = None
        self._green_surface = None
        self._blue_surface = None

    def apply(self, surface: pygame.Surface):
        width, height = surface.get_size()

        if self._surface is None or self._surface.get_size() != (width, height):
            self._surface = surface.copy()
            self._red_surface = surface.copy()
            self._green_surface = surface.copy()
            self._blue_surface = surface.copy()

        # Clear the target surface to black so we can add channels back in
        self._surface.blit(surface, (0, 0))
        surface.fill((0, 0, 0))
        
        self._red_surface.blit(self._surface, (0, 0))
        self._red_surface.fill((255, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        surface.blit(self._red_surface, (self.red_shift, 0), special_flags=pygame.BLEND_ADD)

        self._green_surface.blit(self._surface, (0, 0))
        self._green_surface.fill((0, 255, 0), special_flags=pygame.BLEND_RGBA_MULT)
        surface.blit(self._green_surface, (0, 0), special_flags=pygame.BLEND_ADD)

        self._blue_surface.blit(self._surface, (0, 0))
        self._blue_surface.fill((0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)
        surface.blit(self._blue_surface, (self.blue_shift, 0), special_flags=pygame.BLEND_ADD)