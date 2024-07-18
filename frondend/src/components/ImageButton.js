import * as React from "react";
import { styled } from "@mui/material/styles";
import Box from "@mui/material/Box";
import ButtonBase from "@mui/material/ButtonBase";
import PropTypes from "prop-types";

const ContainerButton = styled(ButtonBase)(({ theme }) => ({
  position: "relative",
  height: 300,
  "&:hover, &.Mui-focusVisible": {
    zIndex: 1,
    "& .MuiImageBackdrop-root": {
      opacity: 0.5
    },
    "& .MuiTypography-root": {
      border: "4px solid currentColor"
    }
  }
}));

const ImageSrc = styled("span")({
  position: "absolute",
  left: 0,
  right: 0,
  top: 0,
  bottom: 0,
  layout: "fill",
  backgroundSize: "cover",
  backgroundPosition: "center 40%"
});

const Image = styled("span")(({ theme }) => ({
  position: "absolute",
  left: 0,
  right: 0,
  top: 0,
  bottom: 0,
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  color: theme.palette.common.white
}));

const ImageBackdrop = styled("span")(({ theme }) => ({
  position: "absolute",
  left: 0,
  right: 0,
  top: 0,
  bottom: 0,
  backgroundColor: theme.palette.common.black,
  opacity: 0.15,
  transition: theme.transitions.create("opacity")
}));

const ImageButton = (props) => {
  return (
    <Box sx={{ display: "flex", flexWrap: "wrap", width: "100%" }}>
      <ContainerButton
        focusRipple
        onClick={props.onClick}
        style={{
          width: props.width
        }}
      >
        <ImageSrc style={{ backgroundImage: `url(${props.url})` }} />
        <ImageBackdrop className="MuiImageBackdrop-root" />
        <Image>{props.label}</Image>
      </ContainerButton>
    </Box>
  );
};

export default ImageButton;
