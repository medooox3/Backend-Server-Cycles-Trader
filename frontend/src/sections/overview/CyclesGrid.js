import * as React from 'react';
import {
  DataGrid,
  gridPageCountSelector,
  gridPageSelector,
  useGridApiContext,
  useGridSelector,
} from '@mui/x-data-grid';
import {  randomCreatedDate,
  randomTraderName,
  randomId ,randomArrayItem} from '@mui/x-data-grid-generator';
import { styled } from '@mui/material/styles';
import Pagination from '@mui/material/Pagination';
import PaginationItem from '@mui/material/PaginationItem';


const initialRows = [
  {
    id: 1,
    symbol: "EURUSD",
    tp: 25,
    sl:100,
    tf:"M5",
    lot:0.01,
    count:5,
    candle:"close",
    auto:"True",
    open: 1.09203,
    close: 1.09533,
    
  },
  {
    id: 2,
    symbol: "EURUSD",
    tp: 25,
    sl:100,
    tf:"M5",
    lot:0.01,
    count:5,
    candle:"close",
    auto:"True",
    open: 1.09203,
    close: 1.09533,
    
  },
  {
    id: 3,
    symbol: "EURUSD",
    tp: 25,
    sl:100,
    tf:"M5",
    lot:0.01,
    count:5,
    candle:"close",
    auto:"True",
    open: 1.09203,
    close: 1.09533,
    
  },
  {
    id: 4,
    symbol: "EURUSD",
    tp: 25,
    sl:100,
    tf:"M5",
    lot:0.01,
    count:5,
    candle:"close",
    auto:"True",
    open: 1.09203,
    close: 1.09533,
    
  },
  {
    id: 5,
    symbol: "EURUSD",
    tp: 25,
    sl:100,
    tf:"M5",
    lot:0.01,
    count:5,
    candle:"close",
    auto:"True",
    open: 1.09203,
    close: 1.09533,
    
  },
  {
    id: 6,
    symbol: "EURUSD",
    tp: 25,
    sl:100,
    tf:"M5",
    lot:0.01,
    count:5,
    candle:"close",
    auto:"True",
    open: 1.09203,
    close: 1.09533,
    
  },
  {
    id: 7,
    symbol: "EURUSD",
    tp: 25,
    sl:100,
    tf:"M5",
    lot:0.01,
    count:5,
    candle:"close",
    auto:"True",
    open: 1.09203,
    close: 1.09533,
    
  },
  {
    id: 8,
    symbol: "EURUSD",
    tp: 25,
    sl:100,
    tf:"M5",
    lot:0.01,
    count:5,
    candle:"close",
    auto:"True",
    open: 1.09203,
    close: 1.09533,
  },
];

function customCheckbox(theme) {
  return {
    '& .MuiCheckbox-root svg': {
      width: 16,
      height: 16,
      backgroundColor: 'transparent',
      border: `1px solid ${
        theme.palette.mode === 'light' ? '#d9d9d9' : 'rgb(67, 67, 67)'
      }`,
      borderRadius: 2,
    },
    '& .MuiCheckbox-root svg path': {
      display: 'none',
    },
    '& .MuiCheckbox-root.Mui-checked:not(.MuiCheckbox-indeterminate) svg': {
      backgroundColor: '#1890ff',
      borderColor: '#1890ff',
    },
    '& .MuiCheckbox-root.Mui-checked .MuiIconButton-label:after': {
      position: 'absolute',
      display: 'table',
      border: '2px solid #fff',
      borderTop: 0,
      borderLeft: 0,
      transform: 'rotate(45deg) translate(-50%,-50%)',
      opacity: 1,
      transition: 'all .2s cubic-bezier(.12,.4,.29,1.46) .1s',
      content: '""',
      top: '50%',
      left: '39%',
      width: 5.71428571,
      height: 9.14285714,
    },
    '& .MuiCheckbox-root.MuiCheckbox-indeterminate .MuiIconButton-label:after': {
      width: 8,
      height: 8,
      backgroundColor: '#1890ff',
      transform: 'none',
      top: '39%',
      border: 0,
    },
  };
}

