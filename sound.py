from pygame import mixer

 
class Mixer:
    DIR = 'assets/sound'
    
    def __init__(self) -> None:
        mixer.init()
        self.mixer = mixer
        
        self.menu_music = 'assets/sound/start_menu.wav'
        self.game_music = 'assets/sound/game_music.mp3'
        self.game_over = 'assets/sound/beatz.wav'
        self.mixer.music.load(self.menu_music)
        
        self.pencil = self.mixer.Sound('assets/sound/writing-pencil.wav')
        self.teacher = self.mixer.Sound('assets/sound/male-yelling.wav') 
    
    def set_music(self, start: bool = False, gameOver: bool = False, isPlaying: bool = True) -> None:
        if start:
            self.mixer.music.load(self.menu_music)
            self.mixer.music.play(-1)
        if gameOver:
            self.mixer.music.load(self.game_over)
            self.mixer.music.play(-1)
        else:
            self.mixer.music.load(self.game_music)
            self.mixer.music.play(-1)
        
    def yell(self, stop: bool = False, volume: float = None) -> None:
        if volume and volume > 0:
            volume = min(float(volume), 1.0)
            self.teacher.set_volume(volume)
        self.teacher.play() if not stop else self.teacher.stop()
    
    def writing(self, volume: float = None, stop: bool = False):
        if volume and volume > 0:
            volume = min(float(volume), 1.0)
            self.pencil.set_volume(volume)
        self.pencil.play(-1) if not stop else self.pencil.stop()