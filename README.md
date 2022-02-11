# Crypto-Files

## Description:
This is the AWS Lambda deployment package + the file that contains the sql functions that interact with the sqlite database.

### Update.py:
This file contains the main function (lambda_handler) that's run in Lambda.
It checks which coins we want to have notifications for and checks if they're near their target price, then sends me an email if those conditions are satisfied.

### Database.py:
This file contains the functions that interact with the sqlite database.
