import PropTypes from 'prop-types';
import { format } from 'date-fns';
import {
  Avatar,
  Box,
  Card,
  Checkbox,
  Collapse,
  IconButton,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TablePagination,
  TableRow,
  Typography
} from '@mui/material';
import { Scrollbar } from '../../components/scrollbar';
import { getInitials } from '../../utils/get-initials';
import {  KeyboardArrowDown, KeyboardArrowUp, Visibility } from '@mui/icons-material';
import { Fragment, useState } from 'react';

export const CustomersTable = (props) => {
  const {
    count = 0,
    items = [],
    onDeselectAll,
    onDeselectOne,
    onPageChange = () => {},
    onRowsPerPageChange,
    onSelectAll,
    onSelectOne,
    page = 0,
    rowsPerPage = 0,
    selected = []
  } = props;
  const [open, setOpen] =   useState(false);
  const selectedSome = (selected.length > 0) && (selected.length < items.length);
  const selectedAll = (items.length > 0) && (selected.length === items.length);
  const editIcon = (
    <IconButton>
      <Visibility color="primary" />
    </IconButton>
  );
  return (
    <Card>
      <Scrollbar>
        <Box sx={{ minWidth: 800 }}>
          <Table>
            <TableHead>
              <TableRow>
              <TableCell>
              <IconButton
            aria-label="expand row"
            size="small"
            onClick={() => setOpen(!open)}
          >
            {open ? <KeyboardArrowUp /> : <KeyboardArrowDown/>}
          </IconButton>
              </TableCell>
             
                <TableCell padding="checkbox">
                  <Checkbox
                    checked={selectedAll}
                    indeterminate={selectedSome}
                    onChange={(event) => {
                      if (event.target.checked) {
                        onSelectAll?.();
                      } else {
                        onDeselectAll?.();
                      }
                    }}
                  />
                </TableCell>
                <TableCell>
                  Name
                </TableCell>
                <TableCell>
                  Email
                </TableCell>
                <TableCell>
                  Location
                </TableCell>
                <TableCell>
                  Phone
                </TableCell>
                <TableCell>
                  Licsense expiry
                </TableCell> 
                <TableCell>
                  Accounts linked
                </TableCell>
                <TableCell>
                  View As
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {items.map((customer) => {
                const isSelected = selected.includes(customer.id);
              
                return (
                  <Fragment  key={customer.id} >
                  <TableRow
                    hover
                    key={customer.id}
                    selected={isSelected}
                  >
                         <TableCell>
              <IconButton
            aria-label="expand row"
            size="small"
            onClick={() => setOpen(!open)}
          >
            {open ? <KeyboardArrowUp /> : <KeyboardArrowDown/>}
          </IconButton>
              </TableCell>
             
                    <TableCell padding="checkbox">
                      <Checkbox
                        checked={isSelected}
                        onChange={(event) => {
                          if (event.target.checked) {
                            onSelectOne?.(customer.id);
                          } else {
                            onDeselectOne?.(customer.id);
                          }
                        }}
                      />
                    </TableCell>
                    <TableCell>
                      <Stack
                        alignItems="center"
                        direction="row"
                        spacing={2}
                      >
                        <Avatar src={customer.avatar}>
                          {getInitials(customer.name)}
                        </Avatar>
                        <Typography variant="subtitle2">
                          {customer.name}
                        </Typography>
                      </Stack>
                    </TableCell>
                    <TableCell>
                      {customer.email}
                    </TableCell>
                    <TableCell>
                      {customer.location}
                    </TableCell>
                    <TableCell>
                      {customer.phone}
                    </TableCell>
                    <TableCell>
                      
                    </TableCell>
                    <TableCell>
                      
                    </TableCell>
                    <TableCell>
                      {editIcon}
                    </TableCell>
                   
                 </TableRow>
                 <TableRow>
                   <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={9}>
                     <Collapse in={open} timeout="auto" unmountOnExit>
                       <Box sx={{ margin: 1 }}>
                         <Typography variant="h6" gutterBottom component="div">
                           Accounts
                         </Typography>
                         <Table size="small" aria-label="purchases">
                           <TableHead>
                             <TableRow>
                               <TableCell>ID</TableCell>
                               <TableCell>License Start date</TableCell>
                               <TableCell align="right">License Expiry Date </TableCell>
                               <TableCell align="right">License status</TableCell>
                               <TableCell align="right">Balance</TableCell>  
                               <TableCell align="right">Broker</TableCell>
                               
                               <TableCell align="right">View</TableCell>
                               
                               

                             </TableRow>
                           </TableHead>
                           <TableBody>
                             
                           </TableBody>
                         </Table>
                       </Box>
                     </Collapse>
                   </TableCell>
                   </TableRow>
                   </Fragment>
                );
              })}
            </TableBody>
          </Table>
        </Box>
      </Scrollbar>
      <TablePagination
        component="div"
        count={count}
        onPageChange={onPageChange}
        onRowsPerPageChange={onRowsPerPageChange}
        page={page}
        rowsPerPage={rowsPerPage}
        rowsPerPageOptions={[5, 10, 25]}
      />
    </Card>
  );
};

CustomersTable.propTypes = {
  count: PropTypes.number,
  items: PropTypes.array,
  onDeselectAll: PropTypes.func,
  onDeselectOne: PropTypes.func,
  onPageChange: PropTypes.func,
  onRowsPerPageChange: PropTypes.func,
  onSelectAll: PropTypes.func,
  onSelectOne: PropTypes.func,
  page: PropTypes.number,
  rowsPerPage: PropTypes.number,
  selected: PropTypes.array
};
