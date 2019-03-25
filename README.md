# use asyncio ping IP and send command
pip3 install aioping

 echo "# pull-test">> README.md
 git init
 git add README.md
 git add *
 git commit -m "first pull some file"
 git config --global user.name "lyc10031"
 git config --global user.email "lyc10031@126.com"
 git commit --amend --reset-author
 git remote add origin https://github.com/lyc10031/pull-test.git
 git push -u origin master
 vim /etc/resolv.conf
