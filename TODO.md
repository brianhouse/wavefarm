values from motion detector are a bit questionable

/

raspis are keeping no memory; if no connection, data is lost

a separate generic event sender powered via beanstalk would make sense. 
process the data in a thread off the main listener, but use beanstalk to cache the communication.

/

should really have range checks on all inputs, especially from apis, a la rain

/

eventually, hardlinks to library files

/

rain is a complicated thing. it's kind of an event, though one that can last for days.
the cumulative / amount thing, in any case, isnt totally hacking it, can take this out when generalizing.
add humidity instead.

//



need event rhythms in there!
need a call to bells --