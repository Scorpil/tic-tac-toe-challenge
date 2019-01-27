### Tic-Tac-Toe challenge

This is a solution for [Anaconda: Tic-Tac-Toe Coding Challenge](https://github.com/ContinuumIO/tic-tac-toe-challenge).
Solution consists of three separate apps:
- Backend API: in Python + Tornado
- Frontend: ReactJS
- Proxy: Nginx server configure to route requests to either frontend or api, depending on url.

Docker + docker-compose is used for conterization and orchestration.

### How to run:
- To start tic-tac-toe in production mode, run `docker-compose up --build` in `./solution` folder.
- To start development mode run `docker-compose -f docker-compose-dev.yml up --build`

Once the service is started, you can play Tic-Tac-Toe on [localhost](http://localhost).

To test the api, run `docker-compose run api pytest`.
