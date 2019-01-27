import React, { Component } from 'react';
import axios from 'axios';
import jwt from 'jsonwebtoken';

import PreGame from './PreGame';
import Game from './Game';
import Controls from './Controls';
import './App.css';

class App extends Component {
  constructor (props) {
    super(props);
    this.state = {
      user: {},
      game: {},
      moveRewind: null,
      playerId: null
    };
  }

  componentDidMount () {
    document.title = 'Tic-Tac-Toe';
  }

  request (method, url, data) {
    return axios[method](url, data, {
      headers: { Authorization: `Bearer ${this.state.user.authToken}` } });
  }

  isInGame () {
    return !!this.state.game.id;
  }

  isLoggedIn () {
    return !!this.state.user.authToken;
  }

  setGame (game, playerId, moveRewind) {
    this.setState({ game, playerId, moveRewind });
  }

  login (username) {
    return axios.post('/api/auth', { name: username })
      .then(response => this.setState({ user: {
        ...jwt.decode(response.data.token),
        authToken: response.data.token
      } }));
  }

  logout () {
    this.setState({ user: {}, game: {} });
  }

  component () {
    if (this.isInGame()) {
      return (<Game
        game={this.state.game}
        moveRewind={this.state.moveRewind}
        playerId={this.state.playerId}
        exitGame={() => this.setState({ game: {} })}
        request={(...args) => this.request(...args)} />);
    }
    if (this.isLoggedIn()) {
      return (<PreGame
        user={this.state.user}
        setGame={(...args) => this.setGame(...args)}
        request={(...args) => this.request(...args)} />);
      // TODO: check logout
    }
    return <Controls login={(...args) => this.login(...args)} />;
  }

  render () {
    return (
      <div className='App'>
        {this.component()}
      </div>
    );
  }
}

export default App;
