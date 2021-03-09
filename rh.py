import pygame
from pygame.locals import *

pygame.init()
pygame.font.init()

# define fps
clock = pygame.time.Clock()
fps = 60

# set up the screen parameters
screen_width = 800
screen_height = 800

# set the grid block size
# remember, the grid is 8 blocks x 8 blocks
block = 100

# set up a few game parameters
selected = None
moving = False
btn_do = ""
level = 0

# build screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Rush Hour')

# load background image
image_folder = r'C:\Users\haley\OneDrive\Documents\Haley Stuff\Python - Haley projects\Breakout\img'

# background image
bg = pygame.image.load(str(image_folder + '\\bg.png'))
bg_rect = bg.get_rect()

# home screen image
hm_img = pygame.image.load(str(image_folder + '\\home_scr.png'))
hm_rec = hm_img.get_rect()

# win image
win = pygame.image.load(str(image_folder + '\\win_text.png'))
win_rect = win.get_rect()

# button images
home_btn_img = pygame.image.load(str(image_folder + '\\home.png'))
reset_btn_img = pygame.image.load(str(image_folder + '\\reset.png'))
pick_new_img = pygame.image.load(str(image_folder + '\\pick_new.png'))
quit_img = pygame.image.load(str(image_folder + '\\quit.png'))
lev1_img = pygame.image.load(str(image_folder + '\\level1.png'))
lev2_img = pygame.image.load(str(image_folder + '\\level2.png'))
lev3_img = pygame.image.load(str(image_folder + '\\level3.png'))

# car images
blue_car_img1 = pygame.image.load(str(image_folder + '\\cars\\blue_car1.png'))
blue_car_img2 = pygame.image.load(str(image_folder + '\\cars\\blue_car2.png'))
brown_car_img1 = pygame.image.load(str(image_folder + '\\cars\\brown_car1.png'))
brown_car_img2 = pygame.image.load(str(image_folder + '\\cars\\brown_car2.png'))
green_car_img1 = pygame.image.load(str(image_folder + '\\cars\\green_car1.png'))
green_car_img2 = pygame.image.load(str(image_folder + '\\cars\\green_car2.png'))
orange_car_img = pygame.image.load(str(image_folder + '\\cars\\orange_car.png'))
pink_car_img1 = pygame.image.load(str(image_folder + '\\cars\\pink_car1.png'))
pink_car_img2 = pygame.image.load(str(image_folder + '\\cars\\pink_car2.png'))
purple_car_img1 = pygame.image.load(str(image_folder + '\\cars\\purple_car1.png'))
purple_car_img2 = pygame.image.load(str(image_folder + '\\cars\\purple_car2.png'))
red_car_img = pygame.image.load(str(image_folder + '\\cars\\red_car.png'))
yellow_car_img = pygame.image.load(str(image_folder + '\\cars\\yellow_car.png'))

# truck images
blue_truck_img = pygame.image.load(str(image_folder + '\\trucks\\blue_truck.png'))
green_truck_img = pygame.image.load(str(image_folder + '\\trucks\\green_truck.png'))
yellow_truck_img = pygame.image.load(str(image_folder + '\\trucks\\yellow_truck.png'))
pink_truck_img = pygame.image.load(str(image_folder + '\\trucks\\pink_truck.png'))
purple_truck_img = pygame.image.load(str(image_folder + '\\trucks\\purple_truck.png'))


