## :pushpin: Quick Start
1. Download a text editor such as [VSCode], [Atom], or the [GitPod online editor].

[VSCode]: https://code.visualstudio.com/
[Atom]: https://atom.io/
[GitPod online editor]: https://www.gitpod.io/

2. If you are using Gitpod, open Gitpod and link your GitHub account. If you want to make changes to GitHub from Gitpod, go to settings and enable writing to public repositories.
Then skip to step 5.

3. If you are using a local editor such as VSCode or Atom, download [git](https://git-scm.com/downloads).
 
4. Run the following command to download this repository to your computer (in `terminal` on OS X or Linux, in `cmd` for Windows)
```bash
$ git clone https://github.com/rockvillerobotics/Incredibots2020.git
```

4. If you haven't already, take a brief look at [how git works](https://guides.github.com/introduction/git-handbook/)

5. Now, you're all set :smile:

## :rocket: Contribution Guide
Let's say you want to add a new feature to the code. Here are the steps you would follow (assuming you use `git` from the command line):

1. Make a [GitHub issue](https://github.com/rockvillerobotics/Incredibots2020/issues) describing the feature. Write enough info so that someone else could complete the task just by reading through your description.
2. In terminal, navigate to your local `Incredibots2020` folder and run
```bash
$ git checkout master # Switch branches to `master` (if you're not already there)
$ git pull            # Pull down changes from the remote Incredibots2020 repository (on github.com)
```
3. Now, make a new branch off of `master` for your feature. For example, if you were designing a new implementation for the Gryo sensor, you might run the following:
```bash
$ git branch redesign-gyro   # Create a new branch called `redesign-gyro`
$ git checkout redesign-gyro # Change the current working branch (from `master` to `redesign-gyro`)
```
or (equivalently)
```bash
$ git checkout -b redesign-gyro # Create a new branch called `redesign-gyro` and check it out
```
4. Make the feature!!!
5. Once the feature is ready, it's time to make your code official. First you have to **stage** your code using `git add` (which tells git which file changes you want to include in your code snapshot), then you `git commit` your changes (to save/take the snapshot of the files you just staged):
```bash
$ git add FILE_YOU_EDITED ANOTHER_FILE_YOU_EDITED
$ git commit -m "Write a descriptive commit message that describes all of the changes you made"
```
> Note that instead of manually calling `git add` on all the files, you can also use `git add .` to add all the files in the current directory.
6. After you've commited all your changes, it's time to send the code up to GitHub so everyone on the team has access. To do that, run
 ```bash
 $ git push # Sends all of your commited changes to the remote (github.com)
 ```
 This command might throw an error because the branch isn't currently tracked by github. In that case, it will show you a command to run, which looks something like this:
 ```bash
 $ git push --set-upstream origin home-page
 ```
 7. Now, you should see a new branch on github with your new changes.
 8. If you think your code is ready to go into the app, it's time to submit a pull request (from your feature branch into master). To do so, click on the `Pull Requests` tab at the top of the repository and submit a new `Pull Request`.
 9. DON'T merge in your own pull request, even if you think it is ready. Someone else will review the changes you made and provide you with feedback. If you need to make new changes to address the feedback, make them on your local version of the branch and continue pushing changes to github. Your pull request will update with the new changes automatically.
 10. Eventually... your pull request will be accepted! After that, you can start working on the next set of features :)

 ### About Using the command line
 If you use GitHub Desktop or VSCode to handle your git operations graphically, the above steps won't be much different (just click the buttons corresponding to the operations described here).

 ## :link: Useful Links
 - [Git Introduction](https://guides.github.com/introduction/git-handbook/)
 - [Intro to HTML and CSS](http://learn.shayhowe.com/html-css/)
 - [Very good (but super long) web dev course](http://www.freecodecamp.com/)
 - [Flask video tutorials by sentdex](https://pythonprogramming.net/practical-flask-introduction/)

