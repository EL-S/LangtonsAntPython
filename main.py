import pygame


def init():
    pygame.init()
    
    info = pygame.display.Info()
    
    screen_width, screen_height = info.current_w, info.current_h

    grid_w, grid_h, grid_pixel_size, current_z = adjust_zoom()

    screen_surface = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

    hist_grid = {}

    ant_position = [0, 0]
    ant_direction = 0  # 0 north, 1 east, 2 south, 3 west

    screen_surface.fill((255, 255, 255))

    pygame.display.update()
    return screen_surface, grid_w, grid_h, hist_grid, ant_position, ant_direction, grid_pixel_size, current_z


def adjust_zoom(current_z=None, direction=None):

    info = pygame.display.Info()
    
    screen_width, screen_height = info.current_w, info.current_h

    potential_grid_sizes = get_grid_sizes(screen_width, screen_height)

    if current_z == None:
        current_z = round((len(potential_grid_sizes) - 1) / 2)
    else:
        if direction == 'in':
            current_z -= 1
        elif direction == 'out':
            current_z += 1
        if current_z < 0:
            current_z = 0
        elif current_z > (len(potential_grid_sizes) - 1):
            current_z = (len(potential_grid_sizes) - 1)
    grid_pixel_size = potential_grid_sizes[current_z]  # median value, 1080p is size 12
    grid_w = int(screen_width / grid_pixel_size)
    grid_h = int(screen_height / grid_pixel_size)
    return grid_w, grid_h, grid_pixel_size, current_z


def get_grid_sizes(pixel_width, pixel_height):
    pixel_width_factors = []
    pixel_height_factors = []
    common_factors = []

    for i in range(1, round((pixel_width)**(1/2))):
        for j in range(round((pixel_width)**(1/2)), pixel_width + 1):
            if i * j == pixel_width:
                pixel_width_factors.append(i)
                pixel_width_factors.append(j)

    for i in range(1, round((pixel_height)**(1/2))):
        for j in range(round((pixel_height)**(1/2)), pixel_height + 1):
            if i * j == pixel_height:
                pixel_height_factors.append(i)
                pixel_height_factors.append(j)

    for factor in pixel_height_factors:
        if factor in pixel_width_factors:
            common_factors.append(factor)

    common_factors.sort()
    return common_factors


def check_ant(grid, pos):
    try:
        value = grid[(pos[0], pos[1])]
    except KeyError:
        value = 0
    # check position tile
    # white is 0
    # black is 1
    # return a value to determine movement
    return value


def orient_ant(orientation, value):
    # if tile is 0 (white), turn clockwise
    # if tile is 1 (black), turn anti-clockwise
    if value == 0:
        orientation += 1  # clockwise
    else:
        orientation -= 1  # anti-clockwise
    if orientation < 0:  # wrap the value
        orientation = 3
    elif orientation > 3:  # wrap the value
        orientation = 0
    return orientation


def move_ant(pos, orientation):
    # move the ant forwards based on its orientation

    prev_pos = pos

    if orientation == 0:
        pos[1] -= 1  # moves up 1 north
    elif orientation == 1:
        pos[0] += 1  # moves right 1 east
    elif orientation == 2:
        pos[1] += 1  # moves down 1 south
    elif orientation == 3:
        pos[0] -= 1  # moves left 1 west
    return pos, prev_pos


def update_grid(grid, prev_pos):
    # update the grid history to
    # black if it went clockwise
    # white if it went anti-clockwise
    # you could probably just set the value to opposite of what it was too but-
    # that won't work for multi-states
    try:
        grid[(prev_pos[0], prev_pos[1])]  # if it doesn't trigger a value error it deletes the value
        del grid[(prev_pos[0], prev_pos[1])]  # delete the value to make it a white tile, probably call a draw function
    except KeyError:
        grid[(prev_pos[0], prev_pos[1])] = 1  # set the tile to black because it didn't exist, which implies it is white
    return grid


