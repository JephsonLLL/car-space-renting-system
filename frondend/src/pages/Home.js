import React from "react";
import { useNavigate } from "react-router-dom";
import IconLabelButtons from "../components/IconLabelButton";
import BasicTextFields from "../components/BasicTextField";
import ImageButton from "../components/ImageButton";
import PropTypes from "prop-types";

const main_windows = [
  {
    img_url: "../images/768x350_Smart-parking.jpg",
    name: "Starred Spaces",
    dest: "/FindCarSpace"
  },
  {
    img_url:
      "https://images.rawpixel.com/image_800/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIyLTA3L2pvYjk0OS0wNzMtdl80LmpwZw.jpg",
    name: "Recommended For You",
    dest: "/FindCarSpace"
  },
  {
    img_url: "../images/lightning.png",
    name: "Quick Park",
    dest: "/FindCarSpace"
  }
];

const Home = (props) => {
  const [search, setSearch] = React.useState("");

  const navigate = useNavigate();
  const searchBtn = async () => {
    const body = {
      search
    };
    //print in console
    console.log(body);
    //get request
    localStorage.setItem("search", search);
    //jump to next search page
    navigate("/FindCarSpace");
  };

  const toMap = async () => {
    navigate("/FindCarSpace");
  };

  return (
    <>
      <h1
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          flexDirection: "column",
          height: "20vh"
        }}
      >
        Car Space Systems
      </h1>
      <br />
      {/* search bar */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          flexDirection: "row"
        }}
      >
        {/* style of search box and button change later */}
        <IconLabelButtons name="searchButton" fullWidth onClick={searchBtn}>
          Find a space
        </IconLabelButtons>
      </div>
      {/* container for three windows */}
      <div
        classNmae="container"
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          flexDirection: "row",
          marginTop: "5vh"
        }}
      >
        {main_windows.map((window) => (
          <div
            name={window.name}
            style={{
              alignItems: "center",
              width: "30vw",
              height: "50vh",
              marginRight: "1vw"
            }}
          >
            <ImageButton
              label={window.name}
              fullWidth
              url={window.img_url}
              width="100%"
              onClick={toMap}
            />
          </div>
        ))}
      </div>
    </>
  );
};

export default Home;
