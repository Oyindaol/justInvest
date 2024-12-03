# justInvest System

## How to run the justInvest system:

1. Connect to Carleton VPN.
2. Connect to the VM.
3. Navigate to where the justInvest Folder is saved and located.
4. To run the program, type in the terminal:
   ### ./justInvest.py or python3 justInvest.py 
   
5. If you have an issue with permissions, type the command below and try step 4 again:
   ### chmod +x justInvest.py 
6. Python3 must be installed on the VM for these instructions to work.

## How to run the tests:
1. Follow the above instructions on how to run the justInvest system (steps 1-3).
2. To run the test, type in the terminal:
    #### For Problem 1 tests-> ./problem1c.py or python3 problem1c.py
    #### For Problem 2 tests-> ./problem2d.py or python3 problem2d.py
    #### For Problem 3 tests-> ./problem3c.py or python3 problem3c.py
    #### For Problem 4 tests-> ./problem4c.py or python3 problem4c.py
3. Follow the above step 5 if permission issues occur.

   
## How to use justInvest
1.. After running the program, you will see the options to (1) Register User (2) Login or (3) Exit. Users will also see a prompt to enter their choice based on the number they type (1, 2, or 3). Selecting any other option will give an error message then display the choices again

2a. If (1) is selected, the user is registering for the system:
    Users will be prompted to enter their username, password, and role (role determines the available operations).
    If the password does not meet the password specifications, a message will be displayed with the expected requirements.
    User will have to enter their role based on the available roles (Case sensitive!)
    If all the prompts entered are valid, the user will be automatically logged in.

2b. If (2) is selected, the user is logging in to the system:
    Users will be prompted to enter their username and password. If these are valid credentials, ACCESS GRANTED, otherwise ACCESS DENIED
    The username, role, and the operations available to the user will be displayed by the number corresponding to the list of operations displayed above.
    If the user types in any of the numbers of the operations available to you, ACCESS GRANTED, otherwise ACCESS DENIED.
    Type 0 to return to the main menu from step 1.

2c. If (3) is selected you will be exited from the system.
