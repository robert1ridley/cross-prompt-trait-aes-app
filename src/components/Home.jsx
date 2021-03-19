import React, { useState, useRef } from 'react';
import { 
	Container, 
	Box, 
	Typography
} from '@material-ui/core';
import Prompts from './Prompts';

export default function Home() {
	return (
		<div>
			<Container maxWidth="sm">
				<Box my={4}>
					<Typography variant="h6" style={{marginBottom: 30}}>
						Choose an essay prompt
					</Typography>
					<Prompts />
				</Box>
			</Container>
		</div>
	)
}