# create car class (also includes trucks)
class car(pygame.sprite.Sprite):
    def __init__(self, x, y, img, move_dir, face_dir, player):
        pygame.sprite.Sprite.__init__(self)

        # determine which way the car is facing to properly load the image
        self.face_dir = face_dir
        if self.face_dir == "face_r":
            self.image = img
        if self.face_dir == "face_l":
            self.image = pygame.transform.flip(img, True, False)  # flip image
        if self.face_dir == "face_t":
            self.image = pygame.transform.rotate(img, 90)  # rotate -90
        if self.face_dir == "face_b":
            self.image = pygame.transform.rotate(img, -90)  # rotate +90

        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.move_dir = move_dir
        self.player = player
        self.start_x = x
        self.start_y = y

    def move(self, move_rng):
        # don't move into other cars
        # only move the car along the designated axis
        # move the car relative to where the mouse position is moving
        # don't move off the game grid

        if event.type == pygame.MOUSEMOTION:

            # move_rng = [left_limit, right_limit, top_limit, bottom_limit]
            left_limit = move_rng[0]
            right_limit = move_rng[1]
            top_limit = move_rng[2]
            bottom_limit = move_rng[3]

            if self.move_dir == "horz":
                # move along x-axis relative to mouse
                self.rect.x += event.rel[0]
                # move only within the game grid + not into other cars
                if self.rect.left < left_limit:
                    self.rect.left = left_limit
                elif self.rect.right > right_limit:
                    self.rect.right = right_limit

            if self.move_dir == "vert":
                # move along y-axis relative to mouse
                self.rect.y += event.rel[1]
                # move only within the game grid + not into other cars
                if self.rect.top < top_limit:
                    self.rect.top = top_limit
                elif self.rect.bottom > bottom_limit:
                    self.rect.bottom = bottom_limit

    def find_rng_xy(self):

        impact_r = []
        impact_l = []
        impact_t = []
        impact_b = []
        left_limit = block
        right_limit = screen_width - block
        top_limit = block
        bottom_limit = screen_height - block

        for car in car_group:
            if car is self:
                continue  # ignore the car being clicked

            # X AXIS - moving right
            # first check if the impact side is already past bumper of moving car (y-axis)
            if car.rect.left >= self.rect.right:  # impact car is located to the right / moving right

                # next, check if any of the impact car's blocks are on the same row as the moving car
                if car.rect.topleft[1] == self.rect.topright[1]:
                    impact_r.append(car.rect.topleft[0])

                if (abs(car.rect.top - car.rect.bottom) == 300):  # aka is it 3 blocks long: a truck
                    if car.rect.midleft[1] - (block // 2) == self.rect.topright[1]:
                        impact_r.append(car.rect.midleft[0])
                # print("length = " + str(abs(car.rect.right - car.rect.left)))
                # print("midleft y = " +str(car.rect.midleft[1] - (block//2)))
                # print("x limit should be = " + str(car.rect.midleft[0]))

                if (car.rect.bottomleft[1] - block) == self.rect.topright[1]:
                    impact_r.append(car.rect.bottomleft[0])

            # X AXIS - moving left
            # first check if the impact side is already past bumper of moving car (y-axis)
            if car.rect.right <= self.rect.left:  # impact car is located to the left / moving left

                # next, check if any of the impact car's blocks are on the same row as the moving car
                if car.rect.topright[1] == self.rect.topleft[1]:
                    impact_l.append(car.rect.topright[0])

                if (abs(car.rect.top - car.rect.bottom) == 300):  # aka is it 3 blocks long: a truck
                    if car.rect.midright[1] - (block // 2) == self.rect.topleft[1]:
                        impact_l.append(car.rect.midright[0])

                if (car.rect.bottomright[1] - block) == self.rect.topleft[1]:
                    impact_l.append(car.rect.bottomright[0])

            # Y AXIS - moving down
            # first check if the impact side is already past bumper of moving car (x-axis)
            if car.rect.top >= self.rect.bottom:  # impact car is located below / moving down

                # next, check if any of the impact car's blocks are on the same column as the moving car
                if car.rect.topleft[0] == self.rect.bottomleft[0]:
                    impact_b.append(car.rect.topleft[1])

                if (abs(car.rect.right - car.rect.left) == 300):  # aka is it 3 blocks long: a truck
                    if car.rect.midtop[0] - (block // 2) == self.rect.bottomleft[0]:
                        impact_b.append(car.rect.midtop[1])

                if (car.rect.topright[0] - block) == self.rect.bottomleft[0]:
                    impact_b.append(car.rect.topright[1])

            # Y AXIS - moving up
            # first check if the impact side is already past bumper of moving car (x-axis)
            if car.rect.bottom <= self.rect.top:  # impact car is located above / moving up

                # next, check if any of the impact car's blocks are on the same row as the moving car
                if car.rect.bottomleft[0] == self.rect.topleft[0]:
                    impact_t.append(car.rect.bottomleft[1])

                if (abs(car.rect.right - car.rect.left) == 300):  # aka is it 3 blocks long: a truck
                    if car.rect.midbottom[0] - (block // 2) == self.rect.topleft[0]:
                        impact_t.append(car.rect.midbottom[1])

                if (car.rect.bottomright[0] - block) == self.rect.topleft[0]:
                    impact_t.append(car.rect.bottomright[1])

        if len(impact_r) > 0:
            impact_r.sort()
            right_limit = impact_r[0]  # the smallest y = the closest the the right side

        if len(impact_l) > 0:
            impact_l.sort(reverse=True)
            left_limit = impact_l[0]  # the largest y = the closest the the left side

        if len(impact_t) > 0:
            impact_t.sort(reverse=True)
            top_limit = impact_t[0]  # the largest x = the closest the the bottom side

        if len(impact_b) > 0:
            impact_b.sort()
            bottom_limit = impact_b[0]  # the smallest x = the closest the the top side

        xy_rng = [left_limit, right_limit, top_limit, bottom_limit]

        return xy_rng

    def snap(self):
        # snap to nearest grid after done moving
        # round axis to nearest hundreds, aka nearest block
        self.rect.x = round(self.rect.x, -2)
        self.rect.y = round(self.rect.y, -2)

    def reset(self):
        self.rect.topleft = [self.start_x, self.start_y]

    def is_player(self):
        if self.player == "player":
            player = True
        else:
            player = False
        return player

    def is_win(self):
        if self.player == "player" and self.rect.right == 800:
            return True


class btn(pygame.sprite.Sprite):
    def __init__(self, x, y, img, action):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.action = action
        self.appear = appear

    def btn_action(self):
        btn_action = self.action
        return btn_action


# create sprite groups
btn_group = pygame.sprite.Group()
car_group = pygame.sprite.Group()


# load buttons into button group

def get_btn_list(appear):
    btn_list = []

    if appear == "home_scr":
        lev1_btn = btn(block + 5, (block * 6) + 5, lev1_img, "lev1")
        lev2_btn = btn((block * 3) + 5, (block * 6) + 5, lev2_img, "lev2")
        lev3_btn = btn((block * 5) + 5, (block * 6) + 5, lev3_img, "lev3")

        btn_list.append([lev1_btn, lev2_btn, lev3_btn])

    if appear == "game_scr":
        home_btn = btn(screen_width - 95, 5, home_btn_img, "home")
        reset_btn = btn(screen_width - (block + 95), 5, reset_btn_img, "reset")

        btn_list.extend([home_btn, reset_btn])

    if appear == "win_scr":
        # win is 450 px wide
        win_win_x = (bg_rect.width - win_rect.width) // 2
        win_win_y = (bg_rect.height - win_rect.height) // 2
        btn_y = win_win_y + win_rect.height - 43  # buttons are ON bottom of win pic, 40 px high, + 3 px black border

        pick_new_btn = btn(win_win_x + 3, btn_y, pick_new_img, "home")  # go home to pick new level
        reset_btn = btn(win_win_x + 263, btn_y, reset_btn_img, "reset")
        quit_btn = btn(win_win_x + 363, btn_y, quit_img, "quit")

        btn_list.extend([pick_new_btn, reset_btn, quit_btn])

    return btn_list

def update_btn_group(btn_list):
    btn_group.empty()
    for i in btn_list:
        btn_group.add(i)

# determine level
def get_level_list(level):
    level_list = []

    if level == 1:  # Beginner

        red_car = car(2 * block, 3 * block, red_car_img, "horz", "face_r", "player")
        blue_car = car(2 * block, 5 * block, blue_car_img1, "horz", "face_r", "npc")
        green_car = car(2 * block, 1 * block, green_car_img1, "horz", "face_r", "npc")
        yellow_car = car(1 * block, 5 * block, yellow_car_img, "vert", "face_t", "npc")
        blue_truck = car(4 * block, 3 * block, blue_truck_img, "vert", "face_b", "npc")
        green_truck = car(3 * block, 6 * block, green_truck_img, "horz", "face_r", "npc")
        yellow_truck = car(6 * block, 4 * block, yellow_truck_img, "vert", "face_t", "npc")
        pink_truck = car(1 * block, 1 * block, pink_truck_img, "vert", "face_b", "npc")

        level_list.extend([red_car, blue_car, green_car, yellow_car, \
                           blue_truck, green_truck, yellow_truck, pink_truck])

    if level == 2:  # Intermediate

        red_car = car(4 * block, 3 * block, red_car_img, "horz", "face_r", "player")
        blue_car2 = car(5 * block, 1 * block, blue_car_img2, "vert", "face_b", "npc")
        green_car1 = car(1 * block, 1 * block, green_car_img1, "horz", "face_r", "npc")
        orange_car = car(3 * block, 1 * block, orange_car_img, "horz", "face_r", "npc")
        pink_car1 = car(3 * block, 2 * block, pink_car_img1, "vert", "face_t", "npc")
        purple_car1 = car(2 * block, 3 * block, purple_car_img1, "vert", "face_t", "npc")
        yellow_car = car(2 * block, 6 * block, yellow_car_img, "horz", "face_r", "npc")
        green_car2 = car(4 * block, 4 * block, green_car_img2, "horz", "face_l", "npc")
        pink_car2 = car(4 * block, 5 * block, pink_car_img2, "vert", "face_t", "npc")
        blue_car1 = car(5 * block, 5 * block, blue_car_img1, "horz", "face_l", "npc")
        purple_car2 = car(5 * block, 6 * block, purple_car_img2, "horz", "face_l", "npc")
        blue_truck = car(1 * block, 4 * block, blue_truck_img, "vert", "face_b", "npc")
        yellow_truck = car(6 * block, 2 * block, yellow_truck_img, "vert", "face_t", "npc")

        level_list.extend([red_car, blue_car2, green_car1, orange_car, pink_car1, purple_car1, yellow_car, \
                            green_car2, pink_car2, blue_car1, purple_car2, blue_truck, yellow_truck])

    if level == 3:  # Expert

        red_car = car(2 * block, 3 * block, red_car_img, "horz", "face_r", "player")
        blue_car2 = car(5 * block, 2 * block, blue_car_img2, "horz", "face_l", "npc")
        green_car1 = car(1 * block, 1 * block, green_car_img1, "horz", "face_l", "npc")
        orange_car = car(4 * block, 2 * block, orange_car_img, "vert", "face_b", "npc")
        pink_car1 = car(1 * block, 3 * block, pink_car_img1, "vert", "face_t", "npc")
        purple_car1 = car(4 * block, 4 * block, purple_car_img1, "horz", "face_r", "npc")
        blue_car1 = car(1 * block, 5 * block, blue_car_img1, "horz", "face_r", "npc")
        pink_truck = car(6 * block, 3 * block, pink_truck_img, "vert", "face_b", "npc")
        yellow_truck = car(4 * block, 1 * block, yellow_truck_img, "horz", "face_r", "npc")
        green_truck = car(4 * block, 6 * block, green_truck_img, "horz", "face_l", "npc")
        purple_truck = car(3 * block, 4 * block, purple_truck_img, "vert", "face_t", "npc")

        level_list.extend([red_car, blue_car2, green_car1, orange_car, pink_car1, purple_car1, blue_car1, \
                            pink_truck, yellow_truck, green_truck, purple_truck])

    return level_list


def update_car_group(level_list):
    car_group.empty()
    for i in level_list:
        car_group.add(i)


# prep the background
def draw_bg():
    screen.blit(bg, (0, 0))


def draw_hm_scr():
    screen.blit(hm_img, (block, block))


def draw_win():
    center_x = (bg_rect.width - win_rect.width) // 2  # 800 - 450 / 2
    center_y = (bg_rect.height - win_rect.height) // 2  # 800 - 290 / 2
    screen.blit(win, (center_x, center_y))


def draw_level_text(level):
    myfont = pygame.font.SysFont('Fixedsys', 30)
    textsurface = myfont.render("LEVEL " + str(level), False, (255, 242, 0))
    screen.blit(textsurface, (50, 10))


state = "home"

# start the game!
run = True
while run:

    clock.tick(fps)

    # event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # figure out if a button was clicked
            for button in btn_group:
                if button.rect.collidepoint(pos):
                    selected = button
                    btn_do = selected.btn_action()

                    if state == "home":
                        level = 0

                        if btn_do == "lev1":
                            level = 1

                        elif btn_do == "lev2":
                            level = 2

                        elif btn_do == "lev3":
                            level = 3

                        # get cars ready
                        get_level = get_level_list(level)
                        update_car_group(get_level)

                        # put the game in motion
                        state = "game"

                    if btn_do == "reset":
                        state = "game" # included b/c we might be resetting from the win screen
                        for car in car_group:
                            car.reset()

                    if btn_do == "home":
                        state = "home"
                        level = 0

                    if btn_do == "quit":
                        run = False

        if state == "game":
            appear = "game_scr"
            print(level)

            # draw background and level text
            draw_bg()
            draw_level_text(level)

            # draw the cars determined by the level choice
            car_group.draw(screen)

            # get screen appearance, build the button group, then draw that group
            btns = get_btn_list(appear)
            update_btn_group(btns)
            btn_group.draw(screen)

            # check for when mouse is clicked down
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                is_car = False

                # figure out if a car was clicked
                for car in car_group:
                    if car.rect.collidepoint(pos):
                        selected = car
                        is_car = True
                        move_rng = selected.find_rng_xy()
                        moving = True


            elif event.type == MOUSEMOTION and moving:
                # b/c I want the player red car to be able to leave the grid if they win...
                if selected.is_player() == True and move_rng[1] == 700:
                    move_rng[1] = 800
                else:
                    selected.move(move_rng)

            elif event.type == MOUSEBUTTONUP:
                if is_car == True:
                    selected.snap()  # only need to snap car to place if it is a car
                    moving = False

                    # check if game won
                    check_win = selected.is_win()
                    if check_win == True:
                        state = "won"

        if state == "home":
            draw_bg()
            draw_hm_scr()
            appear = "home_scr"
            btns = get_btn_list(appear)
            update_btn_group(btns)
            btn_group.draw(screen)

        if state == "won":
            draw_win()
            appear = "win_scr"
            btns = get_btn_list(appear)
            update_btn_group(btns)
            btn_group.draw(screen)

    pygame.display.update()

pygame.quit()
