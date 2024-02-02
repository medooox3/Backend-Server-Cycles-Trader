import * as React from 'react';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';

import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';



export default function LicesnceForm({ LicenseStart, setLicenseStart, LicenseExp, setLicenseExp, AccountId, setAccountId, AccountName, setAccountName }) {
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
            variant="standard"
            value={AccountId}
            onChange={(e) => setAccountId(e.target.value)}

          />
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField
            required
            id="Name"
            label="Account Name"
            fullWidth
            variant="standard"
            value={AccountName}
            onChange={(e) => setAccountName(e.target.value)}


          />
        </Grid>
        <Grid item xs={12} md={6}>
          <LocalizationProvider dateAdapter={AdapterDayjs} >
            <DatePicker label="Start Date" variant="standard" value={LicenseStart} onChange={(e) => setLicenseStart(e)} />
          </LocalizationProvider>

        </Grid>
        <Grid item xs={12} md={6}>
          <LocalizationProvider dateAdapter={AdapterDayjs} >
            <DatePicker label="Expiry Date" variant="standard" value={LicenseExp} onChange={(e) => setLicenseExp(e)} />
          </LocalizationProvider>
         
        </Grid>

      </Grid>
    </React.Fragment>
  );
}