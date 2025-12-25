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
    {"value": 3, "color": "red", "health": 3},
    {"value": 2, "color": "green", "health": 2},
    {"value": 1, "color": "blue", "health": 1},
]


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.surface = pygame.Surface(CELL_SIZE)
        self.surface.fill("white")
        self.rect = self.surface.get_rect()
        self.value = 0
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

def end_turn():
    global selected_pin,turn,pin_counts_p1,pin_counts_p2,pin_counts

    for pin in pin_selectors:
        if selected_pin is pin:
            pin.selected = False
    selected_pin = None
    turn = turn ^ 1
    if turn == 0:
        pin_counts = pin_counts_p1
    else:
        pin_counts = pin_counts_p2

class PinSelector:
    def __init__(self, x, y, size, value, color,health):
        self.value = value
        self.color = color
        self.health = health
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
            pin["health"],
        )
    )

#player turns
turn = 1  # 0 is player, 1 is AI
turn_counter = 0
#pins
selected_pin = None
moving_pin = None

pin_counts = [0,0,0,0]
pin_counts_p1 = [0,3,3,2]
pin_counts_p2 = [0,3,3,2]

# pin_rock = 3
# pin_lily = 3
# pin_lotus = 2
end_turn()
running = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #left click
            mouse_pos = event.pos
            #selecting the pin to place
            for pin in pin_selectors:
                if pin.is_clicked(mouse_pos) and selected_pin is not pin and pin_counts[pin.value] != 0:
                    print("selecting pin:" , pin.color, " ", pin.health)
                    selected_pin = pin
                    for p in pin_selectors:
                        p.selected = False
                    pin.selected = True
                    break
                elif pin.is_clicked(mouse_pos) and selected_pin is  pin:
                    selected_pin = None
                    pin.selected = False
                    break
            #clicking the board
            else:
                #placing a pin
                if selected_pin and not moving_pin:
                    for cell in cells:
                        if cell.rect.collidepoint(mouse_pos) and cell.value == 0:
                            if turn == 0 and cell.row >= GRID_ROWS - 2:
                                cell.set_pin(selected_pin.value, selected_pin.color)
                                pin_counts_p1[selected_pin.value] -= 1
                                print(selected_pin.color, pin_counts_p1[selected_pin.value])
                                end_turn()
                            elif turn == 1 and cell.row <= 1 :
                                cell.set_pin(selected_pin.value, selected_pin.color)
                                pin_counts_p2[selected_pin.value] -= 1
                                print(selected_pin.color, pin_counts_p2[selected_pin.value])
                                end_turn()
                            break
                #moving a pin
                else:
                    for cell in cells:
                        if cell.rect.collidepoint(mouse_pos) and cell.value != 0:
                            moving_pin = (cell.value, cell.color,cell.row, cell.col)
                            break
                        elif cell.rect.collidepoint(mouse_pos) and cell.value == 0 and moving_pin is not None:
                            cell.set_pin(moving_pin[0], moving_pin[1])
                            for cell in cells:
                                if cell.row == moving_pin[2] and cell.col == moving_pin[3]:
                                    cell.set_pin(0, "white")
                            moving_pin = None
                            end_turn()



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
