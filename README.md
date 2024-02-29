# The Kingfish Sustainability Project - Penguin Dash

## Deploying the Django Project
The project requires python versions `3.10` to `3.11`
To install dependencies, navigate to the `root directory` and run the command:
```
pip install -r requirements.txt
```

Then you can navigate to the directory `mysite` and deploy the server by running the command:
```
python manage.py runserver
```
## Work performed by each group member

### Loki - Database Design and Development:

Loki worked on the design of the database and its creation on the back end. His work can be seen in the Database design document.

### Daniel Hibbin - Game Design and Development:

Daniel Hibbin worked on the game design and development for the PenguinRunner game. His work was performed in the Godot Game Engine and his work can be seen in the `PeguinRunnerGodotProject` directory. This game engine supports HTML5 exports and the initial export can be seen in the `PenguinGameExport` directory. All of the files in this directory are the results of compilation and are not commented as a result. These compiled files are also placed in `The-Kingfish\mysite\static\game`.

This game engine uses GDscript as a language, which lacks any strongly enforced standards or guides. Daniel has tried his best to format and comment this code to be as readable and professional as possible. 

### Daniel Banks - Front End Design and Development:

Daniel Banks worked on the front end of the website. This included the creation of the static `.html` files and `.css` files and ensuring their compatability with the back end. 

### Back End Design and Development
Members working on this include:
- Jaspser
- Tom
- Charlie

### Tom Tooley - Sustainability Quiz:
Tom Tooley worked on implementing both the front and back end of the sustainability quiz feature of the site, a multiple-choice quiz a user can partake in to gain bonus coins after redeeming a qrcode to raise environmental awareness. The django backend for this work can be found in the 'quiz' app directory, and the front end can be found in the static html/quiz directory.

### Jasper Wise - Account, Leaderboard and Qrcode systems back end:
Jasper Wise worked on implementing the back end for the account management system of the site, the leaderboard feature, as well as the system for generating and redeeming qrcodes. These features support the fundamental functionality of the site, allowing users to make an account, gain coins to play the game via redeeming the qrcodes, and compete against other users via the leaderboard. This work can be found in the 'qrcodes', 'accounts', and 'siteadmin' app directories.

### Charlie Walford - Project documentaion and support of back end development:
Charlie Walford documented the development process, wrote up the product document, and assisted both Tom Tooley and Jasper Wise in the development of the back end in each of their parts through both contributing to the code and helping with debugging.


