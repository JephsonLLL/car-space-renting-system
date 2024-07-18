import React from "react";

import Register from "../pages/Register";
import Home from "../pages/Home";
import Profile from "../pages/Profile";
import RegisterCarSpace from "../pages/RegisterCarSpace";
import UpdateCarSpaceDetail from "../pages/UpdateCarSpaceDetail";
import CarSpaceDetail from "../pages/CarSpaceDetail";
import CarSpaceInfo from "../pages/CarSpaceInfo";
import Booking from "../pages/Booking";
import Rate from "../pages/Rate";
import Starred from "../pages/Starred";
import Payment from "../pages/Payment";
import FindCarSpace from "../pages/FindCarSpace";

import IconLabelButtons from "./IconLabelButton";
import TextButtonGroup from "./TextButtonGroup";
import Button from "./BasicButton";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import MenuList from "@mui/material/MenuList";
import Grow from "@mui/material/Grow";
import Paper from "@mui/material/Paper";
import Popper from "@mui/material/Popper";

import ChangePassword from "../pages/ChangPassword";
import Login from "../pages/Login";

import { Routes, Route, useNavigate, useLocation } from "react-router-dom";

function Site() {
  const navigate = useNavigate();
  const homeBtn = () => {
    navigate("/");
  };
  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);
  const onClickHandler = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const closeMenu = () => {
    setAnchorEl(null);
  };

  const onClickProfile = () => {
    navigate("/profile");
  };

  const onClickBooking = () => {
    navigate("/booking");
  };

  const onClickRegisterCarSpace = () => {
    navigate("/registerCarSpace");
  };

  const onClickStarred = () => {
    navigate("/starred");
  };

  const onClickChangepassword = () => {
    navigate("/change_password");
  };

  const onClickLogout = () => {
    navigate("/login");
  };

  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/registerCarSpace" element={<RegisterCarSpace />} />
        <Route path="/register" element={<Register />} />
        <Route path="/profile" element={<Profile />} />
        <Route
          path="/updateCarSpaceDetail"
          element={<UpdateCarSpaceDetail />}
        />
        <Route path="/carSpaceDetail" element={<CarSpaceDetail />} />
        <Route path="/carSpaceInfo" element={<CarSpaceInfo />} />
        <Route path="/booking" element={<Booking />} />
        <Route path="/rate" element={<Rate />} />
        <Route path="/starred" element={<Starred />} />
        <Route path="/payment" element={<Payment />} />
        <Route path="/findcarspace" element={<FindCarSpace />} />
        <Route path="/change_password" element={<ChangePassword />} />
        <Route path="/login" element={<Login />} />
      </Routes>
      {/* nav bar can be displayed only after login in, modify later*/}
      {
        <div
          style={{ position: "absolute", top: "10px", alignItems: "center" }}
        >
          <TextButtonGroup>
            <Button onClick={homeBtn}>Home</Button>
            {/* <Button>Notifications</Button>
                <Button>My Reward Points</Button> */}
            <Button onClick={onClickRegisterCarSpace}>
              Register a new car space
            </Button>
            <Button onClick={onClickProfile}>Personal Profile</Button>
            <Button onClick={onClickLogout}>Provided Car Space</Button>
            <Button onClick={onClickBooking}>Bookings</Button>
            <Button onClick={onClickChangepassword}>Change password</Button>
            <Button onClick={onClickLogout}>Logout</Button>

            {/* <Button
                  onClick={onClickHandler} 
                  aria-controls="basic-menu"
                  aria-haspopup="true"
                  aria-expanded={open ? 'true' : undefined}
                >My Account</Button>
                <Menu 
                  open={open}
                  onClose={closeMenu}
                  MenuListProps={{
                    'aria-labelledby': 'basic-button',
                  }}
                  >
                    <MenuItem onClick={onClickProfile}>Personal Profile</MenuItem>
                    <MenuItem>Provided Car Space</MenuItem>
                    <MenuItem onClick={onClickBooking}>Bookings</MenuItem>
                    <MenuItem onClick={onClickStarred}>Starred</MenuItem>
                    <MenuItem>Change password</MenuItem>
                    <MenuItem>Logout</MenuItem>
                </Menu> */}
          </TextButtonGroup>
        </div>
      }
    </>
  );
}

export default Site;