def render_graphics(screen_surface, grid, pos, grid_pixel_size, grid_w, grid_h):
    screen.fill((255, 255, 255))  # probably not
    for cell_pos, cell_value in grid.items():
        cell_colour = (0, 0, 0)
        draw_cell(screen_surface, cell_pos[0], cell_pos[1], cell_colour, grid_w, grid_h, grid_pixel_size)
    draw_ant(screen_surface, pos, grid_w, grid_h, grid_pixel_size)
    draw_grid(screen_surface, grid_pixel_size, grid_w, grid_h)
    pygame.display.update()  # Only update the affected cells, do a full update when scrolling

    
def draw_grid(screen_surface, grid_pixel_size, grid_w, grid_h):  # fine
    colour = (0, 0, 0)
    # print(screen_surface, grid_pixel_size, grid_w, grid_h)
    for cell_x in range(0, grid_w):  # think of a better automatic method
        pixel_offset_x_start = (cell_x * grid_pixel_size)  # +(grid_w * grid_pixel_size)
        pixel_offset_y_start = 0
        pixel_offset_x_end = (cell_x * grid_pixel_size)  # + (grid_w * grid_pixel_size)
        pixel_offset_y_end = grid_h * grid_pixel_size

        start_pos = (pixel_offset_x_start, pixel_offset_y_start)
        end_pos = (pixel_offset_x_end, pixel_offset_y_end)
        pygame.draw.line(screen_surface, colour, start_pos, end_pos)
    for cell_y in range(0, grid_h):
        pixel_offset_x_start = 0
        pixel_offset_y_start = (cell_y * grid_pixel_size)  # +(grid_h * grid_pixel_size)
        pixel_offset_x_end = grid_w * grid_pixel_size
        pixel_offset_y_end = (cell_y * grid_pixel_size)  # + (grid_h * grid_pixel_size)

        start_pos = (pixel_offset_x_start, pixel_offset_y_start)
        end_pos = (pixel_offset_x_end, pixel_offset_y_end)
        pygame.draw.line(screen_surface, colour, start_pos, end_pos)
    return


def draw_cell(screen_surface, cell_x, cell_y, colour, grid_w, grid_h, grid_pixel_size):
    # cell_x goes from negative to positive with 0 being in the middle of the screen
    # cell_y goes from negative to positive with 0 being in the middle of the screen
    # take a cell x and a cell y and a state, then draw it
    pixel_offset_x_start = (cell_x * grid_pixel_size) + int((grid_w * grid_pixel_size) / 2)
    pixel_offset_y_start = (cell_y * grid_pixel_size) + int((grid_h * grid_pixel_size) / 2)
    pixel_offset_width = grid_pixel_size
    pixel_offset_height = grid_pixel_size
    
    points = (pixel_offset_x_start, pixel_offset_y_start, pixel_offset_width, pixel_offset_height)

    pygame.draw.rect(screen_surface, colour, points)
    return


def draw_ant(screen_surface, pos, grid_w, grid_h, grid_pixel_size):
    ant_colour = (255, 0, 0)
    ant_x = pos[0]
    ant_y = pos[1]
    draw_cell(screen_surface, ant_x, ant_y, ant_colour, grid_w, grid_h, grid_pixel_size)
    return


screen, grid_width, grid_height, history_grid, ant_pos, ant_orientation, grid_size, current_zoom = init()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                grid_width, grid_height, grid_size, current_zoom = adjust_zoom(current_zoom, 'out')
            elif event.button == 5:
                grid_width, grid_height, grid_size, current_zoom = adjust_zoom(current_zoom, 'in')
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                
    tile_value = check_ant(history_grid, ant_pos)
    ant_orientation = orient_ant(ant_orientation, tile_value)
    ant_pos, ant_prev_pos = move_ant(ant_pos, ant_orientation)
    history_grid = update_grid(history_grid, ant_prev_pos)
    render_graphics(screen, history_grid, ant_pos, grid_size, grid_width, grid_height)

pygame.quit()
