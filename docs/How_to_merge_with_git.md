=====================
How to merge with git
=====================

The repo is organized in one main branch:

 - master (production)
 
Master is _always_ deployable and _it_ is deployed.

Anything else which is being working on shuold be in its own _named_ branch, stemming of 
master.

This blog post here: http://scottchacon.com/2011/08/31/github-flow.html explains how it is done.

For example with a brand new clone you'll have something close to this:

	mattions@triton:ssouk_web(fixing_doc)$ git branch -a
	  adding-uniform-validation
	* fixing_doc
	  master
	  remotes/origin/adding-uniform-validation
	  remotes/origin/fixing_doc
	  remotes/origin/master

Note that for sure you will have the master branch, the remote master branch (remotes/origin/master) and several 
_named branches_ which are giving you the idea of what is going on the repo. 
The more the name is specific the best is, so it's easier to know what people are working on.

You can always see what is being working on checking this pages https://github.com/ssouk/ssouk_web/branches

Creating a new named branch, exporting on the server
============================================

Opening a new topic branch 
--------------------------

    git checkout master # switch to master branch
    git pull # get the latest 
    git checkout -b my_topic_branch # create a new branch
	git push origin my_topic_branch # pushing the branch on the server.
    # hacking time!

Now when you ready to merge it back, or you want to have your code reviewed you open a Pull Request!
(Point number 4 on this blog post http://scottchacon.com/2011/08/31/github-flow.html

When ppl say it's good to be merged, do it!

    git checkout master # Back to master
    git pull master # Get always the latest before rebasing.
    git checkout my_topic_branch # Back to my_topic_branch
    git rebase master # Adding my stuff on top of the latest master
    git checkout master # Back to the master
    git merge my_topic_branch --no-ff # Merging and recording which branch
    git push # push everything online

Merge and publish as soon as possible, even small stuff.
More info on the rebase are here: http://learn.github.com/p/rebasing.html

Git is cool, you'll love it soon.

Deploy on godor infrastructure
==============================

We deploy on Gondor so far. 

https://gondor.io/

*Write me!*


Working with git
================

If you new to git, have a look around on this website:

- http://help.github.com/
- http://progit.org/
- http://git-scm.com/


Git prompt
---------

It's very useful to have a git prompt to always know what's going on and where you are.
If you use bash, slap this into your .bashrc 

	function parse_git_dirty {
  [[ $(git status 2> /dev/null | tail -n1) != "nothing to commit (working directory clean)" ]] && echo "*"
	}
	function parse_git_branch {
	  git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e "s/* \(.*\)/(\1$(parse_git_dirty))/"
	}
	
	export PS1='\u@\h \[\033[1;33m\]\w\[\033[0m\]$(parse_git_branch)$ '
	
	#grey
	PS1='\[\033[0;32m\]\u\[\033[1;32m\]@\[\033[0;32m\]\h\[\033[00m\]:\[\033[01;34m\]\W\[\033[1;30m\]$(parse_git_branch)\[\033[00m\]\$ '


Quick Git intro
------


You already have _my topic branch_ and you are in that brranch. 
So you're in the Hacking time!

what you do usually is

	Hack Hack Hack
	$ git commit -am "I've done this and I'm explaining it on the commit message"
    Hack Hack Hack
	$ git commit -am "I've done something else and I'm writing it on this message!"
    $ git push # This push your local thing, online so it's on the github server and it's back up and ppl know!

Enjoy and thanks for reading so far :) 