const StyledDataGrid = styled(DataGrid)(({ theme }) => ({
  border: 0,
  color:
    theme.palette.mode === 'light' ? 'rgba(0,0,0,.85)' : 'rgba(255,255,255,0.85)',
  fontFamily: [
    '-apple-system',
    'BlinkMacSystemFont',
    '"Segoe UI"',
    'Roboto',
    '"Helvetica Neue"',
    'Arial',
    'sans-serif',
    '"Apple Color Emoji"',
    '"Segoe UI Emoji"',
    '"Segoe UI Symbol"',
  ].join(','),
  WebkitFontSmoothing: 'auto',
  letterSpacing: 'normal',
  '& .MuiDataGrid-columnsContainer': {
    backgroundColor: theme.palette.mode === 'light' ? '#fafafa' : '#1d1d1d',
  },
  '& .MuiDataGrid-iconSeparator': {
    display: 'none',
  },
  '& .MuiDataGrid-columnHeader, .MuiDataGrid-cell': {
    borderRight: `1px solid ${
      theme.palette.mode === 'light' ? '#f0f0f0' : '#303030'
    }`,
  },
  '& .MuiDataGrid-columnsContainer, .MuiDataGrid-cell': {
    borderBottom: `1px solid ${
      theme.palette.mode === 'light' ? '#f0f0f0' : '#303030'
    }`,
  },
  '& .MuiDataGrid-cell': {
    color:
      theme.palette.mode === 'light' ? 'rgba(0,0,0,.85)' : 'rgba(255,255,255,0.65)',
  },
  '& .MuiPaginationItem-root': {
    borderRadius: 0,
  },
  ...customCheckbox(theme),
}));


function CustomPagination() {
  const apiRef = useGridApiContext();
  const page = useGridSelector(apiRef, gridPageSelector);
  const pageCount = useGridSelector(apiRef, gridPageCountSelector);

  return (
    <Pagination
      color="primary"
      variant="outlined"
      shape="rounded"
      page={page + 1}
      count={pageCount}
      // @ts-expect-error
      renderItem={(props2) => <PaginationItem {...props2} disableRipple />}
      onChange={(event, value) => apiRef.current.setPage(value - 1)}
    />
  );
}

const PAGE_SIZE = 10;

export default function Cycles() {
  const [rows, setRows] = React.useState(initialRows);

  const columns = [
    { field: 'id', headerName: 'Cycle',type:'number', width: 70, editable: false,headerAlign: 'left',align: 'left' },
    { field: 'symbol', headerName: 'Symbol', width: 120, editable: false ,headerAlign: 'left',align: 'left'},
    { field: 'tp', headerName: 'TP', width: 70, editable: true ,type:'number',headerAlign: 'left',align: 'left'},
    { field: 'sl', headerName: 'SL', width: 70, editable: true ,type:'number',headerAlign: 'left',align: 'left'},
    { field: 'tf', headerName: 'TF', width: 70, editable: true , type: 'singleSelect', valueOptions: ['M1', 'M5', 'M15','M30','H1','H4','D1','W1','MN'],headerAlign: 'left',align: 'left'},
    { field: 'lot', headerName: 'Lot', width: 70, editable: true ,type:'number',headerAlign: 'left',align: 'left'},
    { field: 'count', headerName: 'Count', width: 70, editable: true ,type:'number',headerAlign: 'left',align: 'left'},
    { field: 'candle', headerName: 'Candle', width: 70, editable: true ,type:'number',headerAlign: 'left',align: 'left'},
    { field: 'auto', headerName: 'Auto',width: 120, editable: true ,type:'number',headerAlign: 'left',align: 'left'},
    { field: 'open', headerName: 'Open', width: 120, editable: true ,type:'number',headerAlign: 'left',align: 'left'},
    { field: 'close', headerName: 'Close',width: 120, editable: true ,type:'number',headerAlign: 'left',align: 'left'},

  ];
  const [paginationModel, setPaginationModel] = React.useState({
    pageSize: PAGE_SIZE,
    page: 0,
  });

  return (
    <div style={{ height: 400, width: '100%' }}>
      <StyledDataGrid
        autoHeight
        columns={columns}
        rows={rows}
        checkboxSelection
        paginationModel={paginationModel}
        onPaginationModelChange={setPaginationModel}
        pageSizeOptions={[PAGE_SIZE]}
        slots={{
          pagination: CustomPagination,
        }}
       
      />
    </div>
  );
}