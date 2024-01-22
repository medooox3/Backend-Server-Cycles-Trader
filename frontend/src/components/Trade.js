import * as React from 'react';
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import { green, lightBlue, purple, red } from '@mui/material/colors';
import { Card, CardContent, CardHeader, TextField } from '@mui/material';
import SymbolsList from './SymbolsList';
import CandleType from './CandleType';


const BuyButton = styled(Button)(({ theme }) => ({
  color: theme.palette.getContrastText(red[500]),
  backgroundColor: green[500],
  '&:hover': {
    backgroundColor: green[700],
  },
}));

const SellButton = styled(Button)(({ theme }) => ({
  color: theme.palette.getContrastText(red[500]),
  backgroundColor: red[500],
  '&:hover': {
    backgroundColor: red[700],
  },
}));
const BuySellButton = styled(Button)(({ theme }) => ({
  color: theme.palette.getContrastText(red[500]),

}));


export default function TradePanel() {
  return (

    <Stack spacing={2} direction="row">

      <Stack spacing={2} direction="column">
        <Stack spacing={2} direction="row">
          <BuyButton variant="contained" color="info">
            Buy
          </BuyButton>
          <SellButton variant="contained" color="info">
            Sell
          </SellButton>
          <BuySellButton variant="contained" color="warning">
            Buy  && Sell
          </BuySellButton>
          <BuySellButton variant="contained" color="secondary">
            Close All
          </BuySellButton>
        </Stack>
        <Card sx={{ minWidth: 275 }}>
          <CardHeader
            subheader="The information can be edited"
            title="Main Parameters"
          />
          <CardContent sx={{ pt: 0 }}>
            <Stack spacing={2} direction="row">
              <TextField
                label="Lot"

                color="warning"
                size='small'
                value={0.01}
              />
              <TextField label="Drawdown" color="secondary" size='small' value={100} />
            </Stack>
            <Stack spacing={2} mt={2} direction="row">
              <TextField label="Sl" color="success" size='small' value={100} />
              <TextField label="Tp" color="success" size='small' value={100} />
            </Stack>
            < Stack spacing={2} mt={2} direction="row">
              <CandleType />
            </Stack>
          </CardContent>
        </Card>
      </Stack>

      <Stack spacing={2} direction="column">
        <Stack spacing={2} direction="row">
          <SymbolsList />
        </Stack>
      </Stack>
    </Stack >


  );
}
