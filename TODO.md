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


process lives on the server.
play makes the call, downloads the result (which isnt stored), does its thing.
easy peasy.


auto generate before the hour. then post to s3. have a download page.

have a cron in the studio. pulls the latest a (copy?) and plays (applescript).
