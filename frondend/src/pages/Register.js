import React from "react";
import { useNavigate } from "react-router-dom";
import VisibilityIcon from "@mui/icons-material/Visibility";
import VisibilityOffIcon from "@mui/icons-material/VisibilityOff";
import {
  Container,
  Step,
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

// Helper function to validate email format
function validateEmail(email) {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailPattern.test(email);
}

// Helper function to validate password format
function validatePassword(password) {
  const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
  return passwordPattern.test(password);
}

// Helper function to validate Australian phone number format
function validatePhoneNumber(phoneNumber) {
  const phoneRegex = /^(?:\+?61|0)[2-478](?:[ -]?[0-9]){8}$/;
  return phoneRegex.test(phoneNumber);
}

// Helper function to validate card number format
function validateCardNumber(cardNumber) {
  const cardNumberRegex = /^[0-9]{16}$/;
  return cardNumberRegex.test(cardNumber);
}

// Helper function to validate CVV format
function validateCVV(cvv) {
  const cvvRegex = /^[0-9]{3}$/;
  return cvvRegex.test(cvv);
}

async function signup(credentials) {
  return fetch("/api/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(credentials)
  }).then((data) => data.json());
}

const Register = () => {
  const navigate = useNavigate();

  const [firstname, setFirstName] = React.useState("");
  const [lastname, setLastName] = React.useState("");
  const [email, setEmail] = React.useState("");
  const [phoneNumber, setPhoneNumber] = React.useState("");
  const [phoneError, setPhoneError] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [confirmPassword, setConfirmPassword] = React.useState("");
  const [emailError, setEmailError] = React.useState("");
  const [passwordError, setPasswordError] = React.useState("");
  const [confirmPasswordError, setConfirmPasswordError] = React.useState("");
  const [showPassword, setShowPassword] = React.useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = React.useState(false);

  const [bankAccount, setBankAccount] = React.useState("");
  const [cvv, setCvv] = React.useState("");
  const [bankAccountError, setBankAccountError] = React.useState("");
  const [cvvError, setCVVError] = React.useState("");

  const [carlicense, setCarlicense] = React.useState("");

  const [activeStep, setActiveStep] = React.useState(0);
  //all steps
  const steps = ["Step1", "Step2", "Step3"];

  const handleNext1 = () => {
    // Get the value of the input box
    const phoneValue = phoneNumber.trim();
    const emailValue = email.trim();
    const passwordValue = password.trim();
    const confirmPasswordValue = confirmPassword.trim();

    // check phone number
    if (!validatePhoneNumber(phoneValue)) {
      setPhoneError("Invalid phone number");
      return;
    } else {
      setPhoneError("");
    }

    // check email address
    if (!validateEmail(emailValue)) {
      setEmailError("Invalid email address");
      return;
    } else {
      setEmailError("");
    }

    // check password
    if (!validatePassword(passwordValue)) {
      setPasswordError("Invalid password");
      return;
    } else {
      setPasswordError("");
    }

    // check confirm password
    if (confirmPasswordValue !== passwordValue) {
      setConfirmPasswordError("Passwords do not match");
      return;
    } else {
      setPasswordError("");
    }

    if (
      !phoneValue.trim() ||
      !emailValue.trim() ||
      !passwordValue.trim() ||
      !confirmPasswordValue.trim()
    ) {
      alert("Please fill in all required fields.");
      return;
    }

    setActiveStep(activeStep + 1);
  };

  const handleNext2 = () => {
    const cardNumberValue = bankAccount.trim();
    const cvvValue = cvv.trim();
    // check card number
    if (!validateCardNumber(cardNumberValue)) {
      setBankAccountError("Invalid Card Number");
      return;
    } else {
      setBankAccountError("");
    }

    // check cvv
    if (!validateCVV(cvvValue)) {
      setCVVError("Invalid CVV number");
      return;
    } else {
      setCVVError("");
    }
    // Check if any field is empty
    if (!cardNumberValue.trim() || !cvvValue.trim()) {
      alert("Please fill in all required fields.");
      return;
    }
    setActiveStep(activeStep + 1);
  };

  const handleSubmit = async () => {
    // Get the value of the input box
    const carLicenseValue = carlicense.trim();

    // Building user information objects
    const userInfo = {
      firstname,
      lastname,
      phoneNumber,
      email,
      password,
      bankAccount,
      cvv,
      carlicense,
      licensePlate: carLicenseValue
    };

    const response = await signup(userInfo);
    console.log(response);
    localStorage.setItem("token", response.access_token);
    navigate("/");
  };

  //go back to previous step
  const handleBack = () => {
    setActiveStep(activeStep - 1);
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 13 }}>
      <Typography component="h1" variant="h6" align="center">
        Sign up
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
                Basic information
              </Typography>
              <Grid
                container
                alignItems="center"
                spacing={2}
                columnSpacing={1}
                xs={5}
                sx={{ ml: 20, mt: 0.7 }}
              >
                <Grid item xs={6}>
                  <TextField
                    name="firstName"
                    required
                    fullWidth
                    label="First Name"
                    size="small"
                    type="text"
                    onChange={(event) => setFirstName(event.target.value)}
                  />
                </Grid>
                <Grid item xs={6}>
                  <TextField
                    required
                    fullWidth
                    label="Last Name"
                    name="lastName"
                    type="text"
                    size="small"
                    onChange={(event) => setLastName(event.target.value)}
                  />
                </Grid>

                <Grid item xs={12}>
                  <TextField
                    required
                    fullWidth
                    label="Phone Number"
                    name="Phone Number"
                    type="text"
                    size="small"
                    // inputRef={phoneNumberRef}
                    onChange={(event) => setPhoneNumber(event.target.value)}
                    error={!!phoneError}
                    helperText={phoneError}
                  />
                </Grid>

                <Grid item xs={12}>
                  <TextField
                    required
                    fullWidth
                    label="Email Address"
                    name="email"
                    type="email"
                    size="small"
                    // inputRef={emailRef}
                    onChange={(event) => setEmail(event.target.value)}
                    error={!!emailError}
                    helperText={emailError}
                  />
                </Grid>
                <Grid item xs={12}>
                  <FormControl fullWidth size="small" variant="outlined">
                    <InputLabel htmlFor="password">Password</InputLabel>
                    <OutlinedInput
                      id="password"
                      name="password"
                      label="Password"
                      type={showPassword ? "text" : "password"}
                      value={password}
                      onChange={(event) => setPassword(event.target.value)}
                      error={!!passwordError}
                      endAdornment={
                        <InputAdornment position="end">
                          <IconButton
                            aria-label="toggle password visibility"
                            onClick={() => setShowPassword(!showPassword)}
                            edge="end"
                          >
                            {showPassword ? (
                              <VisibilityIcon />
                            ) : (
                              <VisibilityOffIcon />
                            )}
                          </IconButton>
                        </InputAdornment>
                      }
                    />
                  </FormControl>
                  {passwordError && (
                    <Typography variant="caption" color="error">
                      {passwordError}
                    </Typography>
                  )}
                </Grid>
                <Grid item xs={12}>
                  <FormControl fullWidth size="small" variant="outlined">
                    <InputLabel htmlFor="confirmPassword">
                      Confirm Password
                    </InputLabel>
                    <OutlinedInput
                      id="confirmPassword"
                      name="confirmPassword"
                      label="Confirm Password"
                      type={showConfirmPassword ? "text" : "password"}
                      value={confirmPassword}
                      onChange={(event) =>
                        setConfirmPassword(event.target.value)
                      }
                      error={!!passwordError}
                      endAdornment={
                        <InputAdornment position="end">
                          <IconButton
                            aria-label="toggle confirm password visibility"
                            onClick={() =>
                              setShowConfirmPassword(!showConfirmPassword)
                            }
                            edge="end"
                          >
                            {showConfirmPassword ? (
                              <VisibilityIcon />
                            ) : (
                              <VisibilityOffIcon />
                            )}
                          </IconButton>
                        </InputAdornment>
                      }
                    />
                  </FormControl>
                  {confirmPasswordError && (
                    <Typography variant="caption" color="error">
                      {confirmPasswordError}
                    </Typography>
                  )}
                </Grid>
                <Grid item xs={12}>
                  <Box mt={2} mb={1}>
                    <Typography
                      variant="body2"
                      color="textSecondary"
                      sx={{ fontSize: "12px" }}
                    >
                      (At least 8 characters with at least one uppercase letter,
                      one lowercase letter, one number, and one special symbol)
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
              <Grid container justifyContent="center" sx={{ mt: 2 }}>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleNext1}
                >
                  Next
                </Button>
              </Grid>
            </>
          )}

          {activeStep === 1 && (
            <>
              <Typography variant="subtitle1" align="center" sx={{ mt: 4 }}>
                Bank Details
              </Typography>

              <Grid item xs={12} sx={{ mt: 2 }}>
                <TextField
                  required
                  fullWidth
                  label="Card Number"
                  name="Band Account"
                  size="small"
                  // inputRef={cardNumberRef}
                  onChange={(event) => setBankAccount(event.target.value)}
                  error={!!bankAccountError}
                  helperText={bankAccountError}
                />
              </Grid>

              <Grid item xs={12} sx={{ mt: 2 }}>
                <TextField
                  required
                  fullWidth
                  label="cvv"
                  name="cvv"
                  size="small"
                  // inputRef={cvvRef}
                  onChange={(event) => setCvv(event.target.value)}
                  error={!!cvvError}
                  helperText={cvvError}
                />
              </Grid>
              <Grid container justifyContent="center" sx={{ mt: 2 }}>
                <Button
                  variant="outlined"
                  color="inherit"
                  onClick={handleBack}
                  sx={{ marginRight: 2 }}
                >
                  Back
                </Button>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleNext2}
                >
                  Next
                </Button>
              </Grid>
            </>
          )}

          {activeStep === 2 && (
            <>
              <Typography variant="subtitle1" align="center" sx={{ mt: 4 }}>
                Consumer: car license
              </Typography>

              <Grid item xs={12} sx={{ mt: 2 }}>
                <TextField
                  required
                  fullWidth
                  label="Car license"
                  name="Car license"
                  size="small"
                  // inputRef={carLicenseRef}
                  onChange={(event) => setCarlicense(event.target.value)}
                />
              </Grid>
              <Grid container justifyContent="center" sx={{ mt: 2 }}>
                <Button
                  variant="outlined"
                  color="inherit"
                  onClick={handleBack}
                  sx={{ marginRight: 2 }}
                >
                  Back
                </Button>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleSubmit}
                  href="/login"
                >
                  Submit
                </Button>
              </Grid>
            </>
          )}
          {/* {renderBackButton()} */}
        </Grid>
      </Grid>
    </Container>
  );
};

export default Register;