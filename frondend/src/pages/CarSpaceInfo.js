import React from 'react';
import { useNavigate } from 'react-router-dom';
import IconLabelButtons from '../components/IconLabelButton';
import BasicTextFields from '../components/BasicTextField';
import PropTypes from 'prop-types';

const CarSpaceInfo = (props) => {
  const [search, setSearch] = React.useState('');
  const navigate = useNavigate();
  const [distance, setDistance] = React.useState('');
  const [price, setPrice] = React.useState('');
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
            {/* search bar */}
            <div style={{
            display: 'flex',
            alignItems: 'left',
            justifyContent: 'center',
            }}>
            {/* style of search box and button change later */}
            <BasicTextFields name='search'>Search here!</BasicTextFields>
            <IconLabelButtons name='searchButton' onClick={searchBtn}>Go</IconLabelButtons>
            </div>

            {/* filter */}
            <div style={{
            display: 'flex',
            alignItems: 'left',
            justifyContent: 'center',
            }}>
              <input type="checkbox" id="filter" name="filter" value="filter"/>filter and sort<br/>
            </div>
            
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
        <div name="map" style={{
          backgroundColor: 'Red',
          width: '70%',
          height: '70vh',
        }}>
          Google Map
        </div>
      </div>
    </>
  );
}

export default CarSpaceInfo;