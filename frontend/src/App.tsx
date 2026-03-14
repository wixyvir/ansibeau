import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LogPage from './pages/LogPage';
import SubmitPage from './pages/SubmitPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/log/:logId" element={<LogPage />} />
        <Route path="/submit" element={<SubmitPage />} />
        <Route path="/" element={<Navigate to="/submit" replace />} />
        <Route path="*" element={<Navigate to="/submit" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
