import React from 'react';
import { Route, Switch } from 'react-router-dom';
import App from './components/App';
import Home from './components/Home';
import EssayForm from './components/EssayForm';
import Header from './components/Header';

const routes = (
	<App>
		<Header />
		<Switch>
			<Route exact path='/' component={Home} />
			<Route path='/essay-write/:id' component={EssayForm} />
		</Switch>
	</App>
)

export { routes };