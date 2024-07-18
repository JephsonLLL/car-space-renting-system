import React from 'react';

import {
   Box,
   Button,
   Typography,
   Rating,
 } from "@mui/material";

 async function book(credentials) {
  return fetch('/api/make_booking', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': localStorage.getItem('token'),
    },
    body: JSON.stringify(credentials)
  })
  .then(response => {
    if (response.ok) {
      return response.json();
    }
    throw new Error('Something went wrong');
  })
}


 const CarspaceCard = ({address, rating, price,id,bookdate}) => {
  const bookBtn = async () => {
    await book({
      id,
      bookdate
    })
    .then(response => {
      console.log(response);
      alert('Success!')
    })
    .catch((error) => {
      console.log(error)
    });
  }

   return (
    <Box
      sx={{
          //mt: 0,
          borderRadius: '5px',
          //fontWeight: 'medium'
          boxShadow: 2,
          minwidth: 300,
          height: 200,
          minHeight:200,
          flexDirection: "column",
          mt:1
      }}
     >

      <Typography sx={{m:1, fontSize: 14 }} color="text.secondary" gutterBottom>
      ${price} per day
      </Typography>

      <Typography sx={{ml:1 }} variant="h6" component="div">
        {address}
      </Typography>

      

      <Rating  sx={{m:1 }} value={rating} readOnly precision={0.1}/>
        <br/>
        <br/>
      <Button size="small" onClick={bookBtn} sx={{m:1 }}>Book now</Button>
  
    </Box>
   );
 }
 export default CarspaceCard;