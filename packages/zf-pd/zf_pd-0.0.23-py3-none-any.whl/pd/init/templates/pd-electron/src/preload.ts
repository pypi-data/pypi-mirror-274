// See the Electron documentation for details on how to use preload scripts:
// https://www.electronjs.org/docs/latest/tutorial/process-model#preload-scripts

// See the Electron documentation for details on how to use preload scripts:
// https://www.electronjs.org/docs/latest/tutorial/process-model#preload-scripts
// In preload.js
import {contextBridge, ipcRenderer} from 'electron';


contextBridge.exposeInMainWorld('electronAPI', {
    invoke(channel: string, ...args: any[]) {
        // console.log("[preload.js] invoke: ", channel, args)
        return ipcRenderer.invoke(channel, ...args)
    },

    send(channel: string, ...args: any[]) {
        // console.log("[preload.js] send: ", channel, args)
        return ipcRenderer.send(channel, ...args)
    },

    on: (channel, func) => {
        ipcRenderer.on(channel, (event, ...args) => func(...args));
    },

    once: (channel, func) => {
        ipcRenderer.once(channel, (event, ...args) => func(...args));
    },
});