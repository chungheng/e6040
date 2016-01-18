# A Brief Introduction to Git - E6040 Spring 2016

Git is a version control system for source code management. It was
initially designed and created by Linux developers for Linux Kernel development.
Nowadays, Git is widely-used in open source community as well as in many private
organizations. If this is your first time heard of Git, you probably would like
to start by reading the official [Git documentation](http://git-scm.com/documentation).

While there are many Git-based systems, such as Github or GitLab, we will
be using [BitBucket](https://bitbucket.org/) in this course. BitBucket allows
user to create unlimited numbers of _private_ repositories. If you have not
had a BitBucket account yet, please create *one*. All homework submission
will be done on BitBucket **_only_**.

**Please email your BitBucket ID along with your UNI to the email address
ecbme6040.columbia AT gmail dot com**.

For each homework assignments, the TA will create a private Git repository
for you, and then grant its access to you. Please DO NOT create any
repositories on your own and share them with the TA. Only the repositories
created by the TA will be graded.

### Installing and Configuring Git on EC2

Installing Git on EC2 is very simple. Type the following command in the
terminal,

```bash
sudo apt-get install git
```

Before you start using Git, you need to configure it. Create (or edit) the file
`~/.gitconfig` with the following content,

```bash
[user]
        name = YOUR_NAME_HERE
        email = YOUR_EMAIL_HERE
[color]
        diff = auto
        status = auto
        branch = auto
[push]
        default = matching
```

Note that `name` and `email` should be the same as on BitBucket.

### Git Work Flow

Git provides over a hundred of operations. In this course, you
will be mainly using `clone`, `diff`, `add`, `status`, `commit`, and `push`.

#### Clone
For each homework, you will start by making a local copy of the
homework repository on EC2. Use the following command,

```bash
git clone https://YOUR_ID@bitbucket.org/E6040TA/hw_#_YOUR_UNI.git
```
or
```bash
git clone git@bitbucket.org/E6040TA/hw_#_YOUR_UNI.git
```

If you use the `https` link, you will be prompted to enter your
BitBucket `ID` and `password`. If you use the `ssh` link, you
need to create a `ssh`key pair. You can find instructions on
setting up ssh key for BitBucket
[here](https://confluence.atlassian.com/bitbucket/set-up-ssh-for-git-728138079.html).

#### Diff, Add, Commit
After you update the homework repository, you can use `git diff` to see what
you have changed,

```bash
git diff [file]
```

If you think a file (or files) is ready to commit, use the `git add` to stash
it,

```bash
git add file [file1 file2 ...]
```

You can see what you are about to commit by using `git diff` with an extra flag,

```bash
git diff --cached
```

After making some changes, commit all stashed files,

```bash
git commit -m "MESSAGE"

```

Replace `"MESSAGE"` with a short sentence of commit summary. Informative commit
summary will help you remember what you have done before. Each commit has
a time stamp. You can commit at any time, but the TA will only grade the
commits before the deadline.

You can use `git status` to monitor your work. It prints a summary of revision,
files that have been modified, files that have been stashed, etc. In particular,
use it before commit to ensure you have everything correct.


#### Push

After several commits, you would like to upload the updated repository onto
BitBucket. Use the following command,

```bash
git push
```

Some information will be printed out. Make sure that you successfully push the
repository.

#### Summary of Work Flow

```bash
git clone LINK_TO_REPOSITORY # download the homework repository

[... make some changes ...]

git diff                     # see what you have modified
git add file1 file2          # see stashed files
git diff --cached            # see what you are about to commit
git commit -m "MESSAGE"      # commit changes


[... make some changes ...]

git status                   # monitor your work

[... a few commits later ...]

git push                     # upload your local changes onto BitBucket
```

### Checking your submissions
Once you `push` local changes, you can use the BitBucket web interface to
review your commits. Please make sure that you have what you intend to submit
on BitBucket.

### Commit Often, Commit More
We can not emphasize how important it is to commit frequently. Try to do
homework incrementally, and commit small changes as often as possible.
