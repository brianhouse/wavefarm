raspis are keeping no memory; if no connection, data is lost

a separate generic event sender powered via beanstalk would make sense. 
process the data in a thread off the main listener, but use beanstalk to cache the communication.

/

eventually, hardlinks

/

rain is not generating much except errors, cumulative might not be working correctly