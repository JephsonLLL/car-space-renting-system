import React from "react";
import { useNavigate } from "react-router-dom";
import IconLabelButtons from "../components/IconLabelButton";
import BasicTextFields from "../components/BasicTextField";
import PropTypes from "prop-types";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Link from "@mui/material/Link";

// Function to validate the Australian phone number format
function validatePhoneNumber(phoneNumber) {
  const phoneRegex = /^(?:\+?61|0)[2-478](?:[ -]?[0-9]){8}$/;
  return phoneRegex.test(phoneNumber);
}

async function updateUserProfile(credentials) {
  return fetch("/api/update_personal_profile", {
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

const UpdateProfile = (props) => {
  const [firstname, setFirstname] = React.useState("");
  const [lastname, setLastname] = React.useState("");
  const [phone, setPhone] = React.useState("");
  const [carLicense, setCarLicense] = React.useState("");
  const [phoneError, setPhoneError] = React.useState("");

  const updateBtn = async (e) => {
    e.preventDefault();

    // Validate the Australian phone number format
    if (!validatePhoneNumber(phone)) {
      setPhoneError("Invalid Phone Number");
      return;
    }
    // Clear previous error messages
    setPhoneError("");

    await updateUserProfile({
      firstname,
      lastname,
      phone,
      carLicense
    })
      .then((response) => {
        console.log(response);
        // Handle successful update if needed
      })
      .catch((error) => {
        console.log(error);
      });
  };

  // const navigate = useNavigate()
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        flexDirection: "column",
        height: "60vh"
      }}
    >
      <Typography component="h5" variant="h5" sx={{mt:5}}>
        Update Personal Details
      </Typography>

      <div style={{ marginTop: "20px", width: "50%" }}>
        <div style={{ marginBottom: "10px" }}>
          <center>
            <BasicTextFields
              name="firstname"
              type="text"
              onChange={(event) => setFirstname(event.target.value)}
              value={firstname}
              error={false}
              helperText={null}
              size='small'
            >
              First Name
            </BasicTextFields>
          </center>
        </div>

        <div style={{ marginBottom: "10px" }}>
          <center>
            <BasicTextFields
              name="lastname"
              type="text"
              onChange={(event) => setLastname(event.target.value)}
              value={lastname}
              error={false}
              helperText={null}
              size='small'
            >
              Last Name
            </BasicTextFields>
          </center>
        </div>

        <div style={{ marginBottom: "10px" }}>
          <center>
            <BasicTextFields
              name="phone"
              type="text"
              onChange={(event) => setPhone(event.target.value)}
              value={phone}
              error={!!phoneError}
              helperText={phoneError}
              size='small'
            >
              Phone
            </BasicTextFields>
          </center>
        </div>

        <div style={{ marginBottom: "10px" }}>
          <center>
            <BasicTextFields
              name="carLicense"
              type="text"
              onChange={(event) => setCarLicense(event.target.value)}
              value={carLicense}
              error={false}
              helperText={null}
              size='small'
            >
              Car License
            </BasicTextFields>
          </center>
        </div>

        <div style={{ display: "flex", justifyContent: "center" }}>
          <IconLabelButtons
            name="updateButton"
            color={"primary"}
            onClick={updateBtn}
          >
            Update
          </IconLabelButtons>
        </div>
      </div>
    </div>
  );
};

export default UpdateProfile;
