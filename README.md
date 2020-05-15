# stalk-market-queue

This is a project inspired by some people stuck indoors for far too long, having to rely on... *unstable* internet connections.

When someone drops a juicy turnip price in our stalk market discord, well, we need some organization.  We need a **queue.**  

Command | Arguments | Explanation | Example
--- | --- | --- | ---
```!queue``` | code (optional) | Starts a new queue.  Optionally pass in the ```code``` argument to set a Dodo Code in the pinned message that is generated by the bot. | ```!queue DS57R```
```!add```  | user (optional) | Adds a new member to the queue.  Optionally pass in the ```user``` argument to add _them_ to the queue; defaults to user calling the command if no argument is passed in. | ```!add @TomNook```
```!next```  | none | Moves to the next user in the queue.  Mentions the next user to get their attention. | ```!next```
```!endqueue```  | none | Clears and ends the queue. | ```!endqueue```
```!dodo``` | code (required) | Edits the current queue with a new Dodo Code.  The ```code``` argument must be passed into this command. | ```!dodo TC88Q```