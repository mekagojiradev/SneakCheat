import pygame

WIDTH, HEIGHT = 1920, 1000



class Button():
    
    
    def __init__(self, screen: pygame.display, image: pygame.Surface,
                 image_alt: pygame.Surface = None,
                 x:int = 0, y:int = 0, scale: int=1) -> None:
        
        width = image.get_width()
        height = image.get_height()
        self.screen = screen
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.image_alt = pygame.transform.scale(image_alt, (int(width * scale), int(height * scale))) if image_alt else None
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.clicked = False
       
    def draw(self) -> bool:
        pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if self.image_alt:
                self.screen.blit(self.image_alt, (self.rect.x, self.rect.y)) 
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                return True    
                
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False       
            
    
        self.screen.blit(self.image, (self.rect.x, self.rect.y)) if not self.rect.collidepoint(pos) else None 
        return False
        
        
        
            
    