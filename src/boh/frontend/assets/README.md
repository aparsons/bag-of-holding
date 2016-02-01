### Compilation of frontend assets
This guide outlines how to obtain and compile the frontend assets needed for Bag of Holding.

**Requirements:**
- [Node.js](https://nodejs.org/) (Version 4.2.3 or newer)

_All of the following commands should be run from within the **assets** directory_

#### Install Node.js dependencies
The following command will install the required node modules.
```
npm install
```

#### Install Bower dependencies
The following command will install the required bower dependencies.
```
npm run bower-install
```

#### Build assets
The following command will run the gulp build and generate all of the files in the **static** directory.
```
npm run gulp
```
