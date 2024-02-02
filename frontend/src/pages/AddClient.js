import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Toolbar from '@mui/material/Toolbar';
import Paper from '@mui/material/Paper';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import StepLabel from '@mui/material/StepLabel';
import Button from '@mui/material/Button';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import AddressForm from '../sections/NewClient/LicesnceForm';
import PaymentForm from '../sections/NewClient/PaymentForm';
import Review from '../sections/NewClient/Review';
import axios from 'axios';

function Copyright() {
  return (
    <Typography variant="body2" color="text.secondary" align="center">
      {'Copyright © '}
      <Link color="inherit" href="#">
        Cycles Trader
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const steps = ['Client Information', 'Licesne'];



export default function AddClient() {
  const [activeStep, setActiveStep] = React.useState(0);
  const [Name, setName] = React.useState('');
  const [profileName, setProfileName] = React.useState('');
  const [Email, setEmail] = React.useState('');
  const [Phone, setPhone] = React.useState('');
  const [Address, setAddress] = React.useState('');
  const [City, setCity] = React.useState('');
  const [State1, setState1] = React.useState('');
  const [Zip, setZip] = React.useState('');
  const [Country, setCountry] = React.useState('');
  const [LicenseStart, setLicenseStart] = React.useState('');
  const [LicenseExp, setLicenseExp] = React.useState('');
  const[AccountId, setAccountId] = React.useState('');
  const[AccountName, setAccountName] = React.useState('');
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  const handleNext = () => {
    if(activeStep===0){
      if(Name==='' || profileName==='' || Email==='' || Phone==='' || Address==='' || City==='' || State1==='' || Zip==='' || Country===''){
        alert('Please fill all the fields');
        return;
      }
    }
    if(activeStep===1){
      if(LicenseStart==='' ){
        alert('Please fill License Start Date');
        return;
      }
      if(LicenseExp==='' ){
        alert('Please fill License Expiry Date');
        return;
      }
      if(AccountId==='' ){
        alert('Please fill Account ID');
        return;
      }
      if(AccountName==='' ){
        alert('Please fill Account Name');
        return;
      }
      if(LicenseStart>LicenseExp){
        alert('License Start Date should be less than License Expiry Date');
        return;
      }
      const token = localStorage.getItem('token');
      axios.post(`${apiUrl}/users`, {
        name: Name,
        profile_name: profileName,
        email: Email,
        phone: Phone,
        location: Address+','+City+','+State1+','+Zip+','+Country,
        password: "string"
      }, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        data: {
          name: Name,
          profile_name: profileName,
          email: Email,
          phone: Phone,
          location: Address+','+City+','+State1+','+Zip+','+Country,
          password: "string"
        }
      }).then((response) => {
        console.log(response);
        if (response.status === 200) {
          alert('Client Added Successfully');
        }
      }).catch((error) => {
        console.log(error);
        alert('Something went wrong');
      });
    }
     
    setActiveStep(activeStep + 1);
  };

  const handleBack = () => {
    setActiveStep(activeStep - 1);
  };
  
  return (
    <React.Fragment>
      
      <CssBaseline />
      <Container component="main" maxWidth="sm" sx={{ mb: 4 }}>
        <Paper variant="outlined" sx={{ my: { xs: 3, md: 6 }, p: { xs: 2, md: 3 } }}>
          <Typography component="h1" variant="h4" align="center">
            Add new client
          </Typography>
          <Stepper activeStep={activeStep} sx={{ pt: 3, pb: 5 }}>
            {steps.map((label) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>
          {activeStep === steps.length ? (
            <React.Fragment>
              <Typography variant="h5" gutterBottom>
                Thank you .
              </Typography>
              <Typography variant="subtitle1">
                New client has been added.
              </Typography>
            </React.Fragment>
          ) : (
            <React.Fragment>
              
             {activeStep === 0 && (<AddressForm  setName={setName}   setAddress={setAddress} setCity={setCity}  setCountry={setCountry}  setState1={setState1} setEmail={setEmail}   
             setPhone={setPhone}  setProfileName={setProfileName}  setZip={setZip} Name={Name} Address={Address} City={City} Country={Country} State1={State1}  Email={Email}  
             Phone={Phone} profileName={profileName} Zip={Zip}  />)}
              {activeStep === 1 && (<PaymentForm setAccountId={setAccountId} setLicenseExp={setLicenseExp}  setLicenseStart={setLicenseStart} setAccountName={setAccountName}  LicenseStart={LicenseStart} AccountId={AccountId}  LicenseExp={LicenseExp} AccountName={AccountName}/>)}
             
              <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                {activeStep !== 0 && (
                  <Button onClick={handleBack} sx={{ mt: 3, ml: 1 }}>
                    Back
                  </Button>
                )}

                <Button
                  variant="contained"
                  onClick={handleNext}
                  sx={{ mt: 3, ml: 1 }}
                >
                  {activeStep === steps.length - 1 ? 'Add' : 'Next'}
                </Button>
              </Box>
            </React.Fragment>
          )}
        </Paper>
        <Copyright />
      </Container>
    </React.Fragment>
  );
}