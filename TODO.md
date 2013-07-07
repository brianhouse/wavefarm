raspis are keeping no memory; if no connection, data is lost

/////

scale is 60:1
one minute becomes one second, etc.
one second becomes 60hz, which is about musical time. (16ths at 120bpm is 32hz)

/////

two types of data: continuous measurements, and discrete events, reflected in the model

'readings' just have a value. if the value repeats, we will assume it's constant. intended to be resampled.
readings are taken every 5 minutes (-> 5 seconds)

'events' have a start, a stop, and an intensity. they also have a quality.
events are quantized to every second (32nd note)

