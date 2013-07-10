values from motion detector are a bit questionable

/

raspis are keeping no memory; if no connection, data is lost

a separate generic event sender powered via beanstalk would make sense. 
process the data in a thread off the main listener, but use beanstalk to cache the communication.

/

should really have range checks on all inputs, especially from apis, a la rain

/

eventually, hardlinks to library files

//

bell sets are working

so for each voice, will have to adjust the envelopes individual to fit the tone

TIDE strike still needs some help