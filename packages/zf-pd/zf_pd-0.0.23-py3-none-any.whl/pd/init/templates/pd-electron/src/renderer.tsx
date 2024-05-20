import './index.css';
import React from 'react';
import ReactDOM from 'react-dom/client';
import MyApp from './App'; // Adjust the path if necessary
import {ChakraProvider} from "@chakra-ui/react";

console.log('👋 This message is being logged by "renderer.js", included via webpack');

const root = ReactDOM.createRoot(
    document.getElementById('root') as HTMLElement
);

root.render(
    <React.StrictMode>
        <ChakraProvider>
            <MyApp/>
    </ChakraProvider>
    </React.StrictMode>
);