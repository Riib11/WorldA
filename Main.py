from Game import Game
from Author import start

args = {
    "name"    : "Test Game",
    "width"   : 800,
    "height"  : 800,
    "dt"      : 1,
    "keycaps" : [
                    b'a',b'd',b'w',b's',b'q',b'e'
                ]
}

# run display main
if __name__ == '__main__':
    game = Game(args)
    start(game)