import pygame
import sys
import time
from pygame.locals import *
from math import *

pygame.init()


clock = pygame.time.Clock()
width, height = 1200, 800
FPS = 24
screen = pygame.display.set_mode((width, height))
z_main = 400
rotate_y = 0
rotate_x = 0
rotate_z = 0
font = pygame.font.SysFont('Arial', 36)
doubles = []


class Dots:
    def __init__(self, position=[width//2, height//2]):
        self.Dts = []
        self.Pths = {}
        self.text = None
        self.place = None
        self.pos = position

    def add(self, *args):
        for dt in args:
            self.Dts.append(dt)
            dt.pos = self.pos

    def add_paths(self, **kwargs):
        for dt1, dt2 in kwargs.items():
            if dt1 in self.Pths.keys():
                self.Pths.get(dt1).extend(dt2)
            else:
                self.Pths.update({dt1: dt2})

    def sorting(self):
        if self.Dts:
            dots = sorted(self.Dts, key=lambda d: z_main - d.get_z(), reverse=True)
            return dots
        else:
            return 0

    def draw_all(self, cond=True):
        if self.text and cond:
            screen.blit(self.text, self.place)
        dots = self.sorting()
        draw = []
        for d in dots:
            d.draw()
            if self.Pths.get(d.name()):
                for path in self.Pths.get(d.name()):
                    if {d, path} in draw:
                        pass
                    else:
                        clr = (max(d.get_color()) + max(path.get_color())) // 2
                        if ({d, path} in doubles) and (d.get_r() >= 20) and (path.get_r() >= 20):
                            pygame.draw.line(screen,
                                             [clr, clr, clr],
                                             (d.get_x() + self.pos[0], d.get_y() + self.pos[1] + 5),
                                             (path.get_x() + self.pos[0], path.get_y() + self.pos[1] + 5),
                                             width=5)
                            pygame.draw.line(screen,
                                             [clr, clr, clr],
                                             (d.get_x() + self.pos[0], d.get_y() + self.pos[1] - 5),
                                             (path.get_x() + self.pos[0], path.get_y() + self.pos[1] - 5),
                                             width=5)
                        else:
                            pygame.draw.line(screen,
                                         [clr, clr, clr],
                                         (d.get_x() + self.pos[0], d.get_y() + self.pos[1]),
                                         (path.get_x() + self.pos[0], path.get_y() + self.pos[1]),
                                         width=5)
                        draw.append({d, path})

    def rotate_y(self, anglex=0, angley=0, anglez=0):
        for d in self.Dts:
            d.rotate_by_y(anglex, angley, anglez)

    def set(self, pos=[width//2, height//2]):
        for d in self.Dts:
            d.pos = pos
            self.pos = pos


class Dot:
    def __init__(self,
                 x=0,
                 y=0,
                 z=0,
                 size=10,
                 color=(255, 255, 255),
                 position=[width//2, height//2]):
        self.x = x
        self.y = - y
        self.z = z
        self.size = size
        self.red = color[0]
        self.green = color[1]
        self.blue = color[2]
        self.pos = position

        self.rotate_by_y()

    def rotate_by_y(self, anglex=0, angley=0, anglez=0):
        self.resx = self.x * cos(angley) * cos(anglez) - self.y * sin(anglez) * cos(angley) + self.z * sin(angley)
        self.resy = self.x * (sin(anglex) * sin(angley) * cos(anglez) + sin(anglez) * cos(anglex)) + self.y * (cos(anglex) * cos(anglez) - sin(anglex) * sin(anglez) * sin(angley)) - self.z * sin(anglex) * cos(angley)
        self.resz = self.x * (sin(anglex) * sin(anglez) - sin(angley) * cos(anglex) * cos(anglez)) + self.y * (sin(anglex) * cos(anglez) + sin(angley) * sin(anglez) * cos(anglex)) + self.z * cos(anglex) * cos(angley)

    def draw(self):
        pygame.draw.circle(screen,
                           self.get_color(),
                           (self.pos[0] + self.get_x(), self.pos[1] + self.get_y()),
                           self.get_r())

    def get_x(self):
        if (z_main - self.resz) == 0:
            return 0
        return (self.resx * z_main) / (z_main - self.resz)

    def get_y(self):
        if (z_main - self.resz) == 0:
            return 0
        return (self.resy * z_main) / (z_main - self.resz)

    def get_r(self):
        if (-1 <= (z_main - self.resz)) and ((z_main - self.resz) <= 1):
            return 1000
        return (self.size * z_main) / (z_main - self.resz)

    def get_z(self):
        return self.resz

    def get_color(self):
        red = self.red
        green = self.green
        blue = self.blue
        res = []
        if red:
            res.append(red * (z_main + self.get_z()) // (z_main))
        else:
            res.append(0)
        if green:
            res.append(green * (z_main + self.get_z()) // (z_main))
        else:
            res.append(0)
        if blue:
            res.append(blue * (z_main + self.get_z()) // (z_main))
        else:
            res.append(0)

        for i in [0, 1, 2]:
            if res[i] > 255:
                res[i] = 255
            if res[i] < 0:
                res[i] = 0

        return tuple(res)

    def name(self):
        for k, v in globals().items():
            if v is self:
                return k

    def make_new(self, ax=0, ay=0, az=0):
        self.rotate_by_y(ax, ay, az)
        res = (self.resx, self.resy, self.resz)
        return res


carbon = Dot(x=0,
             z=0,
             size=25,
             color=[255, 0, 0])
hydro1 = Dot(x=0,
             z=0,
             y=100,
             size=20,
             color=[0, 0, 128])
xyz2 = hydro1.make_new(0.33 * pi, 0, 0)
hydro2 = Dot(x=round(xyz2[0]),
             y=round(xyz2[1]),
             z=round(xyz2[2]),
             size=20,
             color=[0, 0, 128])
xyz3 = hydro2.make_new(0, 0.66 * pi, 0)
hydro3 = Dot(x=round(xyz3[0]),
             y=round(xyz2[1]),
             z=round(xyz3[2]),
             size=20,
             color=[0, 0, 128])
xyz4 = hydro2.make_new(0, 1.32 * pi, 0)
hydro4 = Dot(x=round(xyz4[0]),
             y=round(xyz2[1]),
             z=round(xyz4[2]),
             size=20,
             color=[0, 0, 128])

D = Dots()
D.add(carbon, hydro1, hydro2, hydro3, hydro4)
D.add_paths(carbon=[hydro1, hydro2, hydro3, hydro4],
            hydro1=[carbon],
            hydro2=[carbon],
            hydro3=[carbon],
            hydro4=[carbon])
D.text = font.render("Метан", True, (255, 255, 255))
D.place = D.text.get_rect(center=(600, 600))

D1 = Dots(position=[-300 + width//2, 0 + height//2])
c1 = Dot(x=0,
         y=120,
         z=0,
         size=25,
         color=[255, 0, 0])
h1 = Dot(x=0,
         y=200,
         z=0,
         size=20,
         color=[0, 0, 128])
xyz = c1.make_new(az=pi/3)
xyzh = h1.make_new(az=pi/3)
c2 = Dot(x=round(xyz[0]),
         y=round(xyz[1]),
         z=round(xyz[2]),
         size=25,
         color=[255, 0, 0])
h2 = Dot(x=round(xyzh[0]),
         y=round(xyzh[1]),
         z=round(xyzh[2]),
         size=20,
         color=[0, 0, 128])
xyz = c1.make_new(az = 2 * pi / 3)
xyzh = h1.make_new(az = 2 * pi / 3)
c3 = Dot(x=round(xyz[0]),
         y=round(xyz[1]),
         z=round(xyz[2]),
         size=25,
         color=[255, 0, 0])
h3 = Dot(x=round(xyzh[0]),
         y=round(xyzh[1]),
         z=round(xyzh[2]),
         size=20,
         color=[0, 0, 128])
xyz = c1.make_new(az = 0)
xyzh = h1.make_new(az = 0)
br4 = Dot(x=round(xyzh[0]),
         y=round(xyzh[1]),
         z=round(xyzh[2]),
         size=35,
         color=[128, 64, 0])
c4 = Dot(x=round(xyz[0]),
         y=round(xyz[1]),
         z=round(xyz[2]),
         size=25,
         color=[255, 0, 0])
h4 = Dot(x=round(xyzh[0]),
         y=round(xyzh[1]),
         z=round(xyzh[2]),
         size=20,
         color=[0, 0, 128])
xyz = c1.make_new(az = 4 * pi / 3)
xyzh = h1.make_new(az = 4 * pi / 3)
c5 = Dot(x=round(xyz[0]),
         y=round(xyz[1]),
         z=round(xyz[2]),
         size=25,
         color=[255, 0, 0])
h5 = Dot(x=round(xyzh[0]),
         y=round(xyzh[1]),
         z=round(xyzh[2]),
         size=20,
         color=[0, 0, 128])
xyz = c1.make_new(az = 5 * pi / 3)
xyzh = h1.make_new(az = 5 * pi / 3)
c6 = Dot(x=round(xyz[0]),
         y=round(xyz[1]),
         z=round(xyz[2]),
         size=25,
         color=[255, 0, 0])
h6 = Dot(x=round(xyzh[0]),
         y=round(xyzh[1]),
         z=round(xyzh[2]),
         size=20,
         color=[0, 0, 128])
D1.add(c1, c2, c3, c4, c5, c6, h1, h2, h3, h4, h5, h6)
D1.add_paths(c1=[h1, c3, c5],
             c2=[h2, c3, c4],
             c3=[h3, c1, c2],
             c4=[h4, c2, c6],
             c5=[h5, c6, c1],
             c6=[h6, c4, c5],
             h1=[c1],
             h2=[c2],
             h3=[c3],
             h4=[c4],
             h5=[c5],
             h6=[c6])
doubles.append({c2, c3})
doubles.append({c1, c5})
doubles.append({c6, c4})
D1.text = font.render("Бензол", True, (255, 255, 255))
D1.place = D.text.get_rect(center=(600, 600))

plus = font.render("+", True, (255,255,255))
place = plus.get_rect(center=(600, 400))

Bor = Dots(position=[300 + width//2, 0 + height//2])
br1 = Dot(x=100,
          y=0,
          z=0,
          size=35,
          color=(128, 64, 0))
br2 = Dot(x=-100,
          y=0,
          z=0,
          size=35,
          color=[128, 64, 0])
Bor.add(br1, br2)
Bor.add_paths(br1=[br2],
              br2=[br1])

brommetan = Dots([width//2 - 200, height//2])
br3 = Dot(y=100,
          size=35,
          color=(128, 64, 0))
brommetan.add(carbon, hydro2, hydro3, hydro4, br3)
brommetan.add_paths(carbon=[br3, hydro2, hydro3, hydro4],
                    hydro2=[carbon],
                    hydro4=[carbon],
                    hydro3=[carbon],
                    br3=[carbon])
hidbr = Dots([width//2 + 200, height//2])
hid = Dot(x=100,
          size=20,
          color=(0, 0, 128))
hidbr.add(hid, br2)
hidbr.add_paths(hid=[br2],
                br2=[hid])
brombenzol = Dots()
brombenzol.add(c1, c2, c3, c4, c5, c6, h1, h2, h3, br4, h5, h6)
brombenzol.add_paths(c1=[h1, c3, c5],
             c2=[h2, c3, c4],
             c3=[h3, c1, c2],
             c4=[br4, c2, c6],
             c5=[h5, c6, c1],
             c6=[h6, c4, c5],
             h1=[c1],
             h2=[c2],
             h3=[c3],
             br4=[c4],
             h5=[c5],
             h6=[c6])



count = [[D],
         [D, Bor],
         [brommetan, hidbr],
         [D1],
         [D1, Bor],
         [brombenzol, hidbr]]
positions = [[()],
             [(width//2 - 200, height//2), (width//2 + 200, height//2)],
             [(width//2 - 200, height//2), (width//2 + 200, height//2)],
             [()],
             [(width//2 - 200, height//2), (width//2 + 200, height//2)],
             [(width//2 - 200, height//2), (width//2 + 200, height//2)]]
text = (True, False, False, True, False, False)
curr = 0

while True:
    # Тело
    screen.fill((0, 0, 0))

    scene = count[curr]
    position = [width//2, height//2]
    for i, dots in enumerate(scene):
        if len(scene) == 2:
            screen.blit(plus, place)
        dots.set(positions[curr][i] if positions[curr][i] else [width//2, height//2])
        dots.draw_all(text[curr])


    pygame.display.update()

    # Проверка выхода
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_0:
                if count[curr] == count[-1]:
                    curr = 0
                else:
                    curr += 1

    # Проверка клавиш
    if pygame.key.get_pressed()[K_RIGHT]:
        rotate_y += pi / 18
        for dots in scene:
            dots.rotate_y(rotate_x, rotate_y, rotate_z)
    if pygame.key.get_pressed()[K_LEFT]:
        rotate_y -= pi / 18
        for dots in scene:
            dots.rotate_y(rotate_x, rotate_y, rotate_z)
    if pygame.key.get_pressed()[K_UP]:
        rotate_x += pi / 18
        for dots in scene:
            dots.rotate_y(rotate_x, rotate_y, rotate_z)
    if pygame.key.get_pressed()[K_DOWN]:
        rotate_x -= pi / 18
        for dots in scene:
            dots.rotate_y(rotate_x, rotate_y, rotate_z)
    if pygame.key.get_pressed()[K_e]:
        rotate_z += pi / 18
        for dots in scene:
            dots.rotate_y(rotate_x, rotate_y, rotate_z)
    if pygame.key.get_pressed()[K_q]:
        rotate_z -= pi / 18
        for dots in scene:
            dots.rotate_y(rotate_x, rotate_y, rotate_z)
    if pygame.key.get_pressed()[K_SPACE]:
        rotate_z, rotate_y, rotate_x = 0, 0, 0
        for dots in scene:
            dots.rotate_y(rotate_x, rotate_y, rotate_z)


    clock.tick(FPS)
    pygame.event.pump()
