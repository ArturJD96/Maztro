from mingus.midi import fluidsynth
import time

fluidsynth.init('FluidR3_GM/FluidR3_GM.sf2')

fluidsynth.play_Note(64,0,100)
time.sleep(1)
fluidsynth.play_Note(64,0,0)