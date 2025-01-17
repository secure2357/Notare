# Notare

Notare is an open source note-taking app for educational YouTube videos. It consists of a Google Chrome extension for note-taking and a companion webapp for note and video organisation, both communicating with a common Flask REST API backend with SQLite database.

![](/frontend/src/demo.png)

## Roadmap

- Replace the Flask SQLite backend with Firebase.
- Various UX improvements, including rich text.

## Running Notare

The follow instruction are for Mac and Linux computers.

If you want to run the frontend, extension and backend together, follow these instructions:

1. Clone the repository by running `git clone https://github.com/alexanderj2357/Notare`
2. Ensure you have the following software installed:
- Python 3, can be installed from https://www.python.org/downloads/
- virtualenv, can be installed using `python3 -m pip install virtualenv`
- Node.js, can be installed from https://nodejs.org/en/download/
- npm, can be installed from https://www.npmjs.com/get-npm/
- yarn, can be installed from https://yarnpkg.com/lang/en/docs/install/
3. Ensure you are in `Notare/`
4. Run `sh run.sh` to run the frontend, backend and extension
5. If the extension is installed on Google Chrome, refresh it from [_chrome://extensions_](chrome://extensions) once the extension completes building

If you want to run the frontend, backend and extension separately, follow the instructions above and then open 3 separate shells and run the following in each shell:

1. Run `sh run_backend.sh` to run the backend.
2. Run `sh run_frontend.sh` to run the frontend.
3. Run `sh run_extension.sh` to run the extension.

To run the frontend, backend and extension manually, check the README.md in their respective directories.

### Installing Extension

1.  Complete the steps to build the project above.
2.  Go to [_chrome://extensions_](chrome://extensions) in Google Chrome.
3.  With the developer mode checkbox ticked, click **Load unpacked** and select the `dist/` folder from this repo.

## Running Tests

Please run the following command: `sh run_backend_tests.sh`
