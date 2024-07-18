import React, { useState, useMemo } from "react";
import { useNavigate } from "react-router-dom";

import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { DateRangePicker } from "@mui/x-date-pickers-pro/DateRangePicker";
import { DemoItem } from "@mui/x-date-pickers/internals/demo";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";

import { GoogleMap, Marker, useLoadScript } from "@react-google-maps/api";

import SearchPlaces from "../components/search";
import CarspaceCard from "../components/carspaceCard";
import {
  Box,
  IconButton,
  RadioGroup,
  Radio,
  FormControlLabel,
  Typography,
  FormControl,
  OutlinedInput,
  InputAdornment,
  InputLabel
} from "@mui/material";

import SearchIcon from "@mui/icons-material/Search";

async function search(credentials) {
  return fetch("/api/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: localStorage.getItem("token")
    },
    body: JSON.stringify(credentials)
  }).then((response) => {
    if (response.ok) {
      return response.json();
    }
    throw new Error("Something went wrong");
  });
}

export default function FindCarSpace() {
  const [selected, setSelected] = useState("");
  const center = useMemo(() => ({ lat: -33.911, lng: 151.23 }), []);

  const [address, setAddress] = React.useState("");
  const [lat, setlat] = React.useState(0);
  const [lng, setlng] = React.useState(0);

  const [sortby, setSortby] = React.useState("default");

  const [date, setDate] = React.useState(null);
  const [distance, setDistance] = React.useState(3);

  const [carspacelist, setCarspacelist] = React.useState([]);
  const [temp, settemp] = React.useState([]);


  const searchBtn = async (e) => {
    e.preventDefault();
    settemp([]);
    await search({
      lat,
      lng,
      sortby,
      date,
      distance
    })
      .then((response) => {
        
      setCarspacelist([]);
        
        for (const key in response){
           
          response[key].book_date=date;
          temp.push(response[key]);
          console.log(temp)
        }
        setCarspacelist(temp)
           
      })
      .catch((error) => {
        console.log(error);
      });
  };

  console.log(carspacelist);
  const carspaceitems = carspacelist.map((carspace) => (
    <>
      <CarspaceCard
        address={carspace.address}
        rating={carspace.rating}
        price={carspace.price_per_day}
        id={carspace.id}
        bookdate={carspace.book_date}
      />
    </>
  ));

  const { isLoaded } = useLoadScript({
    googleMapsApiKey: "AIzaSyDpsPxJU1pU4V_LhqoOK3HUjAVsibLc8Lg",
    libraries: ["places"]
    //language:'en'
  });

  if (!isLoaded) return <div>Loading...</div>;
  return (
    <Box
      sx={{
        display: "flex",
        overflow: "hidden",
        height: 620,
        width: 1,
        mt: 7
      }}
    >
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          width: 0.33,
          height: 1,
          ml: 1
          //mr:1,
        }}
      >
        <Box
          sx={{
            //mt: 0,
            borderRadius: "5px",
            //fontWeight: 'medium'
            boxShadow: 1,
            width: 1,
            height: 310
            //display: 'flex',
          }}
        >
          <Box sx={{ display: "flex", flexDirection: "row", ml: 1 }}>
            <Box sx={{ width: 0.9 }}>
              <SearchPlaces
                setSelected={setSelected}
                setlat={setlat}
                setlng={setlng}
                setAddress={setAddress}
              />
            </Box>
            <IconButton
              onClick={searchBtn}
              color="primary"
              size="large"
              sx={{ m: 1.5, width: 5, height: 1 }}
              aria-label="search"
            >
              <SearchIcon fontSize="inherit" />
            </IconButton>
          </Box>

          <Box sx={{ display: "flex", flexDirection: "row", ml: 1 }}>
            <Typography variant="body2" sx={{ m: 1 }}>
              Sort by
            </Typography>

            <RadioGroup
              row
              defaultValue="default"
              sx={{ ml: 1 }}
              onChange={(event, value) => {
                setSortby(value);
              }}
            >
              <FormControlLabel
                value="default"
                size="small"
                control={<Radio />}
                label="default"
              />
              <FormControlLabel
                value="price"
                size="small"
                control={<Radio />}
                label="price"
              />
              <FormControlLabel
                value="distance"
                size="small"
                control={<Radio />}
                label="distance"
              />
              <FormControlLabel
                value="rating"
                size="small"
                control={<Radio />}
                label="rating"
              />
            </RadioGroup>
          </Box>
          <Box sx={{ m: 1, ml: 2, mr: 2 }}>
            <LocalizationProvider dateAdapter={AdapterDayjs}>
              <DemoItem label="Choose date range" component="DateRangePicker">
                <DateRangePicker
                  disablePast
                  onChange={(newValue) => setDate(newValue)}
                />
              </DemoItem>
            </LocalizationProvider>
          </Box>

          <Box sx={{ display: "flex", flexDirection: "row", ml: 1 }}>
            <Typography variant="body2" sx={{ m: 3, ml: 1 }}>
              Choose search range
            </Typography>

            <FormControl size="small" variant="outlined" sx={{ mt: 2 }}>
              <InputLabel>Searching range</InputLabel>
              <OutlinedInput
                type="number"
                label="Searching range"
                endAdornment={
                  <InputAdornment position="end">km</InputAdornment>
                }
                onChange={(e) => setDistance(e.target.value)}
                inputProps={{
                  step: 0.1
                }}
              />
            </FormControl>
          </Box>
        </Box>

        <Box
          sx={{
            m: 1,
            display: "flex",
            flexDirection: "column",
            height: 700,
            overflow: "hidden",
            overflowY: "scroll"
            // justifyContent="flex-end" # DO NOT USE THIS WITH 'scroll'
          }}
        >
          {carspaceitems}
        </Box>
      </Box>

      <Box
        sx={{
          ml: 1,
          width: 0.65,
          height: 1
        }}
      >
        <GoogleMap
          mapContainerStyle={{ width: "100%", height: "100%" }}
          center={center}
          zoom={6}
        >
          {selected && <Marker position={selected} />}
        </GoogleMap>
      </Box>
    </Box>
  );
}
