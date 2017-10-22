from Scenes.TestScene import TestScene
from Scenes.RotatingCube import RotatingCube

def start(game):
    # TestScene(game)
    RotatingCube(game)

    game.setScene("RotatingCube")
    game.main()