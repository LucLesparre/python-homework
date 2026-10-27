# T1 – Snake procédural

Nous allons écrire, pas à pas, un petit jeu de Snake avec la bibliothèque pygame. L'objectif n'est pas d'écrire le prochain succès du jeu vidéo, mais de construire un programme complet qui marche, et de comprendre au passage comment tourne une *boucle de jeu*. Ce TP se fait **en séance, individuellement, et ne se rend pas** ; prenez-le tout de même au sérieux, car le Snake nous suivra jusqu'au tournoi de bots.

D'après le TP « Snake » de Thierry Parmentelat et Aurélien Noce ([flotpython/exos-python](https://github.com/flotpython/exos-python)), réécrit pour ce cours.

## Et l'IA ?

Vous pouvez vous servir d'une IA comme d'un outil pour comprendre : vous faire expliquer une erreur, une fonction de pygame, ou demander une piste quand vous êtes bloqués. En revanche, **on ne copie jamais le code qu'elle propose** : on comprend sa réponse assez bien pour réécrire le code soi-même, fenêtre de l'IA fermée. Si vous n'y arrivez pas, c'est qu'il faut lui reposer des questions, pas lui recopier. Pour la même raison, coupez la complétion automatique (Copilot ou autre) dans VS Code, qui écrit à votre place.

Ce n'est pas une punition : ces huit étapes sont courtes, et c'est en les écrivant vous-même que la boucle de jeu deviendra un réflexe.

## Mode d'emploi

Vous travaillez dans **un seul fichier**, `snake.py`, que vous faites évoluer d'étape en étape. Et à chaque étape qui marche, vous faites un commit : ainsi, quand un bug apparaît, il suffit de regarder ce qui a changé depuis la dernière version qui marchait.

Chacun avance à son rythme : en séance, je vous arrêterai de temps en temps pour regarder ensemble un conseil ou un piège, puis chacun reprend là où il en était. Si vous êtes bloqués, la section « Coups de pouce », à la fin, peut vous aider.

Les tests (`tests/test_snake.py`) vérifient les fonctions de la partie « logique » du fichier. Au début, ils sont presque tous rouges : c'est normal, chaque étape en fait passer quelques-uns au vert. Gardez donc les noms et les paramètres des fonctions déjà présentes dans `snake.py`.

## Étape 0 – On s'installe

Dézippez `T1-snake.zip` à la racine de votre dépôt `python-homework` : vous obtenez un dossier `T1/`. Ouvrez-le dans un terminal (ou dans VS Code : *File → Open Folder*), puis :

```bash
cd T1
uv add pygame-ce        # ajoute pygame au projet et crée l'environnement .venv
uv run snake.py         # lance le jeu
```

⚠️ On installe `pygame-ce`, mais on l'importe sous le nom `pygame`. C'est une version de pygame maintenue par la communauté, qui s'installe sans souci sur les Python récents. N'installez jamais `pygame` et `pygame-ce` dans le même projet : ils se marchent dessus.

Une fenêtre s'ouvre et change de couleur toutes les secondes. Vous ne pouvez pas la fermer avec la croix : c'est normal à ce stade, tapez `Ctrl+C` dans le terminal.

Avant d'aller plus loin, réglons VS Code une fois pour toutes :

1. ouvrez le dossier `T1` lui-même (*File → Open Folder*), et non `python-homework` : VS Code trouve alors tout seul l'environnement `.venv` du projet ;
2. installez les extensions **Python** (Microsoft) et **Ruff** ;
3. choisissez l'interpréteur du projet : `Ctrl+Shift+P` (`Cmd+Shift+P` sur Mac) → *Python: Select Interpreter* → celui qui contient `.venv` ;
4. lancez vos commandes depuis le terminal intégré (*Terminal → New Terminal*), qui s'ouvre directement dans `T1`. Sous Windows, ce terminal doit être **Git Bash**, pas PowerShell : `Ctrl+Shift+P` → *Terminal: Select Default Profile* → *Git Bash* ;
5. le bouton ▶ *Run Python File*, en haut à droite, lance lui aussi le fichier dans le `.venv`, mais seulement si le point 3 est fait. Pour les tests et ruff, on garde `uv run`.

Vous savez que c'est bon quand la barre du bas affiche `(.venv)` et que `import pygame` n'est plus souligné.

Lancez ensuite les tests :

```bash
uv run pytest
```

Un seul test passe pour l'instant : c'est normal, les autres passeront au vert au fil des étapes.

Enfin, depuis la racine de `python-homework`, faites votre premier commit :

```bash
git add T1
git commit -m "T1 : étape 0"
```

💡 Le fichier `.gitignore` de `T1/` évite de commiter le dossier `.venv`, qui est lourd et se recrée en une commande (`uv sync`).

## Étape 1 – Lire la boucle de jeu

Lisez `main()` sans rien modifier. La boucle `while` fait trois choses à chaque tour, c-à-d. à chaque *image* (frame) : elle lit les événements (clavier, souris), met à jour l'état du jeu, puis dessine.

**Questions.**

1. Ajoutez `print("tour")` au début de la boucle : combien de lignes s'affichent par seconde ?
2. Que fait `clock.tick(1)` ? Remplacez `1` par `10` pour vérifier.
3. Commentez la ligne `pg.display.update()` : que voit-on ? En effet, toutes les fonctions de dessin travaillent sur une image en mémoire (rapide) ; c'est `update()` qui l'envoie à l'écran (beaucoup plus lent). On l'appelle donc une seule fois par tour de boucle.
4. Qui décide *quand* la fenêtre est redessinée : vous, ou pygame ?

