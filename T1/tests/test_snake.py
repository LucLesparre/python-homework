"""Les tests du T1. Lancez-les avec : uv run pytest

Au début, presque tout est rouge : c'est normal. Chaque étape de l'énoncé
fait passer quelques tests au vert.
"""

import pygame as pg

import snake

# --- étape 0 : importer snake.py ne doit rien lancer -------------------------


def test_import_n_ouvre_pas_de_fenetre():
    # Si cette ligne échoue, c'est que du code tourne au moment de l'import :
    # la boucle de jeu doit vivre dans main(), appelée sous `if __name__ == ...`.
    assert pg.display.get_surface() is None


# --- étape 5 : le serpent avance ---------------------------------------------


def test_in_scope():
    assert snake.in_scope((0, 0))
    assert snake.in_scope((snake.X - 1, snake.Y - 1))
    assert not snake.in_scope((-1, 5))
    assert not snake.in_scope((5, snake.Y))


def test_next_head():
    s = [(10, 15), (11, 15), (12, 15)]
    assert snake.next_head(s, (1, 0)) == (13, 15)
    assert snake.next_head(s, (0, -1)) == (12, 14)
    assert s == [(10, 15), (11, 15), (12, 15)]  # pas modifié


def test_move_avance_d_une_case():
    s = [(10, 15), (11, 15), (12, 15)]
    assert snake.move(s, (1, 0), (0, 0)) == "moved"
    assert s == [(11, 15), (12, 15), (13, 15)]


# --- étape 6 : les flèches ---------------------------------------------------


def test_turn():
    assert snake.turn((1, 0), pg.K_UP) == (0, -1)
    assert snake.turn((1, 0), pg.K_DOWN) == (0, 1)
    assert snake.turn((0, 1), pg.K_LEFT) == (-1, 0)
    assert snake.turn((1, 0), pg.K_a) == (1, 0)  # autre touche : on garde le cap


def test_turn_pas_de_demi_tour():
    assert snake.turn((1, 0), pg.K_LEFT) == (1, 0)
    assert snake.turn((0, -1), pg.K_DOWN) == (0, -1)


# --- étape 7 : le fruit ------------------------------------------------------


def test_move_mange_le_fruit():
    s = [(10, 15), (11, 15), (12, 15)]
    assert snake.move(s, (1, 0), (13, 15)) == "ate"
    assert s == [(10, 15), (11, 15), (12, 15), (13, 15)]


def test_random_fruit_tombe_sur_une_case_libre():
    s = [(x, y) for x in range(snake.X) for y in range(snake.Y)]
    libre = s.pop(42)
    assert snake.random_fruit(s) == libre


# --- étape 8 : fin de partie -------------------------------------------------


def test_move_sort_du_plateau():
    s = [(snake.X - 2, 0), (snake.X - 1, 0)]
    assert snake.move(s, (1, 0), (0, 5)) == "out-of-board"


def test_move_se_mord():
    # la tête est en (5, 6) ; en montant, elle arrive sur (5, 5), dans le corps
    s = [(4, 5), (5, 5), (6, 5), (6, 6), (5, 6)]
    assert snake.move(s, (0, -1), (0, 0)) == "self-bite"


# --- étape 2 : la boucle de jeu s'arrête sur q ------------------------------


class TropDImages(Exception):
    pass


def test_main_s_arrete_sur_q(monkeypatch):
    # On remplace le clavier par un « q » tapé à chaque image, et on compte les
    # images : au-delà de 3, la boucle ne s'arrête visiblement pas.
    images = []

    def evenements(*args, **kwargs):
        return [pg.event.Event(pg.KEYDOWN, key=pg.K_q)]

    def update(*args, **kwargs):
        images.append(1)
        if len(images) > 3:
            pg.quit()
            raise TropDImages("la boucle ne s'arrête pas quand on tape q")

    monkeypatch.setattr(pg.event, "get", evenements)
    monkeypatch.setattr(pg.display, "update", update)
    monkeypatch.setattr(pg.display, "flip", update)
    snake.main()
    assert pg.display.get_surface() is None  # pg.quit() a bien été appelé
