import pygame
import pymunk
import random
import helper_1
import theme_1 as T

# ── Constants ────────────────────────────────────────────────────────────────
MULTIPLIERS = [50, 4, 3, 0.8, 0.3, 0.8, 3, 4, 50]
LAYERS      = 8
SPACING     = 110
START_Y     = 160
CHIP_R      = 14


def _bucket_color(mult):
    if mult >= 10:
        return T.GOLD
    if mult >= 1:
        return T.WIN_GREEN
    return (100, 100, 120)


def plinko_main(win, username, password, file: helper_1.csv_file):
    W, H = win.get_size()
    data  = helper_1.csv_get_data(file, {"username": username, "password": password})
    cash  = float(data["cash"])

    START_X = W // 2

    bet_bar  = T.BetBar(START_X, H - 100, min_bet=1, default=10, step=5)
    btn_drop = T.Button("Drop Chip", (START_X - 80, H - 58, 160, 44),
                        color=T.ACCENT, hover_color=T.ACCENT_DIM,
                        text_color=T.BG, hover_text=T.BG, bold=True)
    btn_back = T.make_back_button()
    banner   = T.Banner()

    # ── Physics setup ────────────────────────────────────────────────────────
    space         = pymunk.Space()
    space.gravity = (0, 500)

    # Active chips list — only shapes still in space.shapes
    chips = []   # list of pymunk.Circle (chip shapes)

    # Pegs
    pegs = []
    for row in range(LAYERS):
        for col in range(row + 1):
            px = int(START_X + (col - row / 2) * SPACING)
            py = int(START_Y + row * SPACING)
            c  = pymunk.Circle(space.static_body, 8, (px, py))
            c.elasticity     = 0.3
            c.friction       = 0.5
            c.collision_type = 3
            space.add(c)
            pegs.append((px, py))

    # Bucket floors + vertical dividers
    bottom_y    = START_Y + LAYERS * SPACING
    num_buckets = LAYERS + 1
    bucket_info = []   # (center_x, bottom_y, spacing, multiplier)

    for i in range(num_buckets):
        bx  = int(START_X + (i - num_buckets / 2 + 0.5) * SPACING)
        seg = pymunk.Segment(
            space.static_body,
            (bx - SPACING // 2, bottom_y),
            (bx + SPACING // 2, bottom_y), 4
        )
        seg.collision_type = 2
        seg.multiplier     = MULTIPLIERS[i]
        seg.elasticity     = 0.0
        seg.friction       = 1.0
        space.add(seg)
        bucket_info.append((bx, bottom_y, SPACING, MULTIPLIERS[i]))

    # Vertical dividers between buckets (stops chips clipping through gaps)
    for i in range(num_buckets + 1):
        dx   = int(START_X + (i - num_buckets / 2) * SPACING)
        wall = pymunk.Segment(
            space.static_body,
            (dx, bottom_y - 50),
            (dx, bottom_y + 40), 3
        )
        wall.elasticity = 0.1
        wall.friction   = 0.8
        space.add(wall)

    # Outer walls
    for wx in (START_X - (num_buckets // 2 + 1) * SPACING,
               START_X + (num_buckets // 2 + 1) * SPACING):
        wall = pymunk.Segment(
            space.static_body,
            (wx, START_Y - 30),
            (wx, bottom_y + 40), 4
        )
        wall.elasticity = 0.5
        space.add(wall)

    # ── Game state ───────────────────────────────────────────────────────────
    game_state = {
        "cash":     cash,
        "last_win": None,
    }

    # ── Collision handler: chip (type 1) hits bucket floor (type 2) ──────────
    # pymunk 7.x uses space.on_collision() instead of add_collision_handler()
    def on_bucket_begin(arbiter, sp, data_arg):
        shapes = arbiter.shapes

        # Identify which shape is the chip and which is the bucket floor
        chip_shape   = None
        bucket_shape = None
        for s in shapes:
            if hasattr(s, "bet_val"):
                chip_shape = s
            if hasattr(s, "multiplier"):
                bucket_shape = s

        if chip_shape is None or bucket_shape is None:
            return

        mult = bucket_shape.multiplier
        gain = round(chip_shape.bet_val * mult, 2)
        game_state["cash"]    += gain
        game_state["last_win"] = gain

        # Schedule removal — never mutate space during a step
        def _remove(sp, sh):
            if sh in sp.shapes:
                sp.remove(sh, sh.body)
            if sh in chips:
                chips.remove(sh)

        sp.add_post_step_callback(_remove, chip_shape)

    space.on_collision(1, 2, begin=on_bucket_begin)

    clock   = pygame.time.Clock()
    running = True

    while running:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                running = False

            if btn_back.is_clicked(e):
                file.update_row(
                    {"username": username, "password": password},
                    {
                        "cash":               game_state["cash"],
                        "times_played_plinko": int(data["times_played_plinko"]) + 1,
                    }
                )
                return

            bet_bar.handle(e, game_state["cash"])

            if btn_drop.is_clicked(e):
                bet = bet_bar.value
                if bet > game_state["cash"]:
                    banner.show("Insufficient funds", T.LOSE_RED)
                else:
                    game_state["cash"] -= bet

                    # Spawn chip body
                    mass   = 1
                    moment = pymunk.moment_for_circle(mass, 0, CHIP_R)
                    body   = pymunk.Body(mass, moment)
                    body.position = (START_X + random.uniform(-8, 8), START_Y - 20)

                    chip              = pymunk.Circle(body, CHIP_R)
                    chip.collision_type = 1
                    chip.elasticity   = 0.3
                    chip.friction     = 0.4
                    chip.bet_val      = bet   # store bet on the shape

                    space.add(body, chip)
                    chips.append(chip)

                    # Persist deducted cash immediately
                    file.update_row(
                        {"username": username, "password": password},
                        {"cash": game_state["cash"]}
                    )

        # Show win banner when a chip lands
        if game_state["last_win"] is not None:
            gain = game_state["last_win"]
            if gain > 0:
                banner.show(f"+${gain:.2f}", T.WIN_GREEN)
            else:
                banner.show("x0 — nothing", T.TEXT_DIM)
            game_state["last_win"] = None
            file.update_row(
                {"username": username, "password": password},
                {"cash": game_state["cash"]}
            )

        # Step physics (sub-steps for accuracy)
        for _ in range(6):
            space.step(1 / 360)

        # ── Draw ─────────────────────────────────────────────────────────────
        win.fill(T.BG)
        T.draw_logo_corner(win)
        T.draw_hud(win, game_state["cash"], username)
        btn_back.draw(win)

        T.draw_text(win, "PLINKO", 48, T.TEXT, START_X, 50, anchor="midtop", bold=True)

        # Pegs
        for px, py in pegs:
            pygame.draw.circle(win, T.ACCENT, (px, py), 8)
            pygame.draw.circle(win, T.BG,     (px, py), 4)

        # Buckets
        for i, (bx, by, sw, mult) in enumerate(bucket_info):
            col = _bucket_color(mult)
            r   = pygame.Rect(bx - SPACING // 2 + 3, by, SPACING - 6, 34)
            T.draw_rrect(win, T.PANEL_LITE, r, radius=6,
                         border=1, border_color=col)
            label = f"x{mult}" if mult >= 1 else f"x{mult:.1f}"
            T.draw_text(win, label, 14, col,
                        r.centerx, r.centery, anchor="center", bold=True)

        # Chips — only draw shapes still present in the space
        for chip in list(chips):
            if chip in space.shapes:
                pos = chip.body.position
                pygame.draw.circle(win, T.GOLD,
                                   (int(pos.x), int(pos.y)), CHIP_R)
                pygame.draw.circle(win, T.BG,
                                   (int(pos.x), int(pos.y)), CHIP_R - 5)

        # HUD strip
        hud = pygame.Rect(START_X - 300, H - 130, 600, 100)
        T.draw_rrect(win, T.PANEL, hud, radius=12,
                     border=1, border_color=T.BORDER)
        bet_bar.draw(win)
        btn_drop.draw(win)

        banner.update_draw(win)
        pygame.display.flip()
        clock.tick(60)
