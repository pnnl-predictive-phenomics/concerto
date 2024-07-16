To use the cookiecutter
`
cookiecutter cookiecutter-memote.zip
`
which will then proceed to make a new repo from the questions it asks. 

Users can then generate a new github repo no github, which generates a url. From within the newly created directory

```
git init 
git remote add origin https://github.com/OWNER/REPOSITORY.git # new url
# you want to add your model file to the folder within the name you selected with the cookiecutter
git add .
git commit -m 'adding memote template'
git push
```

Once made, the user will still be required to generate a gh-pages branch. 

```
git checkout gh-pages
git push
```

In theory, all changes to the model.xml will be tracked under the github pages created. 

To modify the cookie-cutter template, unzip the folder, make changes, then rezip before submitting to repo. 