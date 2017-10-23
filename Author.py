from Scenes.RotatingCube import RotatingCube
import Scenes.Loader

def start(game):
    # load scenes
    Scenes.Loader.loadAll(game)

    # set scene
    game.setScene("RotatingCube")
    game.main()