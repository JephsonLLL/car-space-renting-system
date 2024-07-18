import React from 'react';
import TextField from '@mui/material/TextField';
import PropTypes from 'prop-types';

const BasicTextFields = (props) => {
    return (
      <TextField
        label={props.children}
        variant="outlined"
        type={props.type}
        onChange={props.onChange}
        InputLabelProps={{ shrink: props.InputLabelProps }}
        size={props.size}
        sx={props.sx}
        defaultValue={props.defaultValue}
        name={props.name}
      />
    );
};

BasicTextFields.propTypes = {
    onChange: PropTypes.func,
    children: PropTypes.string,
    type: PropTypes.string,
    size: PropTypes.string,
    name: PropTypes.string,
    defaultValue: PropTypes.string,
    InputLabelProps: PropTypes.bool,
    sx: PropTypes.object,
};

export default BasicTextFields;
