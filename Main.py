import Game
import Author

args = {
    "name"          : "Test Game",
    "width"         : 800,
    "height"        : 800,
    "fullscreen"    : False,
    "dt"            : 1,
    "keycaps"       : [
                        b'a',b'd',b'w',b's',b'q',b'e',b'j',b'k',b'l',b'i',b'g',b'f',b't',b'h',
                        b'1',b'2',b'3',b'4',b'5',b'6'
                    ]
}

# run display main
if __name__ == '__main__':
    game = Game.Game(args)
    Author.start(game)