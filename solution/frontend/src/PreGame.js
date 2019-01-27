import axios from 'axios';

import React, { Component } from 'react';

class PreGame extends Component {
  constructor (props) {
    super(props);
    this.request = this.props.request;

    this.state = { games: [] };
  }

  componentDidMount () {
    this.refreshGames();
    this.refreshInterval = setInterval(() => this.refreshGames(), 1000);
  }

  componentWillUnmount () {
    clearInterval(this.refreshInterval);
  }

  refreshGames () {
    axios.get('/api/games')
      .then(response => this.setState({
        games: response.data.items
      }));
  }

  renderGameList () {
    if (this.state.games.length === 0) {
      return ([<div key='no-game-msg'>No games yet :(</div>]);
    }
    return this.state.games
      .map(game => this.gameButton(game));
  }

  gameButton (game) {
    switch (game.state) {
      case 'matchmaking':
        return (<div className='join-game button'
          key={game.id}
          onClick={() => this.joinGame(game)}>
              Join game created by {game.players[0]}
        </div>);
      case 'finished':
        return (<div
          key={game.id}
          className='watch-game button'
          onClick={() => this.watchGame(game)}>
              Watch finished game between {game.players[0]} and {game.players[1]}
        </div>);
      default: return '';
    }
  }

  startGame () {
    const newGame = { players: [this.props.user.name], moves: [] };
    axios.post('/api/games', newGame,
      { headers: { authorization: `Bearer ${this.props.user.authToken}` } })
      .then(request => this.props.setGame(request.data, 0));
  }

  watchGame (game) {
    this.request('get', `/api/games/${game.id}`)
      .then(({ data }) => this.props.setGame(data, null, 0));
  }

  joinGame (game) {
    axios.post(`/api/games/${game.id}`,
      { ...game, players: [...game.players, this.props.user.name] },
      { headers: { authorization: `Bearer ${this.props.user.authToken}` } })
      .then(request => this.props.setGame(request.data, 1));
  }

  render () {
    return (
      <div className='pre-game'>
        <div className='start-game button' href='#' onClick={() => this.startGame()}>Start New Game</div>
        { this.renderGameList() }
      </div>
    );
  }
}

export default PreGame;
