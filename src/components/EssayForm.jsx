import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { makeStyles } from '@material-ui/core/styles';
import { 
	Button,
	Container, 
	Box, 
	Typography, 
	Input,
	Modal
} from '@material-ui/core';
import { Link, DirectLink, Element, Events, animateScroll as scroll, scrollSpy, scroller } from 'react-scroll';
import RadarChart from './RadarChart';
import { useParams } from 'react-router';
  
function getModalStyle() {
	const top = 50
	const left = 50

	return {
		top: `${top}%`,
		left: `${left}%`,
		transform: `translate(-${top}%, -${left}%)`,
	};
}
  
const useStyles = makeStyles((theme) => ({
	paper: {
		position: 'absolute',
		overflow:'scroll',
		width: '80%',
		height: '80%',
		backgroundColor: theme.palette.background.paper,
		display:'block',
		padding: 12
	},
	content: {
		padding: 10
	}
}));

export default function EssayForm() {
	const classes = useStyles();
	const { id } =  useParams();
	const [modalStyle] = useState(getModalStyle);
	const [promptID, setPromptID] = useState();
	const [prompt, setPrompt] = useState();
	const [data, setData] = useState(null);
	const [essayText, setEssayText] = useState('');
	const [scoreHidden, setScoreHidden] = useState(true);
	const [open, setOpen] = useState(false);
	
	useEffect(() => {
		getPromptText(id);
    }, [])

	const getScore = () => {
		const payload = {
			essayText
		}
		axios.post(
			`http://localhost:7082/api/score`, payload)
			.then(res => {
				setData(res.data);
				setScoreHidden(false);
				scrollTo();
			})
			.catch(error => {
				console.log(error)
			})
	}

	const scrollTo = () => {
		scroller.scrollTo('radar-graph', {
			duration: 200,
			delay: 0,
			smooth: 'easeInOutQuart'
		})
	}

	const getPromptText = (id) => {
		setPromptID(id);
		const payload = {'promptid': id}
		axios.post(
			`http://localhost:7082/api/prompt`, payload)
			.then(res => {
				setPrompt(res.data);
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

	const handleOpen = () => {
		setOpen(true);
	};
	
	const handleClose = () => {
		setOpen(false);
	};

	const body = (
		<div style={modalStyle} className={classes.paper}>
			{
				prompt &&
				prompt.map((paragraph, i) => 
					<Typography key={i} className={classes.content} variant="body2" id="simple-modal-description">
						{paragraph}
					</Typography>
				)
			}
		</div>
	);

	return (
		<div>
			<Container maxWidth="sm">
				<Box my={4}>
					<Typography variant="body1" gutterBottom>
						Essay prompt {promptID}
					</Typography>{' '}
					<Button variant="contained" color="primary" onClick={handleOpen} style={{marginBottom: 20}}>View Prompt</Button>
					<Modal
						open={open}
						onClose={handleClose}
						aria-labelledby="simple-modal-title"
						aria-describedby="simple-modal-description"
					>
						{body}
					</Modal>
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
						<div id='radar-graph'>
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