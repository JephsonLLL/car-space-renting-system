import React from 'react';
import { useNavigate } from 'react-router-dom';
import IconLabelButtons from '../components/IconLabelButton';
import BasicTextFields from '../components/BasicTextField';
import PropTypes from 'prop-types';
import BasicButton from '../components/BasicButton';

import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import { makeStyles } from '@mui/material/styles';

// const useStyles = makeStyles((theme) => ({
//     root: {
//       flexGrow: 1,
//     },
//     paper: {
//       padding: theme.spacing(2),
//       textAlign: 'center',
//       color: theme.palette.text.secondary,
//     },
//   }));

const UpdateCarSpaceDetail = (props) => {
  const [search, setSearch] = React.useState('');
  const navigate = useNavigate();
  const searchBtn = async () => {
    const body = {
      search
    };
    //print in console
    console.log(body);
    //get request
    localStorage.setItem('search', search);
    //jump to next search page
    navigate('/search')
  }
  const [price, setPrice] = React.useState('');
  const [minPrice, setMinPrice] = React.useState('');
  const [maxPrice, setMaxPrice] = React.useState('');
  const [pricingMethod, setPricingMethod] = React.useState(''); 
//   const classes = useStyles();
  return (
    <>
      <h1 style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'column',
        height: '10vh',
      }}>Update Car space system</h1>
      <br/>
      {/* form for car space detail */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'column',
      }}>
        <BasicTextFields name='Price' type='number' onChange={(event) => setPrice(event.target.value)}>Price per week</BasicTextFields>
      </div>
      {/* display check box */}
      <div class='container' style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}>
        <input type='checkbox' name='recommend_choice'></input>
        <label>Use Recommended Price</label>
        <input type='checkbox' name='recommend_choice'></input>
        <label>Allow Dynamic Pricing</label>
      </div>

      {/* form */}
      {/* <div className={classes.root}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper className={classes.paper}>xs=12</Paper>
        </Grid>
        <Grid item xs={6}>
          <Paper className={classes.paper}>xs=6</Paper>
        </Grid>
        <Grid item xs={6}>
          <Paper className={classes.paper}>xs=6</Paper>
        </Grid>
        <Grid item xs={3}>
          <Paper className={classes.paper}>xs=3</Paper>
        </Grid>
        <Grid item xs={3}>
          <Paper className={classes.paper}>xs=3</Paper>
        </Grid>
        <Grid item xs={3}>
          <Paper className={classes.paper}>xs=3</Paper>
        </Grid>
        <Grid item xs={3}>
          <Paper className={classes.paper}>xs=3</Paper>
        </Grid>
      </Grid> 
    </div> */}
    </>
  );
}

export default UpdateCarSpaceDetail;