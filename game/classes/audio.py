import pygame

class Audio:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.set_num_channels(4)
        self.channel_music = pygame.mixer.Channel(0)
        self.channel_player = pygame.mixer.Channel(1)
        self.channel_enemy = pygame.mixer.Channel(2)
        self.channel_other = pygame.mixer.Channel(3)
        self.audio_map = {}
        
        self.walk_playing = False

    def load_audio(self, name, filename):
        sound = pygame.mixer.Sound(filename)
        self.audio_map[name] = sound

    def play_music(self, name):
        if name in self.audio_map:
            music = self.audio_map[name]
            self.channel_music.play(music, -1)
            print('playing ', name)

    def play_player(self, name):
        if name in self.audio_map:
            sfx = self.audio_map[name]
            
            if not self.channel_player.get_busy():
                if name == 'player_walk':
                    self.channel_player.play(sfx)
                    self.walk_playing = True

            elif self.channel_player.get_sound() == self.audio_map['player_walk']:
                #print('JOJFJPFJPFJDSP')
                if name == 'player_jump':
                    self.channel_player.play(sfx)
                elif name == 'player_land':
                    self.channel_player.play(sfx)

                print('sound ', name)

    def play_enemy(self, name):
        if name in self.audio_map:
            sfx = self.audio_map[name]
            if not self.channel_enemy.get_busy():
                self.channel_enemy.play(sfx)

            elif self.channel_enemy.get_sound() == self.audio_map['vamp_walk']:
                if name == 'vamp_jump' or name == 'vamp_land':
                    self.channel_enemy.play(sfx)

            print('sound ', name)


    def play_other(self, name):
        if name in self.audio_map:
            sfx = self.audio_map[name]
            if not self.channel_other.get_busy():
                self.channel_other.play(sfx)

    def stop_music(self):
        self.channel_music.stop()

    def stop_player(self):
        self.channel_player.stop()
        self.walk_playing = False

    def stop_enemy(self):
        self.channel_enemy.stop()

    def stop_other(self):
        self.channel_other.stop()
    
    def stop_walk(self):
        if self.walk_playing:
            self.channel_player.stop()
            self.walk_playing = False

    def fadeout_music(self):
        self.channel_music.fadeout(3000)