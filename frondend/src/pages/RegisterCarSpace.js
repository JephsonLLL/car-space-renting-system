import React, { useState, useMemo } from "react";
import { useNavigate } from "react-router-dom";

import { GoogleMap, Marker, useLoadScript } from "@react-google-maps/api";

import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { DateRangePicker } from "@mui/x-date-pickers-pro/DateRangePicker";
import { DemoItem } from "@mui/x-date-pickers/internals/demo";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";

import SearchPlaces from "../components/search";

import {
  Container,
  Box,
  Step,
  Stepper,
  StepLabel,
  Typography,
  Grid,
  TextField,
  Button,
  FormControl,
  OutlinedInput,
  InputAdornment,
  InputLabel,
  FormControlLabel,
  Switch,
  FormGroup
} from "@mui/material";

async function register(credentials) {
  return fetch("/api/register_car_space", {
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

async function recPrice(credentials) {
  return fetch("/api/recommendPrice", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(credentials)
  }).then((response) => {
    if (response.ok) {
      return response.json();
    }
    throw new Error("Something went wrong");
  });
}

const RegisterCarSpace = () => {
  const navigate = useNavigate();

  const { isLoaded } = useLoadScript({
    googleMapsApiKey: "AIzaSyDpsPxJU1pU4V_LhqoOK3HUjAVsibLc8Lg",
    libraries: ["places"],
    language: "en"
  });

  const [selected, setSelected] = useState("");
  const center = useMemo(() => ({ lat: -33.911, lng: 151.23 }), []);

  const [address, setAddress] = React.useState(null);
  const [addressError, setAddressError] = React.useState("");
  const [lat, setlat] = React.useState(0);
  const [lng, setlng] = React.useState(0);

  const [spaceLength, setSpaceLength] = React.useState(null);
  const [spaceLengthError, setSpaceLengthError] = React.useState("");

  const [spaceWidth, setSpaceWidth] = React.useState(null);
  const [spaceWidthError, setSpaceWidthError] = React.useState("");

  const [availableDate, setAvailableDate] = React.useState(null);
  const [availableDateError, setAvailableDateError] = React.useState("");

  const [price, setPrice] = React.useState(null);
  const [priceError, setPriceError] = React.useState("");

  const [autoprice, setAutoPrice] = React.useState(false);

  const submitBtn = async (e) => {
    // judge each input is fullfilled the restrictions or not
    // restrcition:
    // carspacename: 1-20 characters
    // cost: 1-5 int numeber
    // startTime and endTime: calendar input
    // bsb: must be 6 int number
    // accountNumber: must be 8 or 9 int number
    //console.log(availableDate)

    e.preventDefault();
    await register({
      address,
      lat,
      lng,
      spaceLength,
      spaceWidth,
      availableDate,
      price
    })
      .then((response) => {
        console.log(response);
        navigate("/");
      })
      .catch((error) => {
        console.log(error);
        alert('Carspace already been registed')
      });
  };

  //current step number
  const [activeStep, setActiveStep] = React.useState(0);
  //all steps
  const steps = ["Step1", "Step2", "Step3", "Step4", "Step5"];
  //to next step
  const handleNext = () => {
    switch (activeStep) {
      case 0:
        if (!address) {
          setAddressError("Please enter an address");
          return;
        }
        setAddressError("");
        break;
      case 1:
        if (!spaceLength || spaceLength <= 3) {
          setSpaceLengthError("Please enter a valid space length");
          return;
        }
        setSpaceLengthError("");
        if (!spaceWidth || spaceWidth <= 1.5) {
          setSpaceWidthError("Please enter a valid space width");
          return;
        }
        setSpaceWidthError("");
        break;
      case 2:
        if (!availableDate) {
          setAvailableDateError("Please select an available date");
          return;
        }
        setAvailableDateError("");
        break;
      case 3:
        if (!price || price <= 0) {
          setPriceError("Please enter a valid price");
          return;
        }
        setPriceError("");
        break;
      default:
        break;
    }
    setActiveStep(activeStep + 1);
  };
  //go back to previous step
  const handleBack = () => {
    setActiveStep(activeStep - 1);
  };

  const handleSwitch = (event) => {
    setAutoPrice(event.target.checked);
    //console.log(!autoprice)
    if (!autoprice) {
      recPrice({
        lat,
        lng,
        spaceLength,
        spaceWidth
      })
        .then((response) => {
          const c = JSON.parse(response.price);
          //const p = response.price.json().price;
          setPrice(c.price);
          console.log(price);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  };

  if (!isLoaded) return <div>Loading...</div>;

  return (
    <Container maxWidth="sm" sx={{ mt: 13 }}>
      <Typography component="h1" variant="h6" align="center">
        Register Your Car Space
      </Typography>

      <Stepper activeStep={activeStep} sx={{ mt: 4 }}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>

      <Grid container direction="column" alignItems="center" spacing={2}>
        <Grid item xs={12}>
          {activeStep === 0 && (
            <>
              <Typography variant="subtitle1" align="center" sx={{ mt: 4 }}>
                Choose car space address
              </Typography>

              <SearchPlaces
                setSelected={setSelected}
                setlat={setlat}
                setlng={setlng}
                setAddress={setAddress}
              />

              {addressError && (
                <Typography color="error" sx={{ mt: 1 }}>
                  {addressError}
                </Typography>
              )}

              <GoogleMap
                mapContainerStyle={{ width: "210px", height: "210px" }}
                center={center}
                zoom={10}
              >
                {selected && <Marker position={selected} />}
              </GoogleMap>
            </>
          )}

          {activeStep === 1 && (
            <>
              <Typography variant="subtitle1" align="center" sx={{ mt: 4 }}>
                Your car space size
              </Typography>

              <Grid item xs={12}>
                <FormControl size="small" variant="outlined" sx={{ mt: 2 }}>
                  <InputLabel>Car Space Length *</InputLabel>
                  <OutlinedInput
                    id="length"
                    type="number"
                    label="Car Space Length"
                    step="0.1"
                    required
                    endAdornment={
                      <InputAdornment position="end">m</InputAdornment>
                    }
                    onChange={(e) => setSpaceLength(e.target.value)}
                    inputProps={{
                      step: 0.1
                    }}
                  />
                </FormControl>
                {spaceLengthError && (
                  <Typography color="error" sx={{ mt: 1 }}>
                    {spaceLengthError}
                  </Typography>
                )}
              </Grid>

              <Grid item xs={12}>
                <FormControl size="small" variant="outlined" sx={{ mt: 2 }}>
                  <InputLabel>Car Space Width *</InputLabel>
                  <OutlinedInput
                    id="width"
                    type="number"
                    step="0.1"
                    label="Car Space Width"
                    required
                    endAdornment={
                      <InputAdornment position="end">m</InputAdornment>
                    }
                    onChange={(e) => setSpaceWidth(e.target.value)}
                    inputProps={{
                      step: 0.1
                    }}
                  />
                </FormControl>
                {spaceWidthError && (
                  <Typography color="error" sx={{ mt: 1 }}>
                    {spaceWidthError}
                  </Typography>
                )}
              </Grid>
            </>
          )}

          {activeStep === 2 && (
            <>
              <Typography variant="subtitle1" align="center" sx={{ mt: 4 }}>
                Set available date
              </Typography>

              <LocalizationProvider dateAdapter={AdapterDayjs}>
                <DemoItem component="DateRangePicker">
                  <DateRangePicker
                    disablePast
                    onChange={(newValue) => setAvailableDate(newValue)}
                    sx={{ mt: 2 }}
                  />
                </DemoItem>
                {availableDateError && (
                  <Typography color="error" sx={{ mt: 1 }}>
                    {availableDateError}
                  </Typography>
                )}
              </LocalizationProvider>
            </>
          )}

          {activeStep === 3 && (
            <>
              <Typography variant="subtitle1" align="center" sx={{ mt: 4 }}>
                Set price
              </Typography>

              <Grid item xs={12}>
                <FormControl size="small" variant="outlined" sx={{ mt: 2 }}>
                  <OutlinedInput
                    id="price"
                    type="number"
                    //disabled
                    disabled={autoprice}
                    //label='Car Space price per day'
                    endAdornment={
                      <InputAdornment position="end">$</InputAdornment>
                    }
                    value={price}
                    onChange={(e) => setPrice(e.target.value)}
                    inputProps={{
                      step: 0.1
                    }}
                  />
                </FormControl>
                {priceError && (
                  <Typography color="error" sx={{ mt: 1 }}>
                    {priceError}
                  </Typography>
                )}
              </Grid>

              <Grid item xs={12}>
                <Box sx={{ display: "flex", flexDirection: "row", ml: 1 }}>
                  <Typography variant="body1" sx={{ m: 1 }}>
                    Recommend price:
                  </Typography>
                  <Switch onChange={handleSwitch} sx={{ mt: 0.2 }} />
                </Box>
              </Grid>
            </>
          )}

          {activeStep === 4 && (
            <>
              <Typography variant="subtitle1" align="center" sx={{ mt: 4 }}>
                Confirm Car Space Information
              </Typography>
              <Grid container spacing={2} sx={{ mt: 2 }}>
                <Grid item xs={12}>
                  <Typography variant="body1">
                    {" "}
                    <strong>Address:</strong> {address}
                  </Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="body1">
                    <strong>Car Space Size:</strong> {spaceLength}{" "}
                    <strong>m</strong> x {spaceWidth} <strong>m</strong>
                  </Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="body1">
                    <strong>Available Date:</strong>{" "}
                    {availableDate &&
                      `${new Date(
                        availableDate[0]
                      ).toLocaleDateString()} - ${new Date(
                        availableDate[1]
                      ).toLocaleDateString()}`}
                  </Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="body1">
                    {" "}
                    <strong>Price:</strong> ${price}
                  </Typography>
                </Grid>
              </Grid>
            </>
            // <>
            //   <Typography variant="subtitle1" align="center" sx={{ mt: 4 }}>
            //     Confirm
            //   </Typography>
            // </>
          )}
        </Grid>

        <Grid item xs={12}>
          {activeStep > 0 && (
            <Button variant="outlined" color="inherit" onClick={handleBack}>
              Back
            </Button>
          )}

          {activeStep < steps.length - 1 ? (
            <Button
              variant="contained"
              color="inherit"
              onClick={handleNext}
              sx={{ marginLeft: 8 }}
            >
              Next
            </Button>
          ) : (
            <Button
              variant="contained"
              color="inherit"
              onClick={submitBtn}
              sx={{ marginLeft: 8 }}
            >
              Submit
            </Button>
          )}
        </Grid>
      </Grid>
    </Container>
  );
};

export default RegisterCarSpace;