import "../styles/globals.css";
import type { AppProps } from "next/app";
import { ChakraProvider } from "@chakra-ui/react";
import { RtlProvider } from "../components/CaceProvider";
import { PersistGate } from "redux-persist/integration/react";

import { createStore } from "redux";
import { persistStore, persistReducer } from "redux-persist";
import storage from "redux-persist/lib/storage"; // defaults to localStorage for web

import rootReducer from "../redux/reducer";
import { Provider } from "react-redux";

const persistConfig = {
  key: "root",
  storage,
};

const persistedReducer = persistReducer(persistConfig, rootReducer);

let store = createStore(persistedReducer);
let persistor = persistStore(store);

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ChakraProvider>
      <RtlProvider>
        <Provider store={store}>
          <PersistGate loading={null} persistor={persistor}>
            <Component {...pageProps} />
          </PersistGate>
        </Provider>
      </RtlProvider>
    </ChakraProvider>
  );
}

export default MyApp;
