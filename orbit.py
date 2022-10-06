import pygame
import math
import random

pygame.init()

# Screen is half the size of the screen
SCREEN =  pygame.display.set_mode((1600, 1000))

WIDTH, HEIGHT = SCREEN.get_size()


# Planet class colors
WHITE = (255, 255, 255)
SUN_COL = (255, 255, 0)
MER_COL = (219, 206, 202)
VEN_COL = (255, 198, 73)
EAR_COL = (100, 149, 237)
MARS_RED = (188, 39, 50)
JUP_COL = (255, 203, 164)
SAT_COL = (123, 120, 105)
URN_COL = (79, 208, 231)
NEP_COL = (41, 144, 181)

FONT = pygame.font.SysFont("comics", 16)


class Planet:
    AU =  149597870700  # meters
    G = 6.674e-11
    TIMESTEP = 3600 * 24 # 1 day
    # How close the planets are to each other, no planet touches sun
    SCALE = 20 / AU

    def __init__(self, x, y, rad, color, mass):
        self.x = x
        self.y = y
        self.radius = rad
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.dis_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, screen):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_coords = []
            for coord in self.orbit:
                x, y = coord
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_coords.append((x, y))

            pygame.draw.lines(screen, self.color, False, updated_coords, 1)

        pygame.draw.circle(screen, self.color, (int(x), int(y)), self.radius)

        if not self.sun:
            # Render distance to sun
            text = FONT.render(f"{round(self.dis_to_sun/1000, 1)}km", 1, WHITE)
            screen.blit(text, (x + self.radius, y - self.radius))
             
        # Screen displays stars. Stars do not move
        if self.sun:
            for i in range(100):
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                pygame.draw.circle(screen, WHITE, (x, y), 1)

       

    # other is the planet that is being attracted to
    def grav(self, other):
        other_x, other_y = other.x, other.y
        dis_x = other_x - self.x
        dis_y = other_y - self.y
        dis = math.sqrt(dis_x ** 2 + dis_y ** 2)

        if other.sun:
            self.dis_to_sun = dis

        force = self.G * self.mass * other.mass / dis ** 2
        theta = math.atan2(dis_y, dis_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_pos(self, planets):
        self.orbit.append((self.x, self.y))

        # if orbit is too long, remove the first element. 1000 is arbitrary
        if len(self.orbit) > 5000:
            self.orbit.pop(0)

        # Calculate the net force on the planet
        net_force_x = 0
        net_force_y = 0
        for planet in planets:
            if planet != self:
                force_x, force_y = self.grav(planet)
                net_force_x += force_x
                net_force_y += force_y

        # Update the velocity
        self.x_vel += net_force_x / self.mass * self.TIMESTEP
        self.y_vel += net_force_y / self.mass * self.TIMESTEP

        # Update the position
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 8, SUN_COL, 1.989e30)
    sun.sun = True

    mercury = Planet(0.387 * sun.AU, 0, 2, MER_COL, 3.285e23)
    mercury.y_vel = 47.87e3

    venus = Planet(0.723 * Planet.AU, 0, 3.5, VEN_COL, 4.87 * 10**24)
    venus.y_vel = 35.02e3

    earth = Planet(1 * Planet.AU, 0, 3.2, EAR_COL, 5.97 * 10**24)
    earth.y_vel = 29.78e3

    mars = Planet(1.524 * Planet.AU, 0, 3, MARS_RED, 6.42 * 10**23)
    mars.y_vel = 24.13e3

    jupiter = Planet(5.203 * Planet.AU, 0, 7, JUP_COL, 1.90 * 10**27)
    jupiter.y_vel = 13.07e3
    
    saturn = Planet(9.539 * Planet.AU, 0, 6, SAT_COL, 5.68 * 10**26)
    saturn.y_vel = 9.69e3
    
    uranus = Planet(19.18 * Planet.AU, 0, 6, URN_COL, 8.68 * 10**25)
    uranus.y_vel = 6.81e3
    
    neptune = Planet(30.06 * Planet.AU, 0, 7, NEP_COL, 1.02 * 10**26)
    neptune.y_vel = 5.43e3

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((0, 0, 0))

        for planet in planets:
            planet.update_pos(planets)
            planet.draw(SCREEN)

        pygame.display.update()

    pygame.quit()


main()

