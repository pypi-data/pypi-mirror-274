import {createBrowserRouter, RouterProvider} from "react-router-dom"
import React from "react"
import Home from "./routes/Home"
import Error from "./Error"

const router = createBrowserRouter([
    {
        path: "/",
        element: <Home/>,
        errorElement: <Error/>
    }
])

function MyApp() {
    return (
        <RouterProvider router={router}/>
    );
}

export default MyApp;