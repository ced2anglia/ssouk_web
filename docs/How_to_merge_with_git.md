=====================
How to merge with git
=====================

The repo is organized in one main branch for now:

 - master (develpment)
 - production (production)
 
Read this blog post http://nvie.com/posts/a-successful-git-branching-model/ 
If not online I've saved in this directory and it's called 
"A_succesful_Git_branching_model.html". This should explain which way are we 
following to hack on stuff.

**Important** You want always to work on your local branch that is _not_ tracking 
a remote one. If you don't follow this, there will be pain.

For example with a brand new clone you'll have

    mattions@triton:ssouk_web(master)$ git branch -a
    * master
      remotes/origin/HEAD -> origin/master
      remotes/origin/master

This means you are in the master branch, which is tracking the origin/master
You _do not develop directly on this branch_.

You create a my_topic_branch (call it local, if your short of name) and work 
there and then follow the following method to bring your stuff in master (which is 
the only one that lives on-line.)

Got no time dude, just tell me how to merge
===========================================

Scenario (i): Got already the topic branch
--------------------------------------

You've done stuff and you want to merge with the master 


    git checkout master # switch to master branch
    git pull # get the latest 
    git checkout my_topic_branch # switch to my local branch
    git rebase master # Adding my stuff on top of the latest master
    git checkout master # Back to the master
    git merge my_topic_branch --no-ff # Merging and recording which branch
    git push # push everything online


Scenario (ii): Opening a new topic branch 
--------------------------------------

    git checkout master # switch to master branch
    git pull # get the latest 
    git checkout -b my_topic_branch # create a new branch
    # hack hack hack
    git checkout master # Back to master
    git pull master # Get always the latest before rebasing.
    git checkout my_topic_branch # Back to my_topic_branch
    git rebase master # Adding my stuff on top of the latest master
    git checkout master # Back to the master
    git merge my_topic_branch --no-ff # Merging and recording which branch
    git push # push everything online

Merge and publish as soon as possible, even small stuff.

Pushing local branch online
---------------------------

Sometimes you have a local branch which has gone through a lot of new things
and maybe you just want to push it online for backup reason, or to make it 
available to other ppl to check it out and can't merged back into master.

Think about this again. Ok, no merging? Right, let's push it online.

To do that just

    git checkout my_topic_branch
    git push origin my_topic_branch
    
This should create a new branch under origin and now the repo should have two 
branches: master and my_topic_branch

To check your local branch is online just do

    git branch -a
    
It's always a good idea to merge this thing back into `master` ASAP and remove the 
branch from the repo.

Merge following the Scenario (i) and then remove the branch online

    git push origin :my_topic_branch
    
You can keep the local branch for further development and fall back to Scenario (i).

Read the html page why this is so cool, or make a leap of faith.
More info on the rebase are here: http://learn.github.com/p/rebasing.html

Git is cool, you'll love it soon.
