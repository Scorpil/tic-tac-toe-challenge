import React, { Component } from 'react';
import Cell from './Cell.js';

class Game extends Component {
  constructor (props) {
    super(props);
    this.playerId = this.props.playerId;
    this.request = this.props.request;
    this.state = {
      game: this.props.game,
      moveRewind: this.props.moveRewind
    };

    this.refreshTimeoutMs = 1000;

    this.isRewindMode = () => Number.isInteger(this.state.moveRewind);
    this.isMatchmaking = () => this.state.game.state === 'matchmaking';
    this.isFinished = () => this.state.game.state === 'finished';

    this.isFirstMove = () => this.moves().length === 0;
    this.isLastMove = () => this.moves().length === this.state.game.moves.length;

    this.playerName = () => this.state.game.players[this.playerId];
    this.opponentName = () => this.state.game.players[this.playerId ^ 1];

    this.nextPlayerId = () => this.moves().length % 2;
    this.nextPlayerName = () => this.state.game.players[this.nextPlayerId()];

    this.canMove = () => this.nextPlayerId() === this.playerId;
    this.isNewestMove = (i) => [...this.moves()].pop() === i;
  }

  refresh () {
    this.request('get', `/api/games/${this.state.game.id}`)
      .then(({ data }) => {
        this.setState({ game: data });
        if (this.isFinished()) {
          this.stopRefresh();
          this.startRewindMode();
        }
      });
  }

  stopRefresh () {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
  }

  componentDidMount () {
    this.refresh();
    if (!this.isFinished()) {
      this.refreshInterval = setInterval(() => this.refresh(), this.refreshTimeoutMs);
    }
  }

  componentWillUnmount () {
    this.stopRefresh();
  }

  startRewindMode () {
    if (this.isRewindMode()) { return; }
    this.setState({ moveRewind: this.state.game.moves.length });
  }

  moves () {
    if (!Number.isInteger(this.state.moveRewind)) {
      return this.state.game.moves;
    }
    return this.state.game.moves.slice(0, this.state.moveRewind);
  }

  finalMessage () {
    if (this.state.game.winner === null) {
      return "It's a draw!";
    }
    return `Winner: ${this.state.game.winner}`;
  }

  turnInfo () {
    switch (true) {
      case this.isMatchmaking(): return 'Waiting for second player to join';
      case this.isFinished(): return this.finalMessage();
      case this.canMove(): return 'Your turn';
      default: return `Waiting for ${this.opponentName()} to make a move`;
    }
  }

  makeMove (i) {
    if (this.state.game.state !== 'in_progress' ||
        !this.canMove() ||
        this.moves().includes(i)) return;
    const newGame = { ...this.state.game, moves: [...this.state.game.moves, i] };
    this.setState({ game: newGame });
    this.request('post', `/api/games/${this.state.game.id}`, newGame)
      .then(response => this.setState({ game: response.data }));
  }

  isMarked (i) {
    const mark = this.moves().indexOf(i);
    if (mark === -1) {
      return null;
    }
    return mark % 2;
  }

  menu () {
    const menu = [];
    if (this.state.game.state === 'finished') {
      let menuButtonClass = 'menu button';

      let prevClasses = menuButtonClass;
      let prevClick = () => this.prevMove();
      if (this.isFirstMove()) {
        prevClasses += ' disabled';
        prevClick = null;
      }
      menu.push(<div className={prevClasses} key='prev'
        onClick={prevClick}>
                Previous Move</div>);

      let nextClasses = menuButtonClass;
      let nextClick = () => this.nextMove();
      if (this.isLastMove()) {
        nextClasses += ' disabled';
        nextClick = null;
      }
      menu.push(<div className={nextClasses} key='next'
        onClick={nextClick}>
                Next Move</div>);
    }
    menu.push(<div className='menu button' key='exit'
      onClick={() => this.props.exitGame()}>
              Exit Game</div>);
    return menu;
  }

  prevMove () {
    this.setState({ moveRewind: (this.state.moveRewind - 1) });
  }

  nextMove () {
    this.setState({ moveRewind: (this.state.moveRewind + 1) });
  }

  render () {
    return (
      <div className='board'>
        <div>{ this.turnInfo() }</div>
        <table className='boardTable'>
          <tbody>
            <tr>
              <td><Cell makeMove={this.makeMove.bind(this)}
                isMarked={this.isMarked(0)}
                isNewestMove={this.isNewestMove(0)}
                id={0} key={0} /></td>
              <td><Cell makeMove={this.makeMove.bind(this)}
                isMarked={this.isMarked(1)}
                isNewestMove={this.isNewestMove(1)}
                id={1} key={1} /></td>
              <td><Cell makeMove={this.makeMove.bind(this)}
                isMarked={this.isMarked(2)}
                isNewestMove={this.isNewestMove(2)}
                id={2} key={2} /></td>
            </tr>
            <tr>
              <td><Cell makeMove={this.makeMove.bind(this)}
                isMarked={this.isMarked(3)}
                isNewestMove={this.isNewestMove(3)}
                id={3} key={3} /></td>
              <td><Cell makeMove={this.makeMove.bind(this)}
                isMarked={this.isMarked(4)}
                isNewestMove={this.isNewestMove(4)}
                id={4} key={4} /></td>
              <td><Cell makeMove={this.makeMove.bind(this)}
                isMarked={this.isMarked(5)}
                isNewestMove={this.isNewestMove(5)}
                id={5} key={5} /></td>
            </tr>
            <tr>
              <td><Cell makeMove={this.makeMove.bind(this)}
                isMarked={this.isMarked(6)}
                isNewestMove={this.isNewestMove(6)}
                id={6} key={6} /></td>
              <td><Cell makeMove={this.makeMove.bind(this)}
                isMarked={this.isMarked(7)}
                isNewestMove={this.isNewestMove(7)}
                id={7} key={7} /></td>
              <td><Cell makeMove={this.makeMove.bind(this)}
                isMarked={this.isMarked(8)}
                isNewestMove={this.isNewestMove(8)}
                id={8} key={8} /></td>
            </tr>
          </tbody>
        </table>
        <div className='noselect'>
          { this.menu() }
        </div>
      </div>
    );
  }
}

export default Game;
