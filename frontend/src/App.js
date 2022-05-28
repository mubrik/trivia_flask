import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import './stylesheets/App.css';
import FormView from './components/FormView';
import QuestionView from './components/QuestionView';
import Header from './components/Header';
import QuizView from './components/QuizView';
import Category from './components/Category';
import Score from './components/Score';

class App extends Component {
  render() {
    return (
      <div className='App'>
        <Header path />
        <Router>
          <Switch>
            <Route path='/' exact component={QuestionView} />
            <Route path='/addQuestion' component={FormView} />
            <Route path='/addCategory' component={Category} />
            <Route path='/play' component={QuizView} />
            <Route path='/scores' component={Score} />
            <Route component={QuestionView} />
          </Switch>
        </Router>
      </div>
    );
  }
}

export default App;
