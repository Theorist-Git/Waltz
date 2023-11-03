"""
Waltz: An open source, cloud-based password manager.
Copyright (C) 2023 <Mayank Vats>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from __init__ import create_app
import logging

app = create_app()

# Logging levels: INFO, WARNINGS, ERROR and CRITICAL
logging.basicConfig(filename='WebRecord.log', level=logging.WARNING,
                    format='%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    print("Running at http://127.0.0.1:5000/")

    def run_dev_server():
        """
        FOR DEVELOPMENT PURPOSES ONLY.
        The server runs with re-loader and debug enabled by default.
        """
        print('\033[1m', 'DEVELOPMENT SERVER', '\033[0m')
        app.run(debug=True, use_reloader=True, port=5000)

    run_dev_server()
