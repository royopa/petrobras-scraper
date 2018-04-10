if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
  echo -e "Starting to update bases\n"

  #copy data we're interested in to other place
  cp -R bases $HOME/bases

  #go to home and setup git
  cd $HOME
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis"

  #using token clone gh-pages branch
  git clone --quiet --branch=master https://${GH_TOKEN}@github.com/royopa/petrobras-scraper.git  master > /dev/null

  #go into directory and copy data we're interested in to that directory
  cd master
  cp -Rf $HOME/bases/* .

  #add, commit and push files
  git add -f .
  git commit -m "Travis build $TRAVIS_BUILD_NUMBER pushed to master"
  git push -fq origin master > /dev/null

  echo -e "Done magic with bases\n"
fi