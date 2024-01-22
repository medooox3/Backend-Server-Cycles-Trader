import * as React from 'react';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';

import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';

function BasicDatePicker(props) {
    const { text } = props;
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs} >
    
        <DatePicker label={text} variant="standard" />
    
    </LocalizationProvider>
  );
}

export default function LicesnceForm() {
  return (
    <React.Fragment>
      <Typography variant="h6" gutterBottom>
        License Information
      </Typography>

      <Grid container spacing={3} mt={2}>
        <Grid item xs={12} md={6}>
          <TextField
            required
            id="AccountID"
            label="MetaTrader Account ID"
            fullWidth
            autoComplete="cc-name"
            
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField
            required
            id="Name"a
            label="Account Name"
            fullWidth
            autoComplete="cc-number"
            
          />
        </Grid>
        <Grid item xs={12} md={6}>
            <BasicDatePicker text="Start Date" />
          {/* <TextField
            required
            id="expDate"
            label="Expiry date"
            fullWidth
            autoComplete="cc-exp"
            variant="standard"
          /> */}
        </Grid>
        <Grid item xs={12} md={6}>
            <BasicDatePicker text="Expiry Date"/>
          {/* <TextField
            required
            id="cvv"
            label="CVV"
            helperText="Last three digits on signature strip"
            fullWidth
            autoComplete="cc-csc"
            variant="standard"
          /> */}
        </Grid>
       
      </Grid>
    </React.Fragment>
  );
}