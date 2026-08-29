import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import InterviewRoom from './pages/InterviewRoom';
import ResultsReport from './pages/ResultsReport';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="/login" element={<Login />} />
          <Route path="/interview" element={<InterviewRoom />} />
          <Route path="/results" element={<ResultsReport />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/interview" element={<InterviewRoom />} />
              <Route path="/results" element={<Results />} />
            </Route >
          </Route >
        </Routes >
      </BrowserRouter >
    </AuthProvider >
  );
}

export default App;
