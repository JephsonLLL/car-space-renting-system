import React from 'react';

import usePlacesAutocomplete, {
   getGeocode,
   getLatLng,
 } from "use-places-autocomplete";

 import { 
  TextField,
  Autocomplete,
} from '@mui/material';
 
 //import { GoogleMap, Marker, useLoadScript } from "@react-google-maps/api";

 const SearchPlaces = ({setSelected,setlat,setlng,setAddress}) => {
  const {
    ready,
    value,
    suggestions: { data },
    setValue,
    clearSuggestions,
  } = usePlacesAutocomplete({
    requestOptions: {
      componentRestrictions: {country: "au"},
      //types: ["(regions)"]
    }
  });

  const handleSelect = async (event, description) => {
    // When user selects a place, we can replace the keyword without request data from API
    // by setting the second parameter to "false"
    setValue(description, false);
    clearSuggestions();
    //console.log(description);

    // Get latitude and longitude
    //const results = await getGeocode({ address: description })
    const results = await getGeocode({ address: description });
    const { lat, lng } = await getLatLng(results[0]);
    //console.log(lat);
    setSelected({ lat, lng })

    setAddress(description)
    setlat(lat)
    setlng(lng)
  };

  return (
    <Autocomplete
        freeSolo
        disableClearable
        disabled={!ready}
        options={data.map((option) => option.description)}
        autoComplete
        includeInputInList
        noOptionsText="No locations"
        inputValue={value}
        onInputChange={(event, newInputValue)  => 
          {setValue(newInputValue);
        }}

        onChange={handleSelect}
               
        renderInput={(params) => (
          <TextField
            {...params}
            size = 'small'
            required
            label="Car Space Address"
            sx={{mt: 2}}
          />
        )}
      />
  );
};

export default SearchPlaces;