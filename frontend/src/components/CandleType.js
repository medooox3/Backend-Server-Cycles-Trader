import * as React from 'react';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';

export default function CandleType() {
  return (
    <FormControl>
      <FormLabel id="demo-row-radio-buttons-group-label">Candle Type</FormLabel>
      <RadioGroup
        row
        aria-labelledby="demo-row-radio-buttons-group-label"
        name="row-radio-buttons-group"
      >
        <FormControlLabel value="Open" control={<Radio />} label="Open" />
        <FormControlLabel value="Close" control={<Radio />} label="Close" />
        <FormControlLabel value="Low" control={<Radio />} label="Low" />
        <FormControlLabel
          value="High"
          control={<Radio />}
          label="High"
        />
      </RadioGroup>
    </FormControl>
  );
}