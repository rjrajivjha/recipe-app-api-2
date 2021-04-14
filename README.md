# recipe-app-api-2
Recipe API Source code


1. Create a Docker File
    - File name : Dockerfile
    - Enter the data accordingly
    - Create an empty app folder
    - Create a requirements.txt
    - Run dockerfile
        `docker build .`
      

2. Docker Compose lecture
   
   - Create a file docker-compose.yml
   - Enter version, services and app build, port, volume, command
   - Run docker-compose file with following command
   `docker-compose build`

3. `docker-compose run app sh -c " django-admin.py startproject app ." `
      
4.  Enable Travis CI for our github project.
   - Login to Travis CI with your github account
   - Create Travis CI configuration file
   - It tells travis what to do, everytime we push a change to our project
   - create `.travis.yml`
   - Enter the details as the file used in this project.
   - Create .flake8 file to add linting support
   - Fill the details such as which file to lint and which to leave.

5. Run Test

   - ```docker-compose run app sh -c "python manage.py test" ```

6. Create core app
   - This will hold all the basic logic for core app and act as layer between all sub-apps
   - `docker-compose run app sh -c "python manage.py startapp core" `
   - Add 'core' to Installed_apps in settings.py file of app project.
   
7. Add tests folder
   - Add tests folder
   - Create test_models.py
   

8. Create User Model
   - write a usermanager class with create_user functionality to override baseUserManager
   - Define a user Model class to override abstractBaseUser
   - Write models field in user class
   - Run migrations
      `docker-compose run app sh -c "python manage.py makemigrations <name_of_app>"`