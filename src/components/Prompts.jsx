import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import { Button } from '@material-ui/core';
import { Link } from 'react-router-dom';

const useStyles = makeStyles((theme) => ({
	root: {
		width: '100%',
		paddingBottom: 50
  	},
	heading: {
		fontSize: theme.typography.pxToRem(15),
		fontWeight: theme.typography.fontWeightRegular,
	},
	promptTitleDiv: {
		padding: 10,
		backgroundColor: 'rgba(0,0,0,.2)',
		cursor: 'pointer',
		borderBottom: '1px solid white'
	},
	promptDiv: {
		margin: 0
	},
	promptParagraph: {
		margin: 10
	},
	buttonDiv: {
		textAlign: 'center',
		marginBottom: 10
	},
	link: {
		textDecoration: 'none'
	}
}));


function AccordionList(props) {
	const [activePanel, setActivePanel] = useState(0); 
	const classes = useStyles();
	const prompts = props.prompts;

	const onHandleActivePanel = (index) => {
		setActivePanel(index);
	}

	const listItems = Object.keys(prompts).map((prompt, i) =>
		<div key={prompt} className={classes.promptDiv}>
			<div className={classes.promptTitleDiv} onClick={() => onHandleActivePanel(i)}>
				<Typography variant='h6'>Prompt {prompt}</Typography>
			</div>
			{
				activePanel === i &&
				<div>
					{
						prompts[prompt].map((paragraph, j) => 
							<Typography variant='body2' key={j} className={classes.promptParagraph}>{paragraph}</Typography>
						)
					}
					<div className={classes.buttonDiv}>
						<Link to={`/essay-write/${prompt}`} className={classes.link}>
							<Button variant="contained" color="primary">Write Essay</Button>
						</Link>
					</div>
				</div>
			}
		</div>
		
	)
	return (
	  	<div>{listItems}</div>
	);
}


const Prompts = (props) => {
	const [prompts, setPrompts] = useState();

	useEffect(() => {
        getPrompts();
    }, [])

    const getPrompts = () => {
        axios.get('http://localhost:7082/api/prompts')
            .then(res => {
                setPrompts(res.data);
            })
            .catch(error => {
                console.log(error)
            })
    }
	
	const classes = useStyles();
	return (
		<div className={classes.root}>
			{
				prompts &&
				<AccordionList prompts={prompts} />
			}
		</div>
	);
}

export default Prompts;
