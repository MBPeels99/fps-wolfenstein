from settings import *
import pygame as pg
import math

class Player:

    def __init__(self, game):
        # Initialize the player with the game context and default settings.
        self.game = game  # Reference to the main game object.
        self.X, self.y = PLAYER_POS  # Player's starting position.
        self.angle = PLAYER_ANGLE  # Player's starting angle.
        self.shot = False  # Flag to indicate if the player has shot.
        self.health = PLAYER_MAX_HEALTH  # Player's health.
        self.rel = 0  # Relative mouse movement.
        self.health_recovery_delay = 700  # Delay in milliseconds for health recovery.
        self.time_prev = pg.time.get_ticks()  # Timestamp for the last health recovery.
        # Correction factor for diagonal movement speed.
        self.diag_move_corr = 1 / math.sqrt(2)

    def recover_health(self):
        # Increment player's health at regular intervals if below maximum.
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def check_health_recovery_delay(self):
        # Check if the required delay has passed for health recovery.
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True

    def check_game_over(self):
        # Check if player's health is depleted and reset the game if so.
        if self.health < 1:
            self.game.object_renderer.game_over()  # Trigger game over sequence.
            pg.display.flip()
            pg.time.delay(1500)  # Short delay before restarting.
            self.game.new_game()  # Restart the game.

    def get_damage(self, damage):
        # Reduce player's health by the given damage amount.
        self.health -= damage
        self.game.object_renderer.player_damage()  # Visual effect for damage.
        self.game.sound.player_pain.play()  # Play pain sound.
        self.check_game_over()  # Check for game over condition.
    
    def single_fire_event(self,event):
        # Handle single fire events like shooting.
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.game.sound.shotgun.play()  # Play gunshot sound.
                self.shot = True  # Set shot flag.
                self.game.weapon.reloading = True  # Set weapon reloading flag.

    def movement(self):
        # Handle player movement based on key presses.
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0  # Delta changes in x and y.
        speed = PLAYER_SPEED * self.game.delta_time  # Movement speed adjusted for delta time.
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        num_key_pressed = -1
        # Movement logic for different keys (W, A, S, D).
        if keys[pg.K_w]:
            num_key_pressed += 1
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            num_key_pressed += 1
            dx -= speed_cos
            dy -= speed_sin
        if keys[pg.K_a]:
            num_key_pressed += 1
            dx += speed_sin
            dy -= speed_cos
        if keys[pg.K_d]:
            num_key_pressed += 1
            dx -= speed_sin
            dy += speed_cos

        # Apply diagonal movement correction.
        if num_key_pressed:
            dx *= self.diag_move_corr
            dy *= self.diag_move_corr

        self.check_wall_collision(dx, dy)  # Check and handle wall collisions.

        self.angle %= math.tau  # Keep the angle within a full circle range.

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        # Check for collisions with walls and adjust player position.
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.X + dx * scale), int(self.y)):
            self.X += dx
        if self.check_wall(int(self.X), int(self.y + dy * scale)):
            self.y += dy

    def mouse_control(self):
        # Control player view direction using the mouse.
        mx, my = pg.mouse.get_pos()
        # Reset mouse position to screen center if it goes too far to the left or right.
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]  # Get horizontal mouse movement.
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))  # Limit mouse movement.
        # Adjust player angle based on mouse movement.
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update(self):
        # Update player state each frame.
        self.movement()  # Update movement.
        self.mouse_control()  # Update mouse control.
        self.recover_health()  # Recover health if needed.

    @property
    def pos(self):
        # Property to get player's current position.
        return self.X, self.y
    
    @property
    def map_pos(self):
        # Property to get player's position on the map (as integers).
        return int(self.X), int(self.y)
