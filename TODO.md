* write a function to detect which tweet was the last and previous
* run main in a loop to look for new tweets
* write log parser to discover failed downloads
* write log analysys tool to graph download statistics

So now there are two processes that run on a schedule...great!

## Number one

Let's call this one the SiteDownloader because it uses the official website at ubuweb.com. It's job is to load up all the wacky rules I defined in the models.py classes and go through every link in the film index page and try really hard to download all of them. After the initial archive is seeded, following runs will scan through everything but not download files with the same name. it's literally just looking for file existance.

## Number two

KG posts stuff to Twitter pretty often, with a single link to the ubuweb.com page for the content. This could corespond to the Work class in the models file but the result from twitter is just a URL. So I guess it's closer to a Page. Perhaps my models might need some adjustment.

Anyhoo, the goal is to have a twitter.py process running with an async poll interval of like...maybe 1 hour...and then do a check for the latest tweet against the previous one. PROBABLY NEED A QUEUE type thing for this and some kind of database to answer the question of "do we already have this content?"

To make it a little more challenging, sometimes the works posted on Twitter are already in the artists index or on the artist's page. But sometimes...they are not!
