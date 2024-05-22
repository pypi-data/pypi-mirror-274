def luxlib():


    print("""
    
cd /home: Go to the / home directory.
cd ..: Go to the directory one level up from the current directory.
cd ../..: Go to the directory two levels up from the current directory.
cd: Go to your home directory.
cd ~user1: Go to another user's home directory.
cd -: Go to the the previous directory from the current working directory.
pwd: Display the working directory.
ls: Display the full list or content of your directory.
ls -F: Display files in the directory.
ls -l: Display details of files and directories.
ls -a: Display the whole list of the current directory including the hidden files.
ls *[0-9]*: Display file and directory names that contain digits.
tree: Display the tree structure of files and directories starting from the root directory.
lstree: Display the tree structure of files and directories starting from the root directory.
mkdir dir1: Create the dir1 directory.
mkdir dir1 dir2: Create two directories concurrently.
mkdir -p /tmp/dir1/dir2: Create a directory with sub-directories.
rm -f file1: Delete the file1 file.
rmdir dir1: Delete the dir1 directory.
rm -rf dir1: Delete the dir1 directory and its content.
rm -rf dir1 dir2: Delete two directories and their content concurrently.
mv dir1 new_dir: Rename or move a directory.
cp file1 file2: Copy a file.
cp dir/*: Copy all files in a directory to the current working directory.
cp -a /tmp/dir1: Copy a directory to the current working directory.
cp -a dir1 dir2: Copy a directory.
ln -s file1 lnk1: Create a soft link to a file or directory.

    """)