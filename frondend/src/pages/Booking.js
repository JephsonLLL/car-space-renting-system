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
        
      </Box>

      
    </Box>
  );
}
