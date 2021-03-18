import React, { useState, useRef } from 'react';
import axios from 'axios';
import { 
	AppBar,
	Button,
	Toolbar,
	Container, 
	Box, 
	Typography, 
	Input
} from '@material-ui/core';
import RadarChart from './RadarChart';

export default function Home() {
	const myRef = useRef();
	const [data, setData] = useState(null);
	const [essayText, setEssayText] = useState('');
	const [scoreHidden, setScoreHidden] = useState(true);

	const getScore = () => {
	const payload = {
		essayText
	}
	axios.post(
		`http://localhost:7082/api/score`, payload)
		.then(res => {
			setData(res.data);
			setScoreHidden(false);
			myRef.current.scrollIntoView({ behavior: 'smooth' })
		})
		.catch(error => {
			console.log(error)
		})
	}

	const handleEssayTextUpdate = (e) => {
		e.preventDefault();
		setScoreHidden(true);
		setEssayText(e.target.value);
	}

	return (
		<div>
			<AppBar position="static">
			<Toolbar>
				<Typography variant="h6">
				Cross-prompt Automated Essay Trait Scorer
				</Typography>
			</Toolbar>
			</AppBar>
			<Container maxWidth="sm">
				<Box my={4}>
					<Typography variant="body1" gutterBottom>
						Essay prompt
					</Typography>
					<Input 
						id="essay-input"
						label="Essay Input"
						placeholder="Enter your essay text here."
						onChange={handleEssayTextUpdate}
						rows={10}
						rowsMax={30}
						fullWidth
						multiline
					/>
					<Button 
						variant="contained" 
						color="primary"
						style={{marginTop: 20, marginBottom: 20}}
						onClick={getScore}
					>
						Submit
					</Button>
					{
						!scoreHidden &&
						<div ref={myRef}>
							<RadarChart
								data={data}
							/>
						</div>
					}
				</Box>
			</Container>
		</div>
	)
}