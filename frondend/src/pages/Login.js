import React from "react";
import { useNavigate } from "react-router-dom";
import IconLabelButtons from "../components/IconLabelButton";
import BasicTextFields from "../components/BasicTextField";
import PropTypes from "prop-types";

import VisibilityIcon from "@mui/icons-material/Visibility";
import VisibilityOffIcon from "@mui/icons-material/VisibilityOff";
import {
  Container,
  Step,
  Link,
  Stepper,
  StepLabel,
  Typography,
  Grid,
  TextField,
  Button,
  InputAdornment,
  FormControl,
  OutlinedInput,
  InputLabel,
  IconButton,
  Box
} from "@mui/material";

// Function to validate the email address format
function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// Function to validate the password format
function validatePassword(password) {
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
  return passwordRegex.test(password);
}

async function loginUser(credentials) {
  return fetch("/api/login", {
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

export default function Login({ setToken }) {
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [emailError, setEmailError] = React.useState("");
  const [passwordError, setPasswordError] = React.useState("");
  const [showPassword, setShowPassword] = React.useState(false);

  const loginBtn = async (e) => {
    e.preventDefault();

    // Validate the email address format
    if (!validateEmail(email)) {
      setEmailError("Please enter a valid email address.");
      return;
    }

    // Validate the password format
    if (!validatePassword(password)) {
      setPasswordError("Invalid Password");
      return;
    }

    // Clear previous error messages
    setEmailError("");
    setPasswordError("");

    // Send login request
    await loginUser({
      email,
      password
    })
      .then((response) => {
        setToken(response.access_token);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          flexDirection: "column",
          height: "50vh"
        }}
      >
        <Typography component="h1" variant="h6">
          Account Login
        </Typography>
        <TextField
          margin="none"
          variant="outlined"
          required
          id="email"
          type="email"
          label="Email Address"
          name="email"
          autoComplete="email"
          autoFocus="true"
          size="small"
          onChange={(e) => setEmail(e.target.value)}
          error={!!emailError}
          helperText={emailError}
        />
        <br />
        <TextField
          margin="none"
          variant="outlined"
          required
          name="password"
          label="Password"
          type="password"
          id="password"
          autoComplete="current-password"
          size="small"
          onChange={(e) => setPassword(e.target.value)}
          error={!!passwordError}
          helperText={passwordError}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton
                  aria-label="toggle password visibility"
                  onClick={() => setShowPassword(!showPassword)}
                  edge="end"
                >
                  {showPassword ? <VisibilityIcon /> : <VisibilityOffIcon />}
                </IconButton>
              </InputAdornment>
            )
          }}
        />
        <br />
        <IconLabelButtons onClick={loginBtn}>Log in</IconLabelButtons>
        <br />
        <Link href="/register" variant="body2">
          {"Don't have an account? Sign Up"}
        </Link>
      </div>
    </>
  );
}