## changes

- better naming?
    unify callback syntax
    dont use callback, use on_end
- unify breakpoint and signal
- have to pay attention to resolution -- maybe auto interpolate? should not have to worry about scaling
- tween should be an object that is passed (Tween factory in tween, not in Voice method)
- tween -> interp
- need mute
- how do accidentals work in pattern? and they are awkward in lilypond output
- phase locking between voices
- need voice mute function
- lilypond should take a template filename, and fill in the score data, and auto-run lilypond
- could add a key listener so that midi-offs are still sent to avoid panics all the time
- should add some versioning
- use libpd and get the BasicMidi interface embedded (will help with raspi)


## bugs
uh oh -- skipping the driver doesnt skip the tweens. not sure how that's going to get fixed.

start_t = driver.t - driver.skip   # or something?


## tempo
seem to be taking the approach where everything runs independently
