# Waltz: _An open source, cloud-based password manager._

## Installation

1. **Clone the Repository**:

   ```bash
   $ https://github.com/Theorist-Git/Waltz.git
   ```
2. Install the required python packages
    ```bash
   $ python3 -m venv /home/theorist/Envs/waltz    // Create a virtual env
   $ source /home/theorist/Envs/waltz/bin/activate // [Recommended]
   $ pip install requirements.txt
   ```
   
3. Make sure that you have a MySQL server installed and configured.

4. Create a `.env` file. It must have the following fields:
   ```text
    WTF_CSRF_SECRET_KEY=1234        ; Key used to generate CSRF tokens
    SECRET_KEY=1234                 ; Key used for securely signing the session cookie
    HOST=localhost                  
    USER=root
    DB=test
    THEORIST_LOCALHOST_PASS=abcd
    SENDER=email                    ; Email ID used by PyCourier to send emails.
    PASSWORD=password               ; App password for the Email ID. Google deprecated actual passwords some time ago.
    ```
   [What is the flask secret key and how do I generate it?](https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY)
5. Running the webserver: (Currently only development server is configured.)

    ```bash
   $ cd waltz
   $ python main.py
    ```    
   
## Features:

1. Creating an account that can be secured by either email or TOTP type two-factor authentication.
2. Zero knowledge architecture: The server never ever sees your passwords in plain text.
   1. Using [WebCrypto API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API) and [IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API),
   your passwords are encrypted and decrypted on the client side.
   2. The back end doesn't have any knowledge of your master password or the encryption key derived from it. So, 
   in the event of a data breach, your passwords are safe.

## Contributing
Pull requests are welcome. For major changes, please open an issue first.

## Author(s)

Contributor names and contact info
* Mayank vats : [Theorist-git](https://github.com/Theorist-Git)
  * Email: dev-theorist.e5xna@simplelogin.com

## License

This project is licensed under the [GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/#) License