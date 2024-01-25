import { createContext, useContext, useEffect, useReducer, useRef } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import querystring from 'querystring';
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
const HANDLERS = {
  INITIALIZE: 'INITIALIZE',
  SIGN_IN: 'SIGN_IN',
  SIGN_OUT: 'SIGN_OUT',
  SIGN_IN_ADMIN: 'SIGN_IN_ADMIN'
};

const initialState = {
  isAuthenticated: false,
  isLoading: true,
  user: null
};

const handlers = {
  [HANDLERS.INITIALIZE]: (state, action) => {
    const user = action.payload;

    return {
      ...state,
      ...(
        // if payload (user) is provided, then is authenticated
        user
          ? ({
            isAuthenticated: true,
            isLoading: false,
            user
          })
          : ({
            isLoading: false
          })
      )
    };
  },
  [HANDLERS.SIGN_IN_ADMIN]: (state, action) => {
    const user = action.payload;
      return {
        ...state,
        isAuthenticated: true,
        user
      };
  },

  [HANDLERS.SIGN_IN]: (state, action) => {
    const user = action.payload;

    return {
      ...state,
      isAuthenticated: true,
      user
    };
  },
  [HANDLERS.SIGN_OUT]: (state) => {
    return {
      ...state,
      isAuthenticated: false,
      user: null
    };
  }
};

const reducer = (state, action) => (
  handlers[action.type] ? handlers[action.type](state, action) : state
);

// The role of this context is to propagate authentication state through the App tree.

export const AuthContext = createContext();

export const AuthProvider = (props) => {
  const { children } = props;
  const [state, dispatch] = useReducer(reducer, initialState);
  const initialized = useRef(false);

  const initialize = async () => {
    // Prevent from calling twice in development mode with React.StrictMode enabled
    if (initialized.current) {
      return;
    }

    initialized.current = true;

    let isAuthenticated = false;

    try {
      isAuthenticated = window.sessionStorage.getItem('authenticated') === 'true';
    } catch (err) {
      console.error(err);
    }

    if (isAuthenticated) {
      const user = {
        id: '5e86809283e28b96d2d38537',
        avatar: '/assets/avatars/avatar-anika-visser.png',
        name: 'Anika Visser',
        email: 'anika.visser@devias.io'
      };

      dispatch({
        type: HANDLERS.INITIALIZE,
        payload: user
      });
    } else {
      dispatch({
        type: HANDLERS.INITIALIZE
      });
    }
  };

  useEffect(
    () => {
      initialize();
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    []
  );

  const skip = () => {
    try {
      window.sessionStorage.setItem('authenticated', 'true');
    } catch (err) {
      console.error(err);
    }

    const user = {
      id: '5e86809283e28b96d2d38537',
      avatar: '/assets/avatars/avatar-anika-visser.png',
      name: 'Anika Visser',
      email: 'anika.visser@devias.io'
    };

    dispatch({
      type: HANDLERS.SIGN_IN,
      payload: user
    });
    
  };
  const signInAdmin = async (email, password) => {
    try {
      const response = await axios.post(`${apiUrl}/token`, querystring.stringify({
        username: email,
        password: password
      }), {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
  
      if (response.status === 200) {
        // Login successful
        const token = response.data.access_token;
        // Store the token in local storage or in memory
        localStorage.setItem('token', token);
        window.sessionStorage.setItem('authenticated', 'true');
        console.log('Login successful');
        console.log(response.data);
      } else {
        // Handle login failure
        console.error('Login failed');
      }
    } catch (error) {
      // Handle request errors
      console.error(error);
    }
    const token = localStorage.getItem('token');
    console.log(token); // log the token to the console
    
    const admin = await axios.get(`${apiUrl}/admin`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    console.log(admin);
   const user = {
     id: '5e86809283e28b96d2d38537',
     avatar: '/assets/avatars/avatar-anika-visser.png',
     name:   response.data.name,
     email:  response.data.email
   };

   dispatch({
     type: HANDLERS.SIGN_IN_ADMIN,
     payload: admin
   });
 };

  const signIn = async (email, password) => {
     const response = await axios.get(`${apiUrl}/admin`, {
      "email": email,
      "password": password
    });
    if (response.status !== 200) {
      throw new Error('Please check your email and password');
    }

    try {
      window.sessionStorage.setItem('authenticated', 'true');
    } catch (err) {
      console.error(err);
      console.log('error');
    }

    const user = {
      id: '5e86809283e28b96d2d38537',
      avatar: '/assets/avatars/avatar-anika-visser.png',
      name:   response.data.name,
      email:  response.data.email
    };

    dispatch({
      type: HANDLERS.SIGN_IN,
      payload: user
    });
  };

  const signUpAdmin = async (email, name, password) => {
    try {
      await axios.post( `${apiUrl}/admin`, {
        "email": email,
        "password": password
      });
    } catch (error) {
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
      } else if (error.request) {
        // The request was made but no response was received
        console.log(error.request);
      } else {
        // Something happened in setting up the request that triggered an Error
        console.log('Error', error.message);
      }
      console.log(error.config);
    }
  };
  const signUp = async (email, name, password) => {
    try {
      await axios.put( `${apiUrl}/users`, {
        "name": name,
        "password": password
      });
    } catch (error) {
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
      } else if (error.request) {
        // The request was made but no response was received
        console.log(error.request);
      } else {
        // Something happened in setting up the request that triggered an Error
        console.log('Error', error.message);
      }
      console.log(error.config);
    }
  };

  const signOut = () => {
    dispatch({
      type: HANDLERS.SIGN_OUT
    });
  };

  return (
    <AuthContext.Provider
      value={{
        ...state,
        skip,
        signIn,
        signUp,
        signOut,
        signInAdmin,
        signUpAdmin
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

AuthProvider.propTypes = {
  children: PropTypes.node
};

export const AuthConsumer = AuthContext.Consumer;

export const useAuthContext = () => useContext(AuthContext);
