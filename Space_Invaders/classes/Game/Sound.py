class Sound(object):
    def __init__(self, sound_dict:dict, start_state:bool, debug:bool):
        """Main class for playing sound"""

        #Store the values for the sound
        self.sounds = sound_dict

        #Store if it is enabled or not
        self.enabled = start_state

    def get_state(self) -> bool:
        """Get the current state of the sound"""
        return self.enabled

    def get_dict(self) -> bool:
        """Get the dictionary of the sounds"""
        return self.sounds

    def play(self, key:str) -> None:
        """Play the sound based on the key that is given"""
        #Get the sound from the dictionary
        sound = self.sounds.get(key, False)

        #If the sound is found
        if sound:

            #If music is not diabled
            if self.enabled:

                #Play it
                sound.play()

        #Otherwise
        else:

            #It is an invalid key
            if self.debug:
                print("Invalid key")


    def toggle(self) -> None:
        """Toggle the enabled status of sound"""
        self.enabled = not self.enabled
        