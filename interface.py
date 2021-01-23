import pygame
from solver import LabyrinthSolver

class GUI:
    def __init__(self, size):
        self.screen = pygame.display.set_mode(size)
        self.solver = LabyrinthSolver()

    def main(self):

        self.solver.take_labyrinth('lab1.png', (980,480))
        background = pygame.image.load('lab1.png')
        backgroundrect = background.get_rect()

        running = True
        points = []
        points_to_draw = None
        taken = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if len(points) < 2:
                        points.append(mouse)
                if len(points) == 2 and not taken:
                    poinst_to_draw = self.solver.solve(points[0], points[1])
                    taken = True
            
            self.screen.blit(background, backgroundrect)
            if taken:
                for point in poinst_to_draw:
                    pygame.draw.circle(self.screen, (0,0,0), (int(point.value[0])-5, int(point.value[1])-5), 10)
            pygame.display.flip()
            

if __debug__ and __name__ == "__main__":

    gui = GUI((1000,600))
    gui.main()