git checkout beta
git pull origin beta

git checkout staging
git pull origin staging
git merge beta
git push origin staging

git checkout testing
git pull origin testing
git merge staging
git push origin testing

git checkout development
git pull origin development
git merge testing
git push origin development

git checkout testing
git pull origin testing
git merge development
git push origin testing

git checkout staging
git pull origin staging
git merge testing
git push origin staging

fab config.set:staging project.update project.restart

git checkout beta
git pull origin beta
git merge staging
git push origin beta

git checkout master
git pull origin master
git merge beta
git push origin master

git checkout development
