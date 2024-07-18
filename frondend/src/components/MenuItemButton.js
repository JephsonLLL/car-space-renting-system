import React from 'react';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';

const MenuItemButton = (props) => {
    return (
        <Menu variant='text'
            color={props.color ? props.color : 'primary'}
            onClick={props.onClick}
            sx={props.sx}
        >
            {props.children}
        </Menu>
    );
};

export default MenuItemButton