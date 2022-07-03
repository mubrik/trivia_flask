import * as React from 'react';
//material
import { Button } from '@mui/material';
// react router
import { useNavigate } from "react-router-dom";


const BaseNavButton = ({navTo, navText, ...props}) => {

  // nav
  const navigate = useNavigate();

  return(
    <Button
      {...props}
      onClick={() => navigate(navTo)}
    >
      {navText}
    </Button>
  );
};

export default BaseNavButton;