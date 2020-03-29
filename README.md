# Azur Lane Sorter

So how did this little thing happen? I got bored and was playing Azur Lane. Team comp can be tough (especially for noobs like me) which is why I thought to make this little script to help determine what my comp should be. 

## Current Design
* Use the LV 100 stats from Azur Lane Wiki (see data_scrape.py)
* Put them into a data file
* Import them and sort to produce the best formation based on user's preference
* Able to filter based on class, nation, and rarity... wanna make it better
  instead of having to call the function multiple times
* TODO: Set bounds on number of each class needed (i.e. # of Carriers or Battleships)
* Produce the ideal formation
