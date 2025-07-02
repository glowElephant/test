# Character Customization Prototype

This repository contains a small prototype showing a Node.js backend and a React front end for the character customizer described in `test.md`.

## Backend

* Located in the `server` directory
* Uses Express and PostgreSQL
* Environment variables can be defined in a `.env` file. See `.env.example` for defaults.
* To install dependencies and start the server:

```bash
cd server
npm install
npm start
```

The server exposes a few JSON APIs such as `/characters`, `/packages` and `/packages/:id/items`.

## Frontend

* A very small React application in `frontend/index.html`
* The page now ships with local copies of React, ReactDOM and Babel (in `frontend/lib`)
  so it works even without internet access.
* Open the file directly in the browser after starting the backend.
* Click a package to see its items and try purchasing them.

## Database

SQL for the required tables is in `server/schema.sql` and is based on the design documented in `db.md`.
