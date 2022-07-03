import React from 'react';
import { 
  BrowserRouter as Router, Route, 
  Routes, Outlet
} from 'react-router-dom';
// import './stylesheets/App.css';
import FormView from './components/FormView';
import QuestionView from './components/QuestionView';
import QuizView from './components/QuizView';
import Category from './components/Category';
import Score from './components/Score';
// material ui
import CssBaseline from '@mui/material/CssBaseline';
import useMediaQuery from '@mui/material/useMediaQuery';
import { 
  createTheme, responsiveFontSizes ,
  ThemeProvider, Container
} from '@mui/material';
// notification
import { SnackbarProvider } from 'notistack';
// comps
import MainNavBar from './components/navigation/Navbar';

// move to config file later
declare module '@mui/material/styles' {
  
  interface PaletteOptions {
    type: string;
    typography: {
      fontFamily: string;
      fontSize: number;
    };
  }
}

const LayoutOutlet = () => {

  return(
    <Container maxWidth='xl' disableGutters>
      <Container maxWidth='xl' disableGutters>
        <MainNavBar />
      </Container>
      <Container maxWidth='xl' disableGutters component={"main"}>
        <Outlet />
      </Container>
    </Container>
  );
};

const App = () => {
  // sytem preference dark mode
  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');
  // responsive theme
  const theme = React.useMemo(() => {
    return responsiveFontSizes(
      createTheme({
        palette: {
          type: prefersDarkMode ? 'dark' : 'light',
          primary: {
            light: '#bc90f9',
            main: '#8a62c6',
            dark: '#593695',
          },
          secondary: {
            light: '#ff8038',
            main: '#e2712e',
            dark: '#912000',
          },
          typography: {
            fontFamily: 'Ubuntu',
            fontSize: 14,
          },
        },
      })
    )
  }, [prefersDarkMode]);

  return (
    <>
    <CssBaseline />
    <ThemeProvider theme={theme}>
    <SnackbarProvider maxSnack={3} 
      anchorOrigin={{
        vertical: 'bottom',
        horizontal: 'center'
      }}
      iconVariant={{
        success: '✅',
        error: '✖️',
        warning: '⚠️',
        info: 'ℹ️',
      }}
    >
    <Router>
      <Routes>
        <Route path="/" element={<LayoutOutlet />}>
          <Route index element={<QuestionView />} />
          <Route path="addQuestion" element={<FormView />} />
          <Route path="addCategory" element={<Category />} />
          <Route path="play" element={<QuizView />} />
          <Route path="scores" element={<Score />} />
        </Route>
      </Routes>
    </Router>
    </SnackbarProvider>
    </ThemeProvider>
    </>
  );
};

export default App;