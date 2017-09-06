"""
Repository Manager for creating and managing Git repository on Bitbucket

This package requires:

1. git-spindle extension (https://github.com/seveas/git-spindle)
2. SSH authentication method for communicating with BitBucket. Make sure that
   "ssh-agent" is running, and a RSA key pair is added locally and remotely.

"""

import argparse
import pandas as pd
import os, shutil
import subprocess as sp


class RepoManager(object):
    def __init__(self, filename, ta_account, ta_email="ta@columbia.edu",
        ta_name="TA", directory=None):
        """
        Repository Manager

        Input
        =====
        filename: string

        ta_account: string
            BitBucket account of the TA. This account is the owner of all
            students' repositories.

        ta_email: string
            Email address of the TA. Git requires an email address.

        ta_name: string
            Name of the TA. Git requires a name.

        directory: string
            Path to the directory where the student repositories reside. If not
            given, use the current working directory.
        """
        self.ta_account = ta_account
        self.ta_email = ta_email
        self.ta_name = ta_name

        self.studentDataFrame = self._read_student(filename)

        # directory where student repositories reside.
        self.pwd = directory or os.getcwd()

    def _read_student(self, filename):
        """
        Read student information from a csv file.

        Input
        =====
        filename: string
            path to the csv file. Each row of the file should follow the format,

            ---
            Name,UNI,Bitbucket username
            John Doe, jd0000, jd0000bitbucket
            ...
            ---

            Note that the first row is mandatory.

        Return
        ======
        pf: pandas DataFrame
            A DataFrame with three columns, "Name", "UNI", and
            "Bitbucket username."
        """
        assert(os.path.exists(filename))
        pf = pd.read_table(filename, sep=r',', skipinitialspace=True)
        assert(not pf.empty)
        assert({"Name", "UNI", "Bitbucket username"}.issubset(pf.columns))
        return pf

    def _set_repo_bitbucket(self):
        """
        Create remote repository on BitBucket. Note this function should only be
        called when the current working directory is a Git repository.
        """
        sp.call(["git","bb","--account=%s" % self.ta_account,"create","--private"])
        sp.call(["git","push","-u","origin","master"])

    def _grant_access(self, studata, access):
        """
        Change access privilege of a student. Note this function should only be
        called when the current working directory is a Git repository.

        Input
        =====
        studata: tuple
            ("uni", "name", "BitBucket_id" )

        access: string
            "write" or "read"
        """
        if access == "write":
            access = "--write"
        elif access == "read":
            access = "--read"
        else:
            raise Exception('unknow privilege: %s' % access)
        sp.call(["git","bb","add-privilege",access,studata["Bitbucket username"]])

    def _remove_access(self, studata):
        """
        Remove access privilege of a student. Note this function should only be
        called when the current working directory is a Git repository.

        Input
        =====
        studata: tuple
            ("uni", "name", "BitBucket_id" )
        """
        sp.call(["git","bb","remove-privilege",studata["Bitbucket username"]])

    def _pull_repo(self):
        """
        Pull repository from the origin. Note this function should only be
        called when the current working directory is a Git repository.
        """
        sp.call(['git','pull'])

    def _create_repo(self, studata):
        """
        Initialize and Create Repository on BitBucket

        Input
        =====
        studata: tuple
            ("uni", "name", "BitBucket_id" )
        """
        # if .git exists, remove it
        if os.path.exists(".git"):
            sh.rmtree(".git")
        sp.call(["git","init"])
        sp.call(["git","config","--local","user.name", self.ta_name])
        sp.call(["git","config","--local","user.email", self.ta_email])
        sp.call(["git","add","*"])
        sp.call(["git","commit","-m","Init repo for " + studata['UNI']])

    def _add_branch(self, branchname):
        """
        Create a new branch. Note this function should only be
        called when the current working directory is a Git repository.

        Input
        =====
        branchname: string
            Name of the branch to be created.
        """
        sp.call(['git','checkout','-b',branchname])

    def _checkout_branch(self, branchname):
        """
        Switch to an existing branch. Note this function should only be
        called when the current working directory is a Git repository.

        Input
        =====
        branchname: string
            Name of the branch.
        """
        sp.call(['git','checkout',branchname])

    def _update_files(self, fileList, remoteFileList):
        """
        Aassuming that absolute path of files are stored filelists

        Input
        =====
        fileList: list
            A list of file names to copy to.

        remoteFileList: list
            A list of file names to be copy from.

        Note that the entries in fileList and entries remoteFileList
        have one to one correspondence, ex.

            fileList = ["foo/foo.py", ...]
            remoteFileList = ["remote/goo/goo/foo.py"]
        """
        for remotefile, localfile in zip(remoteFileList, fileList):
            assert(os.path.isfile(remotefile))
            assert(!os.path.isfile(localfile))
            sp.call(['cp', remotefile, localfile])
            sp.call(['git','add', localfile])

    def _commit_and_push_branch(self, branchname, msg=None, push=True):
        """
        Commit the local change, and push to remote.

        TODO: the inteface of this function needs rework.

        Input
        =====
        branchname: string
            Name of the branch.

        msg: string
            Commit message.

        push: bool
            Whether to push or not.
        """
        if msg is None:
            msg = 'Create branch: {0}'.format(branchname)
        sp.call(['git','commit','-m',msg])
        if push:
            sp.call(['git','push','origin',branchname])

    def create_student_repo(self, dirpath, dirname=""):
        """
        Create student repository locally and remotely.

        Input
        =====
        dirpath: string
            Path to the skeleton repository, ex: path/to/homeworks/hw4

        dirname: string
            Prefix of the student repository. For example, if "dirname" is
            "e6040_hw4", the student repository will be "e6040_hw4_uni0000."
            If dirname is not set, the last part of "dirpath" will be used.

        """
        assert(os.path.exists(dirpath))

        # navigate to the directory where student repositories locate
        os.chdir(self.pwd)

        seg = dirpath.split('/')
        if seg[-1]:
            seg = seg[-1]
        else:
            seg = seg[-2]
        stuDirTemplate = (dirname or seg) + '_{0}'

        for _, studata in self.studentDataFrame.iterrows():
            studirname = stuDirTemplate.format(studata['UNI'])

            # TODO: need to check if the repo exists on BitBucket
            if os.path.exists(studirname):
                print "%s already exists... skip" % studirname
                continue

            # copy homework skeleton to student specific folder
            shutil.copytree(filepath, studirname)
            os.chdir(studirname)

            # set up git repo
            self._create_repo(studata)

            # set up repo on bitbucket
            self._set_repo_bitbucket(studata)

            # grant access
            self._grant_access(studata, "write")

            # go back to the upper directory
            os.chdir(self.pwd)

    def pass_deadline(self, dirpath):
        """
        Switch write access to read access after passing deadline.

        Input
        =====
        dirpath: string
            Prefix of the student repository. For example, if "dirpath" is
            "e6040_hw4", the student repository will be "e6040_hw4_uni0000."

        """
        assert(os.path.exists(dirpath))

        # navigate to the directory where student repositories locate
        os.chdir(self.pwd)

        for _, studata in self.studentDataFrame.iterrows():
            studirname = dirpath + "_" + studata["UNI"]

            # TODO: need to check if the repo exists on BitBucket
            if not os.path.exists(studirname):
                print "%s does not exist... skip" % studirname
                continue

            # navigate into student's folder
            os.chdir(studirname)

            # remove write access
            self._remove_access(studata)

            # grant access
            self._grant_access(studata,"read")

            # go back to the upper directory
            os.chdir(self.pwd)

    def download_student_repo(self, dirpath):
        """
        Pull student's commits from BitBucket.

        Input
        =====
        dirpath: string
            Prefix of the student repository. For example, if "dirpath" is
            "e6040_hw4", the student repository will be "e6040_hw4_uni0000."
        """
        assert(os.path.exists(dirpath))

        # navigate to the directory where student repositories locate
        os.chdir(self.pwd)

        for _, studata in self.studentDataFrame.iterrows():
            studirname = direpath + '_' + studata['UNI']

            # TODO: need to check if the repo exists on BitBucket
            if not os.path.exists(studirname):
                print "%s does not exist... skip" % studirname
                continue

            # navigate into student's folder
            os.chdir(studirname)
            self._checkout_branch('master')

            # grant access
            self._pull_repo()

            # go back to the upper directory
            os.chdir(self.pwd)

    def create_branch(self, dirpath, branchname, filelist, dirname=""):
        """
        Create a new branch, and add new files to the branch.

        Input
        =====
        dirpath: string
            Path to the directory that contains files listed in "filelist."

        branchname: string
            Name of the new branch.

        filelist: list of string
            List of file names. The file names are relative to "dirpath." Note
            that the hierachy of the files in "filelist" will be copied to the
            Git repository.

        dirname: string
            Prefix of the student repository. For example, if "dirpath" is
            "e6040_hw4", the student repository will be "e6040_hw4_uni0000."
            If dirname is not set, the last part of "dirpath" will be used.
        """
        assert(os.path.exists(dirpath))

        # navigate to the directory where student repositories locate
        os.chdir(self.pwd)

        seg = dirpath.split('/')
        if seg[-1]:
            seg = seg[-1]
        else:
            seg = seg[-2]
        stuDirTemplate = (dirname or seg) + '_{0}'

        # covert files in filelist from relative path to absolute path
        absfilelist = []
        for i, filename in enumerate(filelist):
            f = os.path.join(dirpath, filename)
            assert(os.path.exists(f))
            absfilelist.append(os.path.abspath(f))

        for _,studata in self.studentDataFrame.iterrows():
            studirname = stuDirTemplate.format(studata['UNI'])

            # TODO: need to check if the repo exists on BitBucket
            if not os.path.exists(studirname):
                print "%s does not exist... skip" % studirname
                continue

            # navigate into student's folder
            os.chdir(studirname)

            # create a new branch
            self._add_branch(branchname)

            # add files to the new branch
            self._update_files(filelist,absfilelist)

            # commit and push the new branch
            self._commit_and_push_branch(branchname)

            # go back to the upper directory
            os.chdir(self.pwd)

    def update_branch(self, dirpath, branchname, filelist, msg, dirname=""):
        """
        Update or add files to an existing branch, and then commit and push.

        Input
        =====
        dirpath: string
            Path to the directory that contains files listed in "filelist."

        branchname: string
            Name of the new branch.

        filelist: list of string
            List of file names. The file names are relative to "dirpath." Note
            that the hierachy of the files in "filelist" will be copied to the
            Git repository.

        msg: string
            Commit message.

        dirname: string
            Prefix of the student repository. For example, if "dirpath" is
            "e6040_hw4", the student repository will be "e6040_hw4_uni0000."
            If dirname is not set, the last part of "dirpath" will be used.
        """
        assert(os.path.exists(dirpath))

        # navigate to the directory where student repositories locate
        os.chdir(self.pwd)

        seg = dirpath.split('/')
        if seg[-1]:
            seg = seg[-1]
        else:
            seg = seg[-2]
        stuDirTemplate = (dirname or seg) + '_{0}'

        # covert files in filelist from relative path to absolute path
        absfilelist = []
        for i, filename in enumerate(filelist):
            f = os.path.join(dirpath, filename)
            assert(os.path.exists(f))
            absfilelist.append(os.path.abspath(f))

        for _,studata in self.studentDataFrame.iterrows():
            studirname = stuDirTemplate.format(studata['UNI'])

            # TODO: need to check if the repo exists on BitBucket
            if not os.path.exists(studirname):
                print "%s does not exist... skip" % studirname
                continue

            # navigate into student's folder
            os.chdir(studirname)

            # checkout branch
            self._checkout_branch(branchname)

            # add files to the new branch
            self._update_files(filelist,absfilelist)

            # commit and push the new branch
            self._commit_and_push_branch(branchname, msg)

            # go back to the upper directory
            os.chdir(self.pwd)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--ta_name", type=str, default="TA",
        help="Name of the TA.")
    parser.add_argument("--ta_email", type=str, default="ta@columbia.edu",
        help="Email address of the TA.")
    parser.add_argument("--ta_account", type=str, default="ta",
        help="BitBucket account of the TA.")
    parser.add_argument("--filename", type=str,
        help="filename of the student information.")

    args = parser.parse_args()

    rm = RepoManager(args.filename, args.ta_account, args.ta_email,
        args.ta_name)

    # rm.create_student_repo('e6040_hw4')
    # rm.pass_deadline('e6040_hw4')
    # rm.download_student_repo('e6040_hw4')
    # rm.create_branch('e6040_hw3','fix',['src/hw3a.py'])
    # rm.update_branch('e6040_hw4','master',['src/hw4b.py'],'update hw4b.py)
