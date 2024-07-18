import * as React from 'react';
import Button from '@mui/material/Button';
import PropTypes from 'prop-types';

const ContainedButton = (props) => {
  return (
    <Button variant='contained'
      color={props.color ? props.color : 'primary'}
      onClick={props.onClick}
      sx={props.sx}
    >
      {props.children}
    </Button>
  );
};

ContainedButton.propTypes = {
  children: PropTypes.string,
  color: PropTypes.string,
  sx: PropTypes.object,
  onClick: PropTypes.func,
};

export default ContainedButton;