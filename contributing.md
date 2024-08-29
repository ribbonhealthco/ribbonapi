# Contribution guide

### Some guidelines, before you get started

The project prioritises Stability and Reliability.

The code you’re writing is going to power critical programs and activities for organisations that make use of the app. 

It should be written with the understanding that your code still needs to be **valid and functional** in 3 years.

It will be used in **diverse environments by a diverse set of people**. For example, it will be used offline 60% of the time, by people who are not high-tech users. This means, your code should not break because of an “unexpected input”.

It’s not possible to prevent failure 100% but we’ll do our best to reduce it. So, some guidelines we will follow.

1. Write documentation first
    1. Documentation lives here on Notion
    2. All new features (endpoints) or changes to features (endpoints) must first be documented
    3. Use in-line documentation for all critical and reusable code (functions, classes, config)
    
> Write documentation like you are handing over the codebase to a novice that will be responsible for testing, code refactoring, and deployment.
    
2. Write tests next
    1. Write Postman tests for failing and successful conditions (Functional tests)
    2. Unit testing (to be introduced later)
3. Write code
    1. Follow established standards. If unsure, follow [PEP8](https://peps.python.org/pep-0008/)
    2. Test your code from Postman
    3. Pull the `staging` branch, `git rebase` on your machine, and **test again**
    4. Now you can push
    5. All PRs should include
        1. change summary (assume it is going to be read by a non-technical end-user)
        2. link to doc
        3. link to postman test
4. Managed deployment
    1. Automated testing and deployment (to be introduced later)
    2. Release to production is a careful affair
    

## Contributing code

### 1. Initial setup

1. [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) the repo [ribbonhealthco/ribbonapi](https://github.com/ribbonhealthco/ribbonapi) into your GitHub account
2. [Clone](https://docs.github.com/en/get-started/quickstart/contributing-to-projects#cloning-a-fork) the repo to your local machine
3. You are ready to start contributing

### 2. Contributing — Your first task

Since you cloned the forked repo to your machine, you should be in the `staging` branch. 

Your first task is to update the `README` file with your name.

1. Checkout the `staging` branch into a new branch called `new-contributor-<firstname>` (i.e `new-contributor-deji`)
    
    Use the command `git checkout -b new-contributor-deji`
    
2. Update the Contributors section of the README file with your name, i.e
    
    ```markdown
    ...
    ### Contributors
    | Name   | GitHub Handle  |
    |--------|----------------|
    | Deji   | [@thedejijoseph](https://github.com/thedejijoseph) |
    | Victor | [@vbello-tech](https://github.com/vbello-tech)   |
    | Opeyemi| [@opeyemiloc](https://github.com/opeyemiloc)    |
    ...
    ```
    
3. Stage, Commit, and Push the branch to your GitHub repo
    1. `git stage README.md`
    2. `git commit -m "adding a new contributor"`
    3. `git push origin new-contributor-deji`
4. Open the repo on your browser and create a new Pull Request. Assign the PR to @thedejijoseph
5. The PR will be reviewed and merged if it does not create a conflict

### 3. Running the server

To run the server,

1. You must have installed [`pipenv`](https://pipenv.pypa.io/en/latest/)
    1. Run `pipenv shell` to activate the virtual environment
    2. Run `pipenv install` to install requirements
        1. Run `pipenv install —dev` to install optional packages, includes ipython for improved interactive shell
2. We use [Infisical](https://infisical.com/) to manage secrets
    1. Send your email address to Deji, he’ll send an invite to the Organisation and Project
    2. To get your access token,
        1. Navigate to the `ribbonapi` project
        2. Go to Access Control
        3. Under the Machine Identities tab…
        4. Create a new machine, titled “your-name’s Machine”
        5. Create a new Client Secret
3. Put these variables into your dev environment
    1. Create a .env file in your root dir (same dir as manage.py)
    2. `INFISICAL_ENV=”dev”`
    3. `INFISICAL_PROJECT_ID`
    4. `INFISICAL_CLIENT_ID`
    5. `INFISICAL_CLIENT_SECRET`
4. Create your Postgres database
    1. Put your postgres credentials in your .env file
5. Your server should run fine
    1. Running `python manage.py runserver` should work just fine
    2. Running `gunicorn mediq.wsgi`  should also work just fine
    3. If you have Heroku installed, you could also run `heroku local`

### 4. Contributing - Subsequent tasks

Important note: When taking up a **new** task, **always, always** start (checkout) from the `staging` branch. Even if you have existing tasks and their branches.

1. Sync your forked `staging` branch with the parent `staging` branch. 
    - There are two ways to go about this:
        1. Remote repo first — recommended option
            
            This means that you update your remote repo (`origin`) before updating your local machine. This is done via the browser.
            
            1. Open up the repo on your browser and Sync the fork
                    
            2. Pull your branch into your local machine
                
                `git checkout staging`
                
                `git pull origin staging`
                
        2. Local machine first
            
            This means that you update your local machine first, then push to remote repo. If you get any error using this method, use the first method above.
            
            1. Pull from `upstream`
                
                `git checkout staging`
                
                `git pull upstream staging`
                
            2. Then push to remote
                
                `git push origin staging`
                
2. Check out from the up-to-date `staging` branch to begin a new task
    
    `git checkout -b new-task`
    
3. Before pushing a completed task, [API tests must be run with Postman](https://www.notion.so/Contribution-guide-Backend-Development-df543cc860194f98986c777cd0c42fcd?pvs=21).
    
    This is to make sure existing API endpoints remain functional, and new endpoints function appropriately while following existing standards.
    
4. Stage, Commit, and Push your changes to your GitHub/remote repo
5. Create a Pull Request for your changes. Assign the PR to @thedejijoseph
6. Once reviewed and merged, your changes will be live on the [staging server](https://www.notion.so/328f8400edbd4331a5d0e0dbe26c4d81?pvs=21)
    
    To reaffirm the completion of your task and confirm that you have not introduced breaking changes, run a Postman test on the entire API Collection.
    

## Testing with Postman

1. Share your email with Deji. You’ll be invited to the Postman Workspace
2. Create folders, requests, and tests
3. Document your work as much as possible
