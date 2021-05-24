import pygame
import operations as op

class triangle:
    def __init__(self, e1, e2, e3):
        self.e1 = e1
        self.e2 = e2
        self.e3 = e3
        self.color = e1.color 
        self.edges = (e1, e2, e3)

    def __repr__(self):
        return str((self.e1.a, self.e2.a, self.e3.a))
    
    def __eq__(self, other):
        return (
                    self.e1.a.xy == other.e1.a.xy and
                    self.e2.a.xy == other.e2.a.xy and
                    self.e3.a.xy == other.e3.a.xy 
                )

    def draw(self, width, screen):
        pygame.draw.polygon(screen, self.color, [self.e1.a.xy, self.e2.a.xy, self.e3.a.xy], width)
    
    def has_vertice(self, vertice):
        return (vertice == self.e1.a or vertice == self.e2.a or vertice == self.e3.a)

    def in_circumcircle(self, vertice):
        ax = self.e1.a.x
        ay = self.e1.a.y
        bx = self.e2.a.x
        by = self.e2.a.y
        cx = self.e3.a.x
        cy = self.e3.a.y
        result = op.inCircle(ax, ay, bx, by, cx, cy, vertice.x, vertice.y) 
        return result

class edge:
    def __init__(self, a, b, color, width):
        self.a = a
        self.b = b
        self.ab = (a, b)
        self.color = color
        self.width = width

    def __repr__(self):
        return str(self.ab)

    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.a.xy, self.b.xy, self.width)

class vertice:
    def __init__(self, x, y, color, size):
        self.x = x
        self.y = y
        self.xy = (x, y)
        self.color = color
        self.size = size

    def __repr__(self):
        return str(self.xy)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.xy, self.size)

    def draw_pos(self, screen, font, color):
        padding = 5
        pos = font.render(str(self.xy), True, color)
        screen.blit(pos, (self.x + padding, self.y + padding))
