import React from 'react';
import { useNavigate } from 'react-router-dom';
import IconLabelButtons from '../components/IconLabelButton';
import BasicTextFields from '../components/BasicTextField';
import PropTypes from 'prop-types';

const Home = (props) => {
  const [search, setSearch] = React.useState('');
  //const navigate = useNavigate();
  const searchBtn = async () => {
    const body = {
      search
    };
    //print in console
    console.log(body);
    //get request
    localStorage.setItem('search', search);
    //jump to next search page
    //navigate('/search')
  }
  return (
    <>
      <h1 style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'column',
        height: '20vh',
      }}>Car space system</h1>
      <br/>
      {/* search bar */}
      <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          }}>
        {/* style of search box and button change later */}
        <BasicTextFields name='search'>Search here!</BasicTextFields>
        <IconLabelButtons name='searchButton' onClick={searchBtn}>Go</IconLabelButtons>
      </div>
      {/* container for three windows */}
      <div class="container" style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'row',
        marginTop: '5vh',
      }}>

        {/* window 1  starred car space*/}
        <div name="star" style={{
          backgroundColor: 'green',
          width: '30vw',
          height: '50vh',
          marginRight: '1vw',
        }}>

        </div>
        {/* window 2  recommended car space*/}
        <div name="recommend" style={{
          backgroundColor: 'green',
          width: '30vw',
          height: '50vh',
          marginRight: '1vw',
        }}>

        </div>
        {/* window 3 quick park*/}
        <div name="park" style={{
          backgroundColor: 'green',
          width: '30vw',
          height: '50vh',
        }}>

        </div>

      </div>
    </>
  );
}

export default Home;