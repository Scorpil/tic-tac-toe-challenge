import React, { Component } from 'react';

class Cell extends Component {
  char () {
    switch (this.props.isMarked) {
      case null: return '';
      case 0: return 'X';
      case 1: return 'O';
      default: throw new Error('Wrong value');
    }
  };

  className () {
    let cName = 'square button';
    if (this.props.isNewestMove) {
      cName += ' newest-cell';
    }
    return cName;
  }

  render () {
    return (
      <div className={this.className()}
        onClick={() => this.props.makeMove(this.props.id)}>
        {this.char()}
      </div>
    );
  }
}

export default Cell;
