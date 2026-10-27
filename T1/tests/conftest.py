import os

# Pas de vraie fenêtre pendant les tests : pygame dessine dans le vide.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
