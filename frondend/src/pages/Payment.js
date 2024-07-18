import React from 'react';
import { useNavigate } from 'react-router-dom';
import IconLabelButtons from '../components/IconLabelButton';
import BasicTextFields from '../components/BasicTextField';

const Payment = (props) => {
  const [firstname, setFirstname] = React.useState('');
  const [lastname, setLastname] = React.useState('');
  const [cardnumber, setCardnumber] = React.useState('');
  const [expirydate, setExpirydate] = React.useState('');
  const [cvv, setCvv] = React.useState('');
  const email = localStorage.getItem('email'); // get email from local storage or get from server
  const pay = async () => {
    const body = {
        firstname,
        lastname,
        cardnumber,
        expirydate,
        cvv,
    };
    //print in console
    console.log(body);
    //POST request to Payment
  }
  const navigate = useNavigate()
  return (
    <>
      <div style={{
        display: 'flex',
        flexDirection: 'row',
        marginTop: '15vh',
      }}>
        {/* payment detail */}
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            height: '70vh',
            width: '40%',
            marginRight: '1vw',
            marginLeft: '10vw',
            borderRadius: '10px',
            border: '1px solid black',
        }}>
            <h2>Payment Detail</h2>
            <label>Name</label>
            <br/>
            <label>Car space</label>
            <br/>
            <label>Time</label>
            <br/>
            <label>Price</label>
            <br/>
            <label>Address</label>
        </div>
        {/* payment method */}
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            height: '70vh',
            width: '40%',
            borderRadius: '10px',
            border: '1px solid black',
        }}>
            <h2>Payment Method</h2>
            <BasicTextFields name="cardnumber" type='text' class="loginfield" onChange={(event) => setCardnumber(event.target.value)} value={cardnumber}>Card Number</BasicTextFields>
            <br/>
            <BasicTextFields name="expirydate" type='text' class="loginfield" onChange={(event) => setExpirydate(event.target.value)} value={expirydate}>Expiry Date</BasicTextFields>
            <br/>
            <BasicTextFields name="cvv" type='text' class="loginfield" onChange={(event) => setCvv(event.target.value)} value={cvv}>CVV</BasicTextFields>
            <br/>
            <IconLabelButtons name='payButton' color={'success'} onClick={pay}>Pay</IconLabelButtons>
        </div>
      </div>
    </>
  );
}


export default Payment;
