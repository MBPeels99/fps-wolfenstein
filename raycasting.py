import pygame as pg
import math
from settings import *

class RayCasting:
    
    def __init__(self, game):
        # Initializing the RayCasting object.
        self.game = game  # Reference to the main game object.
        self.ray_casting_result = []  # Stores the results of ray casting.
        self.objects_to_render = []  # Stores objects that need to be rendered.
        self.textures = self.game.object_renderer.wall_textures  # Texture data for walls.
    
    def get_objects_to_render(self):
        # Determines which objects to render based on ray casting results.
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            # Handling the case when projected height is less than the screen height.
            if proj_height < HEIGHT:
                # Selecting a portion of the texture to render.
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                # Scaling the texture to fit the projection height.
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                # Calculating position to render the wall segment.
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                # Handling textures for walls taller than the screen.
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                # Scaling the texture to fit the entire screen height.
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                # Positioning the texture at the top of the screen.
                wall_pos = (ray * SCALE, 0)

            # Adding the prepared wall segment to objects to render.
            self.objects_to_render.append((depth, wall_column, wall_pos))
    
    def ray_cast(self):
        # Performs ray casting to determine visibility of walls and objects.
        self.ray_casting_result = []

        ox, oy = self.game.player.pos  # Player's position.
        x_map, y_map = self.game.player.map_pos  # Player's position on the map.

        texture_vert, texture_hor = 1, 1

        # Initial angle for ray casting.
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # Checking for horizontal grid intersections.
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            # Looping to find the nearest horizontal wall hit.
            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # Checking for vertical grid intersections.
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            # Looping to find the nearest vertical wall hit.
            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # Determining the closer hit between horizontal and vertical.
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # Correcting the 'fishbowl' distortion effect.
            depth *= math.cos(self.game.player.angle - ray_angle)

            # Calculating the height of the wall projection on the screen.
            proj_height = SCREEN_DIST / (depth + 0.0001)

            # Storing the ray casting result for rendering.
            self.ray_casting_result.append((depth, proj_height, texture, offset))

            # Incrementing the angle for the next ray.
            ray_angle += DELTA_ANGLE

    def update(self):
        # Update method called every frame to perform ray casting and determine renderable objects.
        self.ray_cast()
        self.get_objects_to_render()
