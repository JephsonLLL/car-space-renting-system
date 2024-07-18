import React from 'react';
import Button from '@mui/material/Button';

const BasicButton = (props) => {
    return (
        <Button variant='text'
            color={props.color ? props.color : 'primary'}
            onClick={props.onClick}
            sx={props.sx}
        >
            {props.children}
        </Button>
    );
};

export default BasicButton