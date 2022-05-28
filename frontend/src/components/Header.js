import React, { Component } from 'react';
import '../stylesheets/Header.css';

class Header extends Component {
  navTo(uri) {
    window.location.href = window.location.origin + uri;
  }

  render() {
    return (
      <nav className='App-header'>
        <h1
          onClick={() => {
            this.navTo('');
          }}
        >
          Udacitrivia
        </h1>
        <div
          className='nav-link'
          onClick={() => {
            this.navTo('');
          }}
        >
          List
        </div>
        <div
          className='nav-link'
          onClick={() => {
            this.navTo('/addQuestion');
          }}
        >
          Add Question
        </div>
        <div
          className='nav-link'
          onClick={() => {
            this.navTo('/addCategory');
          }}
        >
          Add Category
        </div>
        <div
          className='nav-link'
          onClick={() => {
            this.navTo('/play');
          }}
        >
          Play
        </div>
        <div
          className='nav-link'
          onClick={() => {
            this.navTo('/scores');
          }}
        >
          Scores
        </div>
      </nav>
    );
  }
}

export default Header;
