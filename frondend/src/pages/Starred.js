import React from 'react';
import { useNavigate } from 'react-router-dom';
import IconLabelButtons from '../components/IconLabelButton';
import BasicTextFields from '../components/BasicTextField';
import PropTypes from 'prop-types';

const Starred = (props) => {
  const navigate = useNavigate();
  const navRatePage = async () => {
    navigate('/payment')
  }
  return (
    <>
      {/* container for two windows */}
      <div class="container" style={{
        display: 'flex',
        flexDirection: 'row',
        marginTop: '15vh',
      }}>

        {/* window 1  side page*/}
        <div name="star" style={{
          backgroundColor: 'green',
          width: '30%',
          height: '70vh',
          marginRight: '1vw',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'left',
        }}>
            <h1 style={{
                alignItems: 'center',
                justifyContent: 'center',
                flexDirection: 'column',
                display: 'flex',
            }}>Starred</h1>
            {/* car space list */}
            <div style={{
            display: 'flex',
            alignItems: 'left',
            justifyContent: 'center',
            flexDirection: 'column',
            }}>
              {/* add button for searched results */}
              <IconLabelButtons>Car space 1</IconLabelButtons>
              <IconLabelButtons>Car space 2</IconLabelButtons>
              <IconLabelButtons>Car space 3</IconLabelButtons>
              <IconLabelButtons>Car space 4</IconLabelButtons>
              <IconLabelButtons>Car space 5</IconLabelButtons>
              <IconLabelButtons>Car space 6</IconLabelButtons>
            </div>
        </div>
        {/* window 2 car info*/}
        <div name="info" style={{
          backgroundColor: 'Red',
          width: '70%',
          height: '70vh',
          display: 'flex',
          flexDirection: 'column',
        }}>
            {/* upper subwindow */}
          <div style={{
            backgroundColor: 'blue',
            width: '100%',
            height: '50%',
          }}>
            <IconLabelButtons>Starred</IconLabelButtons>
          </div>
            {/* lower subwindow */}
          <div style={{
            backgroundColor: 'yellow',
            width: '100%',
            height: '50%',
          }}>
            <IconLabelButtons onClick={navRatePage}>Book</IconLabelButtons>
          </div>
        </div>
      </div>
    </>
  );
}

export default Starred;