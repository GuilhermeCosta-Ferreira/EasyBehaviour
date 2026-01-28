import MainPage from "../features/home/pages/HomePage";
import SupportPageDLC from "../features/dlc_support/pages/SupportPageDLC";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/dlc_support" element={<SupportPageDLC />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
