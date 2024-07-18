import React from "react";
import { useNavigate } from "react-router-dom";
import UpgradeOutlinedIcon from "@mui/icons-material/UpgradeOutlined";
import VisibilityIcon from "@mui/icons-material/Visibility";
import VisibilityOffIcon from "@mui/icons-material/VisibilityOff";
import {
  Typography,
  TextField,
  Button,
  InputAdornment,
  FormControl,
  OutlinedInput,
  InputLabel,
  IconButton,
  FormHelperText,
  Box
} from "@mui/material";

async function changePwd(credentials) {
  return fetch("/api/change_password", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "*",
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

// Helper function to validate password format
function validatePassword(password) {
  const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
  return passwordPattern.test(password);
}

const ChangePassword = () => {
  const [password, setPassword] = React.useState("");
  const [confirm_password, setConfirmPassword] = React.useState("");
  const [passwordsMatch, setPasswordsMatch] = React.useState(true);
  const [validPassword, setValidPassword] = React.useState(true);
  const [showPassword, setShowPassword] = React.useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = React.useState(false);

  const handleConfirmPasswordChange = (event) => {
    setConfirmPassword(event.target.value);
    setPasswordsMatch(password === event.target.value);
  };

  const updateBtn = async (e) => {
    e.preventDefault();

    // Check if new password and confirm password match
    if (!passwordsMatch) {
      setConfirmPassword("");
      setPassword("");
      alert("Passwords Do Not Match!");
      return;
    }

    // Check if the new password is valid (at least 8 characters long)
    if (!validatePassword(password)) {
      setValidPassword(false);
      return;
    } else {
      setValidPassword(true);
    }

    await changePwd({
      password,
      confirm_password
    })
      .then((response) => {
        console.log(response);
        if (response.status === 200) {
          alert("Password Updated Successfully!");
        }
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
          flexDirection: "row",
          alignItems: "center",
          justifyContent: "center"
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            marginTop: "10vh",
            width: "30vw",
            border: "1px solid black",
            borderRadius: "10px",
            padding: "2vw"
          }}
        >
          <Typography
            variant="h5"
            gutterBottom
            component="div"
            color={{
              color: "Black"
            }}
          >
            Change Password
          </Typography>
          <br />
          <Box mt={2} mb={1}>
            <Typography variant="body2" color="textSecondary">
              (At least 8 characters with at least one uppercase letter, one
              lowercase letter, one number, and one special symbol)
            </Typography>
          </Box>
          <FormControl size="small" variant="outlined">
            <InputLabel>New Password</InputLabel>
            <OutlinedInput
              required
              name="password"
              type={showPassword ? "text" : "password"}
              size="small"
              onChange={(event) => setPassword(event.target.value)}
              error={!validPassword}
              // helperText={!validPassword && "Invalid Password"}
              inputProps={{
                minLength: 8
              }}
              endAdornment={
                <InputAdornment position="end">
                  <IconButton
                    onClick={() =>
                      setShowPassword((prevShowPassword) => !prevShowPassword)
                    }
                    edge="end"
                  >
                    {showPassword ? <VisibilityIcon /> : <VisibilityOffIcon />}
                  </IconButton>
                </InputAdornment>
              }
            />
            {!validPassword && (
              <FormHelperText error>Invalid Password</FormHelperText>
            )}
          </FormControl>
          <br />
          <FormControl size="small" variant="outlined">
            <InputLabel>Confirm Password</InputLabel>
            <OutlinedInput
              required
              name="confirm_password"
              type={showConfirmPassword ? "text" : "password"}
              size="small"
              onChange={handleConfirmPasswordChange}
              error={!passwordsMatch}
              // helperText={!passwordsMatch && "Passwords do not match"}
              inputProps={{
                minLength: 8
              }}
              endAdornment={
                <InputAdornment position="end">
                  <IconButton
                    onClick={() =>
                      setShowConfirmPassword(
                        (prevShowConfirmPassword) => !prevShowConfirmPassword
                      )
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
            {!passwordsMatch && (
              <FormHelperText error>Passwords do not match</FormHelperText>
            )}
          </FormControl>
          <br />
          <Button
            variant="contained"
            endIcon={<UpgradeOutlinedIcon />}
            onClick={updateBtn}
            href="/home"
          >
            Update
          </Button>
        </div>
      </div>
    </>
  );
};

export default ChangePassword;
