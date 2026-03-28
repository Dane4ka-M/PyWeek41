import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        super().__init__()

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.rect = pygame.Rect(x, y, width, height)
        
        if not image:
            image = pygame.Surface((0, 0))
            
        self.image = image



    def draw(self, screen, camera):
        screen.blit(self.image, (0, 0))