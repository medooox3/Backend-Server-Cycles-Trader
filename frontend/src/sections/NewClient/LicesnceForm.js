import * as React from 'react';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';

export default function AddressForm({Name, setName, profileName, setProfileName, Email, setEmail, Phone, setPhone, Address, setAddress, City, setCity, State1, setState1, Zip, setZip, Country, setCountry}) {
  
  return (
    <React.Fragment>
      <Typography variant="h6" gutterBottom>
        Client Information
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6}>
          <TextField
            required
            id="userName"
            name="userName"
            label="User Name"
            fullWidth
            autoComplete="given-name"
            variant="standard"
            value={Name}
            onChange={(e) => setName(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            required
            id="FullName"
            name="FullName"
            label="Full Name"
            fullWidth
            autoComplete="family-name"  
            variant="standard"  
            value={profileName}
            onChange={(e) => setProfileName(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            required
           id="email"
            name="email"
            label="Email"
            autoComplete="email"
            variant="standard"
            value={Email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </Grid>
        <Grid item xs={12}sm={6} >
          <TextField
            required
            id="phone"
            name="phone"
            label="Phone"
            autoComplete="phone"
            variant="standard"
            value={Phone}
            onChange={(e) => setPhone(e.target.value)}
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            id="address2"
            name="address2"
            label="Address line 2"
            fullWidth
            autoComplete="shipping address-line2"
            variant="standard"
            value={Address}
            onChange={(e) => setAddress(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            required
            id="city"
            name="city"
            label="City"
            fullWidth
            autoComplete="shipping address-level2"
            variant="standard"
            value={City}
            onChange={(e) => setCity(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            id="state"
            name="state"
            label="State/Province/Region"
            fullWidth
            variant="standard"
            value={State1}
            onChange={(e) => setState1(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            
            id="zip"
            name="zip"
            label="Zip / Postal code"
            fullWidth
            autoComplete="shipping postal-code"
            variant="standard"
            value={Zip}
            onChange={(e) => setZip(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            required
            id="country"
            name="country"
            label="Country"
            fullWidth
            autoComplete="shipping country"
            variant="standard"
            value={Country}
            onChange={(e) => setCountry(e.target.value)}
          />
        </Grid>
        {/* <Grid item xs={12}>
          <FormControlLabel
            control={<Checkbox color="secondary" name="saveAddress" value="yes" />}
            label="Use this address for payment details"
          />
        </Grid> */}
      </Grid>
    </React.Fragment>
  );
}