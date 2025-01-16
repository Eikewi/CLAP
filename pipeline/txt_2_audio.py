txt = '''
Der Himmel erscheint uns blau aufgrund eines Phänomens namens Streuung, das auftritt, wenn Sonnenlicht mit den winzigen Molekülen der Gase in der Atmosphäre interagiert. Hier ist eine vereinfachte Erklärung:
	1.	Sonnenlicht tritt in die Erdatmosphäre ein: Wenn die Sonne scheint, sendet sie ein breites Spektrum elektromagnetischer Strahlung aus, einschließlich sichtbarem Licht, ultravioletter (UV) Strahlung und infraroter (IR) Strahlung.
	2.	Streuung tritt auf: Während das Sonnenlicht durch die Atmosphäre reist, trifft es auf winzige Moleküle von Gasen wie Stickstoff (N2), Sauerstoff (O2) und anderen. Diese Moleküle sind viel kleiner als die Wellenlänge des Lichts, sodass sie die kürzeren (blauen) Wellenlängen effizienter streuen als die längeren (roten) Wellenlängen.
	3.	Blaues Licht wird in alle Richtungen gestreut: Das gestreute blaue Licht wird dann in alle Richtungen verteilt und erreicht unsere Augen aus allen Teilen des Himmels. Deshalb erscheint der Himmel tagsüber blau.
	4.	Rotes Licht reist weiterhin geradeaus: Die längeren Wellenlängen des roten Lichts und der infraroten Strahlung hingegen reisen relativ geradeaus, ohne so stark gestreut zu werden. Daher sehen wir mehr Rottöne und Orangen bei Sonnenaufgang und Sonnenuntergang.

Zusammenfassend lässt sich sagen, dass der Himmel blau erscheint, weil das Sonnenlicht von den winzigen Molekülen in der Atmosphäre gestreut wird, wobei kürzere (blaue) Wellenlängen den längeren (roten) Wellenlängen bevorzugt werden.
'''

import pyttsx3

def init_audio():
    return pyttsx3.init()

def tts_process(tts_queue):
    """Separater Prozess für die TTS-Engine."""
    engine = pyttsx3.init() # can not be refactored, because engine can not be pickled
    engine.setProperty('rate', 165)

    while True:
        text = tts_queue.get()
        if text is None:  # signal to end process
            break
        #print(f"TTS verarbeitet: {text}")
        engine.say(text)
        engine.runAndWait()

def create_audio(text, tts_queue):
    # Initialisieren des TTS-Engines
    tts_queue.put(text)

#available Languages:
'''
US:

Voice: Albert | ID: com.apple.speech.synthesis.voice.Albert | Language: ['en_US']
Voice: Bad News | ID: com.apple.speech.synthesis.voice.BadNews | Language: ['en_US']
Voice: Bahh | ID: com.apple.speech.synthesis.voice.Bahh | Language: ['en_US']
Voice: Bells | ID: com.apple.speech.synthesis.voice.Bells | Language: ['en_US']
Voice: Boing | ID: com.apple.speech.synthesis.voice.Boing | Language: ['en_US']
Voice: Bubbles | ID: com.apple.speech.synthesis.voice.Bubbles | Language: ['en_US']
Voice: Cellos | ID: com.apple.speech.synthesis.voice.Cellos | Language: ['en_US']
Voice: Wobble | ID: com.apple.speech.synthesis.voice.Deranged | Language: ['en_US']
Voice: Eddy (Englisch (USA)) | ID: com.apple.eloquence.en-US.Eddy | Language: ['en_US']
Voice: Flo (Englisch (USA)) | ID: com.apple.eloquence.en-US.Flo | Language: ['en_US']
Voice: Fred | ID: com.apple.speech.synthesis.voice.Fred | Language: ['en_US']
Voice: Good News | ID: com.apple.speech.synthesis.voice.GoodNews | Language: ['en_US']
Voice: Grandma (Englisch (USA)) | ID: com.apple.eloquence.en-US.Grandma | Language: ['en_US']
Voice: Grandpa (Englisch (USA)) | ID: com.apple.eloquence.en-US.Grandpa | Language: ['en_US']
Voice: Jester | ID: com.apple.speech.synthesis.voice.Hysterical | Language: ['en_US']
Voice: Junior | ID: com.apple.speech.synthesis.voice.Junior | Language: ['en_US']
Voice: Kathy | ID: com.apple.speech.synthesis.voice.Kathy | Language: ['en_US']
Voice: Organ | ID: com.apple.speech.synthesis.voice.Organ | Language: ['en_US']
Voice: Superstar | ID: com.apple.speech.synthesis.voice.Princess | Language: ['en_US']
Voice: Ralph | ID: com.apple.speech.synthesis.voice.Ralph | Language: ['en_US']
Voice: Reed (Englisch (USA)) | ID: com.apple.eloquence.en-US.Reed | Language: ['en_US']
Voice: Rocko (Englisch (USA)) | ID: com.apple.eloquence.en-US.Rocko | Language: ['en_US']
Voice: Samantha | ID: com.apple.voice.compact.en-US.Samantha | Language: ['en_US']
Voice: Sandy (Englisch (USA)) | ID: com.apple.eloquence.en-US.Sandy | Language: ['en_US']
Voice: Shelley (Englisch (USA)) | ID: com.apple.eloquence.en-US.Shelley | Language: ['en_US']
Voice: Trinoids | ID: com.apple.speech.synthesis.voice.Trinoids | Language: ['en_US']
Voice: Whisper | ID: com.apple.speech.synthesis.voice.Whisper | Language: ['en_US']
Voice: Zarvox | ID: com.apple.speech.synthesis.voice.Zarvox | Language: ['en_US']

DE:

Voice: Anna | ID: com.apple.voice.compact.de-DE.Anna | Language: ['de_DE']
Voice: Eddy (Deutsch (Deutschland)) | ID: com.apple.eloquence.de-DE.Eddy | Language: ['de_DE']
Voice: Flo (Deutsch (Deutschland)) | ID: com.apple.eloquence.de-DE.Flo | Language: ['de_DE']
Voice: Grandma (Deutsch (Deutschland)) | ID: com.apple.eloquence.de-DE.Grandma | Language: ['de_DE']
Voice: Grandpa (Deutsch (Deutschland)) | ID: com.apple.eloquence.de-DE.Grandpa | Language: ['de_DE']
Voice: Reed (Deutsch (Deutschland)) | ID: com.apple.eloquence.de-DE.Reed | Language: ['de_DE']
Voice: Rocko (Deutsch (Deutschland)) | ID: com.apple.eloquence.de-DE.Rocko | Language: ['de_DE']
Voice: Sandy (Deutsch (Deutschland)) | ID: com.apple.eloquence.de-DE.Sandy | Language: ['de_DE']
Voice: Shelley (Deutsch (Deutschland)) | ID: com.apple.eloquence.de-DE.Shelley | Language: ['de_DE']

'''



