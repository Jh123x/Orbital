class Sound(object):
    def __init__(self, sound_dict:dict, start_state:bool, volume:float, debug:bool):
        """Main class for playing sounds"""

        #Store the values for the sound
        self.sounds = sound_dict

        #Store if it is enabled or not
        self.enabled = start_state

        #Store the volume of the sound
        self.volume = volume

        #Set the debug
        self.debug = debug

    def get_state(self) -> bool:
        """Get the current state of the sound"""
        return self.enabled

    def get_volume(self) -> float:
        """Return the volume level of the sound"""
        return self.volume

    def volume_toggle(self) -> None:
        """Toggles the volume of the sound"""

        #If the volume is lower than 1
        if self.volume < 1:

            #Increment it by 0.25
            self.volume += 0.25

        #Otherwise
        else:
            
            #Go back to 0.25
            self.volume = 0.25

    def get_dict(self) -> bool:
        """Get the dictionary of the sounds"""
        return self.sounds

    def play(self, key:str) -> bool:
        """Play the sound based on the key that is given"""
        #Get the sound from the dictionary
        sound = self.sounds.get(key, False)

        #If the sound is found
        if sound:

            #If music is not diabled
            if self.enabled:

                #Set the volume
                sound.set_volume(self.volume)

                #Play it
                sound.play()

                return True

        #Otherwise
        else:

            #It is an invalid key
            if self.debug:
                print("Invalid key")

        return False

    def toggle(self) -> None:
        """Toggle the enabled status of sound"""
        self.enabled = not self.enabled
        