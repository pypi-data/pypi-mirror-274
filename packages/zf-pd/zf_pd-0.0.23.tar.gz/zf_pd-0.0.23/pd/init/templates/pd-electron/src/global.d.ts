declare global {
    interface Window {
        electronAPI: {
            invoke: (channel: string, data: any) => Promise<any>;
            send: (channel: string, data: any) => void;

            on: (channel, func) => void;
            once: (channel, func) => void;
        }
    }
}

export {};