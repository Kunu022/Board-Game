import pygame
pygame.init()
screen = pygame.display.set_mode((1000, 720), pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.display.set_caption("game")
CELL_SIZE = (100, 100)
CELL_GAP = 10
GRID_ROWS = 6
GRID_COLS = 6
PIN_SIZE = (60, 60)
PIN_MARGIN = 20

PIN_TYPES = [
    {"value": 1, "color": "red"},
    {"value": 2, "color": "green"},
    {"value": 3, "color": "blue"},
]


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.surface = pygame.Surface(CELL_SIZE)
        self.surface.fill("white")
        self.rect = self.surface.get_rect()
    def set_pin(self, value, color):
        self.value = value
        self.color = color
        self.surface.fill(color)

    def draw(self, surface, offset_x, offset_y):
        x = offset_x + self.col * (CELL_SIZE[0] + CELL_GAP)
        y = offset_y + self.row * (CELL_SIZE[1] + CELL_GAP)
        self.rect.topleft = (x, y)
        surface.blit(self.surface, self.rect)

cells = []
for i in range(GRID_ROWS):
    for j in range(GRID_COLS):
        cells.append(Cell(i, j))

def get_grid_offset(screen_width, screen_height):
    grid_width = GRID_COLS * CELL_SIZE[0] + (GRID_COLS - 1) * CELL_GAP
    grid_height = GRID_ROWS * CELL_SIZE[1] + (GRID_ROWS - 1) * CELL_GAP

    offset_x = (screen_width - grid_width) // 2
    offset_y = (screen_height - grid_height) // 2

    return offset_x, offset_y

class PinSelector:
    def __init__(self, x, y, size, value, color):
        self.value = value
        self.color = color
        self.surface = pygame.Surface(size)
        self.surface.fill(color)
        self.rect = self.surface.get_rect(topleft=(x, y))
        self.selected = False

    def draw(self, surface):
        surface.blit(self.surface, self.rect)
        if self.selected:
            pygame.draw.rect(surface, "yellow", self.rect, 4)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

pin_selectors = []
start_x = 20
start_y = 100

for i, pin in enumerate(PIN_TYPES):
    pin_selectors.append(
        PinSelector(
            start_x,
            start_y + i * (PIN_SIZE[1] + PIN_MARGIN),
            PIN_SIZE,
            pin["value"],
            pin["color"],
        )
    )

selected_pin = None

running = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for pin in pin_selectors:
                if pin.is_clicked(mouse_pos):
                    selected_pin = pin
                    for p in pin_selectors:
                        p.selected = False
                    pin.selected = True
                    break
            else:
                if selected_pin:
                    for cell in cells:
                        if cell.rect.collidepoint(mouse_pos):
                            cell.set_pin(selected_pin.value, selected_pin.color)
                            break
    screen.fill("black")
    #pin buttons
    for pin in pin_selectors:
        pin.draw(screen)
    #cells
    offset_x, offset_y = get_grid_offset(*screen.get_size())
    for cell in cells:
        cell.draw(screen, offset_x, offset_y)
        
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
