import Head from 'next/head';
import { Box, Container, Unstable_Grid2 as Grid, Tab, Tabs } from '@mui/material';
import { Layout as DashboardLayout } from '../layouts/dashboard/layout';
import { OverviewBudget } from '../sections/overview/overview-budget';
import { OverviewTasksProgress } from '../sections/overview/overview-tasks-progress';
import { OverviewTotalCustomers } from '../sections/overview/overview-total-customers';
import { OverviewTotalProfit } from '../sections/overview/overview-total-profit';
import Cycles from '../sections/overview/CyclesGrid';
import { useCallback, useState } from 'react';
import TradePanel from '../components/Trade';
import Orders from '../sections/overview/OrdersGrid';
const now = new Date();

const Page = () => {
  const [method, setMethod] = useState('cycles');

  const handleMethodChange = useCallback(
    (event, value) => {
      setMethod(value);
    },
    []
  );

  return (
  <>
    <Head>
      <title>
        Overview | Cycles Trader
      </title>
    </Head>
    <Box
      component="main"
      sx={{
        flexGrow: 1,
        py: 8
      }}
    >
      <Container maxWidth="xl">
        <Grid
          container
          spacing={3}
        >
          <Grid
            xs={12}
            sm={6}
            lg={3}
          >
            <OverviewBudget
              difference={12}
              positive
              sx={{ height: '100%' }}
              value="$24k"
            />
          </Grid>
          <Grid
            xs={12}
            sm={6}
            lg={3}
          >
            <OverviewTotalCustomers
              difference={16}
              positive={false}
              sx={{ height: '100%' }}
              value="1.6k"
            />
          </Grid>
          <Grid
            xs={12}
            sm={6}
            lg={3}
          >
            <OverviewTasksProgress
              sx={{ height: '100%' }}
              value={75.5}
            />
          </Grid>
          <Grid
            xs={12}
            sm={6}
            lg={3}
          >
            <OverviewTotalProfit
              sx={{ height: '100%' }}
              value="$15k"
            />
          </Grid>

         <Grid
            xs={12}
            lg={12}
          >
            <Tabs
              onChange={handleMethodChange}
              scrollButtons="auto"
              value={method}
              variant="scrollable"
            >
               <Tab
                label="Trade"
                value="trade"
              />
              <Tab
                label="Cycles"
                value="cycles"
              />
              <Tab
                label="Orders"
                value="orders"
              />
            </Tabs>
          </Grid>
          <Grid
            xs={12}
            lg={12}
          >
           {method === 'cycles' && <Cycles/>} 
          {method === 'orders' && <Orders/>}
          {method === 'trade' && <TradePanel/>}
          </Grid>

        </Grid>
      </Container>
    </Box>
  </>
);}

Page.getLayout = (page) => (
  <DashboardLayout>
    {page}
  </DashboardLayout>
);

export default Page;
