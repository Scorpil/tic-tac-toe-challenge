import React, { Component } from 'react';

class Controls extends Component {
  constructor (props) {
    super(props);
    this.state = { inputUsername: '' };
    this.login = props.login;
  }

  render () {
    return (
      <div className='controls'>
        <input type='text' className='name-input' maxLength='15'
          value={this.state.inputUsername}
          onChange={event => this.setState({ inputUsername: event.target.value })}
          onKeyPress={event => event.key === 'Enter' ? this.login(this.state.inputUsername) : null} />
        <div className='save-button' href='#' onClick={() => this.login(this.state.inputUsername)}>Login</div>
      </div>
    );
  }
}

export default Controls;
