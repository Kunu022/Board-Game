import pygame
pygame.init()
screen = pygame.display.set_mode((1000, 720), pygame.RESIZABLE)
pygame.display.set_caption("game")
CELL_SIZE = (50, 50)
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = CELL_SIZE
        self.value = 0
        self.surface = pygame.Surface(CELL_SIZE)
        self.surface.fill("white")
        self.rect = self.surface.get_rect(topleft=(x, y))
        self.color = "white"


    def draw(self,surface):
        surface.blit(self.surface,self.rect)

cells = []
for i in range(6):
    for j in range(6):
        cells.append(Cell(j * (CELL_SIZE[0] + 10), i * (CELL_SIZE[1] + 10)))



running = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    for cell in cells:
        cell.draw(screen)
        
    pygame.display.flip()
pygame.quit()