## Étape 2 – Pouvoir quitter

Commencez par ajouter `print(event)` dans la boucle `for event in pg.event.get():`, puis bougez la souris et tapez quelques touches : chaque action devient un *événement*, que votre code lit à chaque tour.

Remplacez `while True` par une boucle qui s'arrête proprement :

- quand on clique sur la croix de la fenêtre (événement de type `pg.QUIT`) ;
- quand on tape la touche `q` (événement de type `pg.KEYDOWN` dont la touche `event.key` vaut `pg.K_q`).

Une fois sorti de la boucle, appelez `pg.quit()` pour libérer la fenêtre (sous Windows en particulier, l'oublier laisse parfois une fenêtre fantôme). Le test `test_main_s_arrete_sur_q` doit passer. Commit !

## Étape 3 – Le damier

Le plateau fait `X × Y` = 30 × 30 cases de `W × H` = 20 × 20 pixels. Ouvrez une fenêtre à la bonne taille, puis dessinez, à chaque image, un damier à la place de la couleur aléatoire. Voici un bout de code qui dessine un rectangle rouge dont le coin en haut à gauche est au pixel (100, 200) :

```python
rect = pg.Rect(100, 200, 20, 20)        # x, y, largeur, hauteur, en pixels
pg.draw.rect(screen, (255, 0, 0), rect)
```

## Étape 4 – Un serpent immobile

Le serpent est une liste de cases. Par convention, la queue est au début de la liste et la tête à la fin :

```python
snake = [(10, 15), (11, 15), (12, 15)]
```

Dessinez-le par-dessus le damier, dans une autre couleur.

## Étape 5 – Un serpent qui avance

Le serpent avance dans une `direction`, un vecteur comme `RIGHT = (1, 0)`. À chaque image, la tête gagne une case dans cette direction, et la queue en perd une. Écrivez :

- `in_scope(tile)`, qui dit si une case est sur le plateau ;
- `next_head(snake, direction)`, qui renvoie la case où arrive la tête, **sans modifier** `snake` ;
- `move(snake, direction, fruit)`, qui **modifie** `snake` sur place et renvoie `"moved"` (on ignore le fruit pour l'instant).

Appelez `move` dans la partie « état » de la boucle, et passez à `clock.tick(6)`. Les tests de l'étape 5 doivent passer.

**Question.** `next_head` ne modifie pas la liste, `move` la modifie. Lequel des deux est le plus facile à tester, et pourquoi ? Nous y reviendrons en séance 3.

## Étape 6 – Les flèches

Écrivez `turn(direction, key)`, qui renvoie la nouvelle direction quand on appuie sur une flèche (`pg.K_UP`, `pg.K_DOWN`, `pg.K_LEFT`, `pg.K_RIGHT`), et l'ancienne pour toute autre touche. Le serpent ne doit pas pouvoir faire demi-tour : s'il va vers la droite, la flèche gauche est ignorée.

## Étape 7 – Le fruit

Un fruit (une case) apparaît sur le plateau. Quand la tête arrive dessus, le serpent grandit d'une case (on ne retire pas la queue), `move` renvoie `"ate"`, et un nouveau fruit apparaît sur une case libre, tirée au hasard par `random_fruit(snake)`.

## Étape 8 – Fin de partie

La partie s'arrête quand la tête sort du plateau (`move` renvoie `"out-of-board"`) ou quand elle arrive sur le corps du serpent (`"self-bite"`). Dans les deux cas, on sort de la boucle et on affiche le score (la longueur du serpent) dans le terminal. Pendant la partie, affichez aussi le score dans le titre de la fenêtre, avec `pg.display.set_caption(...)`.

Pour finir, vérifiez que tout est propre :

```bash
uv run pytest          # tout doit être vert
uv run ruff check .    # aucune remarque
```

Et un dernier commit !

## Coups de pouce

À ne lire que si vous êtes bloqués depuis plusieurs minutes : en séance, nous en parlons ensemble, une fois que la plupart d'entre vous auront rencontré le problème.

- **Étape 3.** Une fonction `draw_tile(screen, tile, color)`, qui colorie la case `tile = (x, y)`, traduit des coordonnées en cases en coordonnées en pixels. Elle vous resservira à chaque étape.
- **Étape 5.** `snake.append(...)` et `snake.pop(0)` modifient la liste sur place et renvoient `None` : `snake = snake.append(...)` laisse donc `snake` à `None`.
- **Étape 6.** Un dictionnaire `{pg.K_UP: UP, ...}` évite une longue cascade de `if`.

## Pour aller plus loin

À faire dans l'ordre qui vous plaît :

- tapez très vite ↑ puis ← quand le serpent va vers la droite : il se mord ! Pourtant `turn` interdit le demi-tour… Comprenez pourquoi (indice : combien de fois `turn` est-il appelé entre deux déplacements ?), puis corrigez ;
- une touche `espace` qui met le jeu en pause ;
- un serpent qui accélère à mesure qu'il grandit ;
- deux fréquences : l'affichage à 60 images par seconde, mais le serpent qui n'avance qu'à 6 cases par seconde (indice : `pg.time.get_ticks()`) ;
- des options en ligne de commande avec `argparse`, par ex. `uv run snake.py --speed 10 --size 40` ;
- un plateau sans bord : le serpent qui sort à droite rentre à gauche ;
- le meilleur score, gardé dans un fichier d'une partie à l'autre ;
- un serpent qui joue tout seul : une fonction `auto(snake, fruit)` qui renvoie une direction vers le fruit, sans se mordre. Cela vous donnera une longueur d'avance pour le tournoi…
