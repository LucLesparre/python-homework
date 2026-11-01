"""T2 – Boids : le code de départ (étape 0).

D'après le TP « boids » de Thierry Parmentelat (flotpython), réécrit pour le
cours AP Python et pour arcade 3.

Lancez-le avec :  uv run boids.py
Testez-le avec :  uv run pytest
"""

import math
import random
from pathlib import Path

import arcade

WIDTH, HEIGHT = 800, 800
BACKGROUND = arcade.color.ALMOND

# Les images, cherchées à côté de ce fichier, d'où qu'on le lance.
HERE = Path(__file__).parent
ARROW = HERE / "media" / "arrow.png"
OBSTACLE = HERE / "media" / "obstacle.png"
SKY = HERE / "media" / "sky.png"
YELLOWSTONE = HERE / "media" / "fond.jpg"  # le décor (étape 9)

SPEED = 100  # pixels par seconde (étape 2)
TURN_SPEED = 180  # degrés par seconde, tant qu'une flèche est enfoncée (étape 5)
NOISE = 3  # écart maximal du cap à chaque mise à jour, en degrés (étape 5)
N_BOIDS = 20  # (étape 4)
GRID = 10  # GRID × GRID obstacles (étape 6)
RADIUS = 30  # rayon de détection des voisins, en pixels (étapes 7 et 8)


# --- les objets du jeu -------------------------------------------------------
# Ces classes et fonctions sont vérifiées par les tests (tests/test_boids.py) :
# gardez leur nom et leurs paramètres.
#
# Chaque `raise NotImplementedError("étape …")` est un trou à remplir. S'il est
# atteint, le programme s'arrête net, avec ce message : il dit à quelle étape
# écrire ce morceau. Quand vous y arrivez, effacez la ligne et écrivez votre code.
# À l'étape 0, la fenêtre n'utilise encore aucune de ces classes : rien ne casse.


class Boid(arcade.Sprite):
    """Un oiseau : une flèche qui avance dans la direction où elle pointe."""

    def __init__(self, x, y, angle, speed=SPEED, others=None):
        super().__init__(ARROW, center_x=x, center_y=y, angle=angle)
        self.speed = speed
        self.turning = 0
        if others is None:
            self.others = []
        else:
            self.others = others
    
    def update(self, delta_time=1 / 60, *args, **kwargs):
        """Appelée par arcade (via la SpriteList) à chaque mise à jour."""
        self.angle +=  self.turning * TURN_SPEED * delta_time + random.uniform(-NOISE,NOISE)
        rad= math.radians(self.angle)
        dx,dy = self.separation(self.others, RADIUS)    
        self.center_x += self.speed*delta_time * math.cos(rad) + dx
        self.center_y -= self.speed*delta_time * math.sin(rad) - dy
        self.center_x %= WIDTH
        self.center_y %= HEIGHT
        voisins = self.neighbours(self.others, RADIUS)
        if len(voisins)>0:
            self.alpha = 100
        else:
            self.alpha = 255
        
        


    def neighbours(self, others, radius=RADIUS):
        """Les objets de `others` à moins de `radius` pixels, sauf soi-même."""
        L= []
        for elmt in others:
            if elmt is not self and math.dist(self.position, elmt.position)<radius:
                    L.append(elmt)
        return L
            

    def separation(self, others, radius=RADIUS):
        """Le déplacement (dx, dy) qui écarte le boid de ses voisins."""
        voisins = self.neighbours(others, radius)
        dx,dy = 0,0
        for vois in voisins:
            d = math.dist(self.position, vois.position)
            dx += (self.center_x - vois.center_x)* 0.5 * (1 - d/radius)
            dy += (self.center_y - vois.center_y)* 0.5 * (1 - d/radius)
        return (dx,dy)


class Obstacle(arcade.Sprite):
    """Un obstacle immobile."""

    def __init__(self, x, y):
        super().__init__(OBSTACLE,center_x=x, center_y = y)


def random_boids(n, others=None):
    """n boids placés et orientés au hasard, qui évitent tous `others`."""
    L = arcade.SpriteList()
    for i in range(n):
        x, y, angle = random.uniform(0,WIDTH), random.uniform(0,HEIGHT), random.uniform(0,360)
        boid=Boid(x,y,angle)
        L.append(boid)
    return L

def obstacle_grid(n):
    """n × n obstacles régulièrement espacés, au centre de leur carré."""
    L= arcade.SpriteList()
    for i in range(n):
        for j in range(n):
            L.append(Obstacle((i + 0.5)*WIDTH / n, (j+0.5)*HEIGHT / n))
    return L


# --- la fenêtre ---------------------------------------------------------------


class MyWindow(arcade.Window):
    def __init__(self, N=40):
        # d'abord, ce que fait toute fenêtre d'arcade : s'ouvrir, en WIDTH × HEIGHT
        # pixels, avec « Boids » pour titre (super() : on y revient en séance)
        super().__init__(WIDTH, HEIGHT, "Boids")
        self.background_color = BACKGROUND  # la couleur que self.clear() étale

        self.sky = arcade.SpriteList()
        fond = arcade.Sprite(YELLOWSTONE, center_x=WIDTH/2, center_y=HEIGHT/2)
        fond.alpha=160
        self.sky.append(fond)

        self.obsts = obstacle_grid(10)
        # pour l'instant, un simple Sprite : une image posée en (100, 100),
        # comptés depuis le coin en bas à 
        self.boids = random_boids(N)
        print(type(self.boids), type(self.obsts))
        A_eviter = arcade.SpriteList()
        A_eviter.extend(self.boids)
        A_eviter.extend(self.obsts)
        for elmt in self.boids:
            elmt.others = A_eviter
        
        # une SpriteList : une liste de sprites, qu'arcade dessine d'un coup
    
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        for elt in self.boids:
            if key == arcade.key.LEFT:
                elt.turning = -1
            elif key == arcade.key.RIGHT:
                elt.turning = 1
            elif key == arcade.key.Q:
                self.close()
        
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        for elt in self.boids:
            if key == arcade.key.LEFT or key == arcade.key.RIGHT:
                elt.turning = 0

    def on_update(self, delta_time):
        self.boids.update(delta_time)
    def on_draw(self):
        self.clear()
        self.sky.draw()
        self.obsts.draw()
        self.boids.draw()


def main():
    MyWindow()
    arcade.run()


# Ce bloc ne s'exécute que si l'on lance ce fichier (uv run boids.py),
# pas quand un autre fichier fait `import boids` (les tests, par ex.).
if __name__ == "__main__":
    main()
