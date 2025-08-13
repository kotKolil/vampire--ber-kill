class AbcParticles:

    def __init__(self):
        #dx and dy is direction on Ox and Oy of movement vector. 1 is up and right, -1 is down and left
        self.dx = 1
        self.dy = 1
        self.x = 0
        self.y = 0
        self.iterative = False
        self.life_s = 0
        self.enemies = []
        self.animation = None

    def collide_script(self):
        pass