# abstract
class Scene:

    def __init__(self,game,name):
        self.game = game
        self.name = name
        self.id = len(self.game.scenes)
        self.game.scenes.append(self)
        self.game.scene_names.append(name)

    # instance methods to override
    def start    (self)       : pass
    def update   (self,dt)    : pass
    def display  (self)       : pass
    def keyboard (self,k,x,y) : pass
    def special  (self,k,x,y) : pass

    def tostring(self):
        return "Scene " + str(self.id) + ": " + self.name
    __str__ = tostring
    __repr__ = tostring