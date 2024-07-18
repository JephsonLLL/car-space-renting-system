import React from "react";
import { useNavigate } from "react-router-dom";
import IconLabelButtons from "../components/IconLabelButton";
import MultilineTextFields from "@mui/material/TextField";
import Rating from "@mui/material/Rating";
import BasicButton from "../components/BasicButton";
import Tooltip from "@mui/material/Tooltip";
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";

const Rate = () => {
  async function changePwd(credentials) {
    return fetch("/api/", {
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

  const [comment, setComment] = React.useState("");
  const [rating, setRating] = React.useState("");
  const [score, setScore] = React.useState("");
  const [notClean, setNotClean] = React.useState(false);
  const [notLargeEnough, setNotLargeEnough] = React.useState(false);
  const [notConvenient, setNotConvenient] = React.useState(false);
  const [lowQualityPriceRatio, setLowQualityPriceRatio] = React.useState(false);
  const [veryClean, setVeryClean] = React.useState(false);
  const [veryLarge, setVeryLarge] = React.useState(false);
  const [veryConvenient, setVeryConvenient] = React.useState(false);
  const [highQualityPriceRatio, setHighQualityPriceRatio] = React.useState(
    false
  );
  const [clickCount1, setClickCount1] = React.useState(0);
  const [clickCount2, setClickCount2] = React.useState(0);
  const [clickCount3, setClickCount3] = React.useState(0);
  const [clickCount4, setClickCount4] = React.useState(0);
  const [clickCount5, setClickCount5] = React.useState(0);
  const [clickCount6, setClickCount6] = React.useState(0);
  const [clickCount7, setClickCount7] = React.useState(0);
  const [clickCount8, setClickCount8] = React.useState(0);

  const handleTag1Click = () => {
    // Toggle the clickCount between 0 and 1 (for two clicks)
    setClickCount1((prevCount) => (prevCount + 1) % 2);
    if (clickCount1 % 2 === 1) {
      setNotClean(true);
    } else {
      setNotClean(false);
    }
  };
  const handleTag2Click = () => {
    // Toggle the clickCount between 0 and 1 (for two clicks)
    setClickCount2((prevCount) => (prevCount + 1) % 2);
    if (clickCount2 % 2 === 1) {
      setNotLargeEnough(true);
    } else {
      setNotLargeEnough(false);
    }
  };
  const handleTag3Click = () => {
    // Toggle the clickCount between 0 and 1 (for two clicks)
    setClickCount3((prevCount) => (prevCount + 1) % 2);
    if (clickCount3 % 2 === 1) {
      setNotConvenient(true);
    } else {
      setNotConvenient(false);
    }
  };
  const handleTag4Click = () => {
    // Toggle the clickCount between 0 and 1 (for two clicks)
    setClickCount4((prevCount) => (prevCount + 1) % 2);
    if (clickCount4 % 2 === 1) {
      setLowQualityPriceRatio(true);
    } else {
      setLowQualityPriceRatio(false);
    }
  };
  const handleTag5Click = () => {
    // Toggle the clickCount between 0 and 1 (for two clicks)
    setClickCount5((prevCount) => (prevCount + 1) % 2);
    if (clickCount5 % 2 === 1) {
      setVeryClean(true);
    } else {
      setVeryClean(false);
    }
  };
  const handleTag6Click = () => {
    // Toggle the clickCount between 0 and 1 (for two clicks)
    setClickCount6((prevCount) => (prevCount + 1) % 2);
    if (clickCount6 % 2 === 1) {
      setVeryLarge(true);
    } else {
      setVeryLarge(false);
    }
  };
  const handleTag7Click = () => {
    // Toggle the clickCount between 0 and 1 (for two clicks)
    setClickCount7((prevCount) => (prevCount + 1) % 2);
    if (clickCount7 % 2 === 1) {
      setVeryConvenient(true);
    } else {
      setVeryConvenient(false);
    }
  };
  const handleTag8Click = () => {
    // Toggle the clickCount between 0 and 1 (for two clicks)
    setClickCount8((prevCount) => (prevCount + 1) % 2);
    if (clickCount8 % 2 === 1) {
      setHighQualityPriceRatio(true);
    } else {
      setHighQualityPriceRatio(false);
    }
  };

  const submitBtn = async () => {
    const body = {
      comment,
      rating,
      score
    };
    //print in console
    ///POST request
    console.log(body);
  };
  return (
    <>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          flexDirection: "column",
          height: "50vh",
          marginTop: "10vh"
        }}
      >
        <label>Rating:</label>
        <Rating
          name="simple-controlled"
          score={score}
          onChange={(event) => {
            setScore(event.target.value);
          }}
        />
        <br />
        <MultilineTextFields
          type="text"
          id="outlined-multiline-static"
          label="Leave your comment here..."
          multiline
          rows={4}
          style={{ width: "50vw" }}
          onChange={(event) => setComment(event.target.value)}
        ></MultilineTextFields>
        {/* Tags */}
        <br />
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexDirection: "row"
          }}
        >
          <Grid>
            <Grid container justifyContent="center">
              <Grid item>
                <Tooltip title="Add" placement="top-start">
                  <Button
                    variant={clickCount1 === 1 ? "contained" : "outlined"}
                    color="success"
                    onClick={handleTag1Click}
                  >
                    Not clean
                  </Button>
                </Tooltip>
                <Tooltip title="Add" placement="top">
                  <Button
                    variant={clickCount2 === 1 ? "contained" : "outlined"}
                    color="success"
                    onClick={handleTag2Click}
                  >
                    Not large enough
                  </Button>
                </Tooltip>
                <Tooltip title="Add" placement="top">
                  <Button
                    variant={clickCount3 === 1 ? "contained" : "outlined"}
                    color="success"
                    onClick={handleTag3Click}
                  >
                    Not convenient
                  </Button>
                </Tooltip>
                <Tooltip title="Add" placement="top-end">
                  <Button
                    variant={clickCount4 === 1 ? "contained" : "outlined"}
                    color="success"
                    onClick={handleTag4Click}
                  >
                    Low quality price ratio
                  </Button>
                </Tooltip>
              </Grid>
            </Grid>

            <Grid container justifyContent="center">
              <Grid item>
                <Tooltip title="Add" placement="top-start">
                  <Button
                    variant={clickCount5 === 1 ? "contained" : "outlined"}
                    color="success"
                    onClick={handleTag5Click}
                  >
                    Very clean
                  </Button>
                </Tooltip>
                <Tooltip title="Add" placement="top">
                  <Button
                    variant={clickCount6 === 1 ? "contained" : "outlined"}
                    color="success"
                    onClick={handleTag6Click}
                  >
                    Very large
                  </Button>
                </Tooltip>
                <Tooltip title="Add" placement="top">
                  <Button
                    variant={clickCount7 === 1 ? "contained" : "outlined"}
                    color="success"
                    onClick={handleTag7Click}
                  >
                    Very convenient
                  </Button>
                </Tooltip>
                <Tooltip title="Add" placement="top-end">
                  <Button
                    variant={clickCount8 === 1 ? "contained" : "outlined"}
                    color="success"
                    onClick={handleTag8Click}
                  >
                    High quality price ratio
                  </Button>
                </Tooltip>
              </Grid>
            </Grid>
          </Grid>
        </div>
        <br />
        <IconLabelButtons onClick={submitBtn}>Submit</IconLabelButtons>
        <br />
      </div>
    </>
  );
};

export default Rate;