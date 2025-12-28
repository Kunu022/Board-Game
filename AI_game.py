import pygame
import math
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


DIRECTIONS = {
    "N":  (-1,  0),
    "NE": (-1,  1),
    "E":  ( 0,  1),
    "SE": ( 1,  1),
    "S":  ( 1,  0),
    "SW": ( 1, -1),
    "W":  ( 0, -1),
    "NW": (-1, -1),
}

ARROW = [
    (0, 0),
    (18, 8),
    (0, 16),
]

PIN_TYPES = [
    {"value": 3, "color": "red", "health": 3},
    {"value": 2, "color": "green", "health": 2},
    {"value": 1, "color": "blue", "health": 1},
]
PIN_TEXTURES = {
    0: None,
    1: pygame.image.load("assets/p1_rock.png").convert_alpha(),
    2: pygame.image.load("assets/p1_lily.png").convert_alpha(),
    3: pygame.image.load("assets/p1_lotus.png").convert_alpha(),
    4: pygame.image.load("assets/p2_rock.png").convert_alpha(),
    5: pygame.image.load("assets/p2_lily.png").convert_alpha(),
    6: pygame.image.load("assets/p2_lotus.png").convert_alpha(),

}
for k, img in PIN_TEXTURES.items():
    if img:
        PIN_TEXTURES[k] = pygame.transform.scale(img, CELL_SIZE)

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.surface = pygame.Surface(CELL_SIZE)
        self.surface.fill("white")
        self.rect = self.surface.get_rect()
        self.value = 0
        self.player = 0
        self.image = 0
        self.directions = set()

    def set_pin(self, value, player,directions=None):
        self.value = value
        #self.color = color

        self.image = PIN_TEXTURES[value]
        self.player = player
        self.directions = directions or set()
        #self.surface.fill(color)

    def draw(self, surface, offset_x, offset_y):
        x = offset_x + self.col * (CELL_SIZE[0] + CELL_GAP)
        y = offset_y + self.row * (CELL_SIZE[1] + CELL_GAP)
        self.rect.topleft = (x, y)
        if self.image and self.image != 0:
            surface.blit(self.image, self.rect)
        else:
            surface.blit(self.surface, self.rect)
        for d in self.directions:
            draw_arrow(surface, d, self.rect)

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

def draw_arrow(surface, direction, rect, color="yellow"):
    dr, dc = direction


    angle = -math.degrees(math.atan2(-dr, dc))

    # place arrow on edge
    margin = 10
    if dr == -1 and dc == 0:       # N
        pos = rect.midtop
    elif dr == 1 and dc == 0:      # S
        pos = rect.midbottom
    elif dr == 0 and dc == 1:      # E
        pos = rect.midright
    elif dr == 0 and dc == -1:     # W
        pos = rect.midleft
    elif dr == -1 and dc == 1:     # NE
        pos = (rect.right - margin, rect.top + margin)
    elif dr == 1 and dc == 1:      # SE
        pos = (rect.right - margin, rect.bottom - margin)
    elif dr == 1 and dc == -1:     # SW
        pos = (rect.left + margin, rect.bottom - margin)
    elif dr == -1 and dc == -1:    # NW
        pos = (rect.left + margin, rect.top + margin)

    cx, cy = pos
    arrow = [(x + cx - 9, y + cy - 8) for x, y in ARROW]
    arrow = rotate_points(arrow, angle, (cx, cy))

    pygame.draw.polygon(surface, color, arrow)

def rotate_points(points, angle_deg, center):
    angle = math.radians(angle_deg)
    cx, cy = center
    rotated = []

    for x, y in points:
        x -= cx
        y -= cy
        rx = x * math.cos(angle) - y * math.sin(angle)
        ry = x * math.sin(angle) + y * math.cos(angle)
        rotated.append((rx + cx, ry + cy))

    return rotated
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

#checking if a move is legal
def move_check(row1,col1,row2,col2):
    print("destination:", row2, " ", col2)
    if row1 == row2 and col1 == col2:
        return False
    else:
        if row1 == row2:
            for cell in cells:
                if col1 > col2 and cell.row == row1:
                    if col2 <= cell.col < col1 and cell.value != 0:
                        print("bitch get out the way1")
                        return False
                elif col1 < col2 and cell.row == row1:
                    if col1 < cell.col <= col2 and cell.value != 0:
                        print("bitch get out the way2")
                        return False

            return True
        elif col1 == col2:
            for cell in cells:
                if row1 > row2 and cell.col == col1:
                    if row2 <= cell.row < row1 and cell.value != 0:
                        print("bitch get out the way1")
                        return False
                elif row1 < row2 and cell.col == col1:
                    if row1 < cell.row <= row2 and cell.value != 0:
                        print("bitch get out the way2")
                        return False
            return True
        elif abs(row2 - row1) == abs(col2 - col1):
            print("diagonal")
            for cell in cells:
                if row1 > row2 and col1 > col2:
                    if row2 <= cell.row < row1 and col2 <= cell.col < col1 and cell.value != 0:
                        print("bitch get out the way1")
                        return False
                elif row1 > row2 and col1 < col2:
                    if row2 <= cell.row < row1 and col1 < cell.col <= col2 and cell.value != 0:
                        print("bitch get out the way2")
                        return False
                elif row1 < row2 and col1 > col2:
                    if row1 < cell.row <= row2 and col2 <= cell.col < col1 and cell.value != 0:
                        print("bitch get out the way3")
                        return False
                elif row1 < row2 and col1 < col2:
                    if row1 < cell.row <= row2 and col1 < cell.col <= col2 and cell.value != 0:
                        if row2 <= cell.row < row1 and col2 <= cell.col < col1 and cell.value != 0:
                            print("bitch get out the way4")
                            return False
            return True
    print("incorrect move")
    return False

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
                                cell.set_pin(selected_pin.value, turn,{DIRECTIONS["NW"],DIRECTIONS["NE"]})
                                pin_counts_p1[selected_pin.value] -= 1
                                print(selected_pin.color, pin_counts_p1[selected_pin.value])
                                end_turn()
                            elif turn == 1 and cell.row <= 1 :
                                cell.set_pin(selected_pin.value + 3, turn,{DIRECTIONS["SE"],DIRECTIONS["SW"]})
                                pin_counts_p2[selected_pin.value] -= 1
                                cell.player = 1
                                print(selected_pin.color, pin_counts_p2[selected_pin.value])
                                end_turn()
                            break
                #moving a pin
                else:
                    for cell in cells:
                        if cell.rect.collidepoint(mouse_pos) and cell.value != 0 and cell.player == turn:
                            moving_pin = (cell.value, cell.player,cell.directions,cell.row, cell.col)
                            print("moving: ", moving_pin)
                            break
                        elif cell.rect.collidepoint(mouse_pos) and cell.value == 0 and moving_pin is not None:
                            if not move_check(moving_pin[3],moving_pin[4],cell.row,cell.col):
                                break
                            cell.set_pin(moving_pin[0], moving_pin[1],moving_pin[2])
                            for cell in cells:
                                if cell.row == moving_pin[3] and cell.col == moving_pin[4]:
                                    cell.set_pin(0, None,None)
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
