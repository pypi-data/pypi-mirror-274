import type {ForgeConfig} from '@electron-forge/shared-types';
import {MakerDMG} from '@electron-forge/maker-dmg';
import {AutoUnpackNativesPlugin} from '@electron-forge/plugin-auto-unpack-natives';
import {WebpackPlugin} from '@electron-forge/plugin-webpack';
import path from 'path';

import {mainConfig, rendererConfig} from './webpack';

const config: ForgeConfig = {
  packagerConfig: {
    asar: true,
    icon: path.join(process.cwd(), "assets", "icon.icns"),
    extraResource: [
      path.join(process.cwd(), "assets", "icon.icns"),
      path.join(process.cwd(), "assets", "icon.png"),
    ],
  },
  rebuildConfig: {},
  makers: [
    new MakerDMG({
      icon: path.join(process.cwd(), "assets", "icon.icns"),
      format: "ULFO",
    }),
  ],
  plugins: [
    new AutoUnpackNativesPlugin({}),
    new WebpackPlugin({
      mainConfig,
      renderer: {
        config: rendererConfig,
        entryPoints: [
          {
            html: './src/index.html',
            js: './src/renderer.tsx',
            name: 'main_window',
            preload: {
              js: './src/preload.ts',
            },
          },
        ],
      },
    }),
  ],
};

export default config;
