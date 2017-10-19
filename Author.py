from Scenes.TestScene import TestScene

def start(game):
    game.addScene(TestScene(game))
    game.setScene("TestScene")
    game.main()