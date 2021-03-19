import React from 'react';
import { Link } from 'react-router-dom';
import { 
	AppBar,
	Toolbar,
	Typography
} from '@material-ui/core';



const Header = () => {
    return (
        <AppBar position="static">
            <Toolbar>
                <Link to={'/'} style={{textDecoration: 'none', color: 'white'}}>
                    <Typography variant="h6">
                        Cross-prompt Automated Essay Trait Scorer
                    </Typography>
                </Link>
            </Toolbar>
        </AppBar>
    )
}

export default Header;