import MainPage from "../features/home/pages/HomePage";
import SupportPageDLC from "../features/dlc_support/pages/SupportPageDLC";
import DBPage from "../features/db_access/pages/DBPage";
import AnalysePage from "../features/analyze_data/pages/AnalyzePage";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/dlc_support" element={<SupportPageDLC />} />
        <Route path="/db_access" element={<DBPage />} />
        <Route path="/analyze" element={<AnalysePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
