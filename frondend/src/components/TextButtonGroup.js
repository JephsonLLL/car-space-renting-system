import React from 'react';
import ButtonGroup from '@mui/material/ButtonGroup';

const VariantButtonGroup = (props) => {
    return (
        <ButtonGroup variant='text'
            color={props.color ? props.color : 'primary'}
            onClick={props.onClick}
            sx={props.sx}
        >
            {props.children}
        </ButtonGroup>
        );
};

export default VariantButtonGroup
