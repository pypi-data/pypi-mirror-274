import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import MyApp from './App';
import {ChakraProvider, extendTheme} from "@chakra-ui/react";
import reportWebVitals from './reportWebVitals';

const theme = extendTheme({
    colors: {
        brand: {
            100: "#2D3748",
            101: "#4299E1",
            801: "#ffe86e",
        },
    },
    fonts: {
        body: `'RosaritoRegular', sans-serif`,
    },
});

const root = ReactDOM.createRoot(
    document.getElementById('root') as HTMLElement
);


root.render(
    <React.StrictMode>
        <ChakraProvider theme={theme}>
            <MyApp/>
        </ChakraProvider>
    </React.StrictMode>
);

reportWebVitals(console.log);