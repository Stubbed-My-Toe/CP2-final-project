import pygame
import pymunk
import pymunk.pygame_util
import random
import helper_1
import theme_1 as T




MULTIPLIERS = [50, 4, 3, 0.8, 0.3, 0.8, 3, 4, 50]
LAYERS      = 8
SPACING     = 110
START_X     = None   # set at runtime based on screen width
START_Y     = 160
CHIP_R      = 14




def _bucket_color(mult):
    if mult >= 10:
        return T.GOLD
    if mult >= 1:
        return T.WIN_GREEN
    return (100, 100, 120)




def _peg_color(col):
    return T.ACCENT_DIM




def plinko_main(win, username, password, file: helper_1.csv_file):
    W, H = win.get_size()
    data  = helper_1.csv_get_data(file, {"username": username, "password": password})
    cash  = float(data["cash"])


    global START_X
    START_X = W // 2


    bet_bar  = T.BetBar(START_X, H - 100, min_bet=1, default=10, step=5)
    btn_drop = T.Button("Drop Chip", (START_X - 80, H - 58, 160, 44),
                        color=T.ACCENT, hover_color=T.ACCENT_DIM,
                        text_color=T.BG, hover_text=T.BG, bold=True)
    btn_back = T.make_back_button()
    banner   = T.Banner()


    # ── Physics ──────────────────────────────────────────────────────────────
    space         = pymunk.Space()
    space.gravity = (0, 500)


    dropped = False
    chips   = []
    chip_data = []  # (shape, bet_value)


    # pegs
    pegs = []
    for row in range(LAYERS):
        for col in range(row + 1):
            px = int(START_X + (col - row / 2) * SPACING)
            py = int(START_Y + row * SPACING)
            body = space.static_body
            c    = pymunk.Circle(body, 8, (px, py))
            c.elasticity = 0.3
            c.friction   = 0.5
            c.collision_type = 3
            space.add(c)
            pegs.append((px, py))


    # bucket floors
    bottom_y  = START_Y + LAYERS * SPACING
    bucket_shapes = []
    num_buckets = LAYERS + 1
    for i in range(num_buckets):
        bx = int(START_X + (i - num_buckets / 2 + 0.5) * SPACING)
        seg = pymunk.Segment(space.static_body,
                              (bx - SPACING // 2, bottom_y),
                              (bx + SPACING // 2, bottom_y), 4)
        seg.collision_type  = 2
        seg.multiplier      = MULTIPLIERS[i]
        seg.elasticity      = 0
        seg.friction        = 1
        space.add(seg)
        bucket_shapes.append((bx, bottom_y, SPACING, seg))


    # walls
    for bx in (START_X - (num_buckets // 2 + 1) * SPACING,
               START_X + (num_buckets // 2 + 1) * SPACING):
        wall = pymunk.Segment(space.static_body, (bx, START_Y - 30), (bx, bottom_y + 40), 4)
        wall.elasticity = 0.5
        space.add(wall)


    # collision handler: chip hits bucket
    game_state = {'cash': cash, 'last_win': None, 'dropped': False}


    def on_bucket(arbiter, space, data_arg):
        chip_shape  = arbiter.shapes[0]
        bucket_seg  = arbiter.shapes[1]
        if not hasattr(chip_shape, 'bet_val'):
            return False
        mult   = bucket_seg.multiplier
        gain   = round(chip_shape.bet_val * mult, 2)
        game_state['cash'] += gain
        game_state['last_win'] = gain
        game_state['dropped']  = False
        space.add_post_step_callback(
            lambda s, sh: s.remove(sh, sh.body), chip_shape
        )
        return False


    handler = space.add_collision_handler(1, 2)
    handler.begin = on_bucket
    handler.data  = game_state


    clock   = pygame.time.Clock()
    running = True
    while running:
        cash = game_state['cash']
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                running = False
            if btn_back.is_clicked(e):
                file.update_row(
                    {"username": username, "password": password},
                    {"cash": game_state['cash'],
                     "times_played_plinko": int(data["times_played_plinko"]) + 1}
                )
                return


            bet_bar.handle(e, cash)


            if btn_drop.is_clicked(e) and not game_state['dropped']:
                bet = bet_bar.value
                if bet > cash:
                    banner.show("Insufficient funds", T.LOSE_RED)
                else:
                    game_state['cash'] -= bet
                    game_state['dropped'] = True
                    # spawn chip
                    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, CHIP_R))
                    body.position = (START_X + random.uniform(-8, 8), START_Y - 20)
                    chip = pymunk.Circle(body, CHIP_R)
                    chip.collision_type = 1
                    chip.elasticity = 0.3
                    chip.friction   = 0.4
                    chip.bet_val    = bet
                    space.add(body, chip)
                    chips.append(chip)
                    file.update_row(
                        {"username": username, "password": password},
                        {"cash": game_state['cash']}
                    )


        # show win notification
        if game_state['last_win'] is not None:
            gain = game_state['last_win']
            if gain > 0:
                banner.show(f"+${gain:.2f}", T.WIN_GREEN)
            else:
                banner.show(f"0 — nothing", T.TEXT_DIM)
            game_state['last_win'] = None
            file.update_row(
                {"username": username, "password": password},
                {"cash": game_state['cash']}
            )


        # step physics
        for _ in range(6):
            space.step(1 / 360)


        # ── Draw ──────────────────────────────────────────────────────────────
        win.fill(T.BG)
        T.draw_logo_corner(win)
        T.draw_hud(win, game_state['cash'], username)
        btn_back.draw(win)


        T.draw_text(win, "PLINKO", 48, T.TEXT, START_X, 50, anchor="midtop", bold=True)


        # draw pegs
        for px, py in pegs:
            pygame.draw.circle(win, T.ACCENT, (px, py), 8)
            pygame.draw.circle(win, T.BG,     (px, py), 4)


        # draw buckets
        for i, (bx, by, sw, seg) in enumerate(bucket_shapes):
            mult  = MULTIPLIERS[i]
            col   = _bucket_color(mult)
            r     = pygame.Rect(bx - SPACING // 2 + 3, by, SPACING - 6, 34)
            T.draw_rrect(win, T.PANEL_LITE, r, radius=6, border=1, border_color=col)
            label = f"x{mult}" if mult >= 1 else f"x{mult:.1f}"
            T.draw_text(win, label, 14, col,
                        r.centerx, r.centery, anchor="center", bold=True)


        # draw chips
        for chip in chips:
            if chip.body in space.bodies:
                pos = chip.body.position
                pygame.draw.circle(win, T.GOLD, (int(pos.x), int(pos.y)), CHIP_R)
                pygame.draw.circle(win, T.BG,   (int(pos.x), int(pos.y)), CHIP_R - 5)


        # HUD strip
        hud = pygame.Rect(START_X - 300, H - 130, 600, 100)
        T.draw_rrect(win, T.PANEL, hud, radius=12, border=1, border_color=T.BORDER)
        bet_bar.draw(win)
        btn_drop.draw(win)


        banner.update_draw(win)
        pygame.display.flip()
        clock.tick(60)
