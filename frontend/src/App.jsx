/**
 * Main App Component with Routing
 */
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Sidebar from './components/layout/Sidebar';
import LoginForm from './components/auth/LoginForm';
import RegisterForm from './components/auth/RegisterForm';
import Dashboard from './components/dashboard/Dashboard';
import FinancialDataForm from './components/financial/FinancialDataForm';
import './App.css';

// Protected Route Component
function ProtectedRoute({ children }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  return isAuthenticated ? children : <Navigate to="/login" replace />;
}

// Public Route Component (redirect if authenticated)
function PublicRoute({ children }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  return !isAuthenticated ? children : <Navigate to="/dashboard" replace />;
}

// Main Layout Component
function MainLayout({ children }) {
  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <div className="lg:pl-64">
        <main className="p-6">
          {children}
        </main>
      </div>
    </div>
  );
}

// Placeholder components for routes not yet implemented
function RiskAssessment() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Risk Assessment</h1>
        <p className="text-muted-foreground">
          Comprehensive risk analysis and scoring
        </p>
      </div>
      <div className="flex items-center justify-center h-64 border-2 border-dashed border-muted rounded-lg">
        <p className="text-muted-foreground">Risk Assessment component coming soon...</p>
      </div>
    </div>
  );
}

function PortfolioAnalysis() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Portfolio Analysis</h1>
        <p className="text-muted-foreground">
          Asset allocation and portfolio optimization
        </p>
      </div>
      <div className="flex items-center justify-center h-64 border-2 border-dashed border-muted rounded-lg">
        <p className="text-muted-foreground">Portfolio Analysis component coming soon...</p>
      </div>
    </div>
  );
}

function MonteCarloSimulation() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Monte Carlo Simulation</h1>
        <p className="text-muted-foreground">
          Portfolio projections and scenario analysis
        </p>
      </div>
      <div className="flex items-center justify-center h-64 border-2 border-dashed border-muted rounded-lg">
        <p className="text-muted-foreground">Monte Carlo Simulation component coming soon...</p>
      </div>
    </div>
  );
}

function Goals() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Financial Goals</h1>
        <p className="text-muted-foreground">
          Set and track your financial objectives
        </p>
      </div>
      <div className="flex items-center justify-center h-64 border-2 border-dashed border-muted rounded-lg">
        <p className="text-muted-foreground">Goals component coming soon...</p>
      </div>
    </div>
  );
}

function Reports() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Reports</h1>
        <p className="text-muted-foreground">
          Generate and download comprehensive reports
        </p>
      </div>
      <div className="flex items-center justify-center h-64 border-2 border-dashed border-muted rounded-lg">
        <p className="text-muted-foreground">Reports component coming soon...</p>
      </div>
    </div>
  );
}

function Analytics() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Analytics</h1>
        <p className="text-muted-foreground">
          Advanced analytics and insights
        </p>
      </div>
      <div className="flex items-center justify-center h-64 border-2 border-dashed border-muted rounded-lg">
        <p className="text-muted-foreground">Analytics component coming soon...</p>
      </div>
    </div>
  );
}

function Settings() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Settings</h1>
        <p className="text-muted-foreground">
          Manage your account and preferences
        </p>
      </div>
      <div className="flex items-center justify-center h-64 border-2 border-dashed border-muted rounded-lg">
        <p className="text-muted-foreground">Settings component coming soon...</p>
      </div>
    </div>
  );
}

// App Routes Component
function AppRoutes() {
  return (
    <Routes>
      {/* Public Routes */}
      <Route
        path="/login"
        element={
          <PublicRoute>
            <LoginForm />
          </PublicRoute>
        }
      />
      <Route
        path="/register"
        element={
          <PublicRoute>
            <RegisterForm />
          </PublicRoute>
        }
      />

      {/* Protected Routes */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <MainLayout>
              <Dashboard />
            </MainLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/financial"
        element={
          <ProtectedRoute>
            <MainLayout>
              <FinancialDataForm />
            </MainLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/risk"
        element={
          <ProtectedRoute>
            <MainLayout>
              <RiskAssessment />
            </MainLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/portfolio"
        element={
          <ProtectedRoute>
            <MainLayout>
              <PortfolioAnalysis />
            </MainLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/simulation"
        element={
          <ProtectedRoute>
            <MainLayout>
              <MonteCarloSimulation />
            </MainLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/goals"
        element={
          <ProtectedRoute>
            <MainLayout>
              <Goals />
            </MainLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/reports"
        element={
          <ProtectedRoute>
            <MainLayout>
              <Reports />
            </MainLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/analytics"
        element={
          <ProtectedRoute>
            <MainLayout>
              <Analytics />
            </MainLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/settings"
        element={
          <ProtectedRoute>
            <MainLayout>
              <Settings />
            </MainLayout>
          </ProtectedRoute>
        }
      />

      {/* Default redirect */}
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      
      {/* 404 fallback */}
      <Route
        path="*"
        element={
          <div className="min-h-screen flex items-center justify-center">
            <div className="text-center">
              <h1 className="text-4xl font-bold text-muted-foreground">404</h1>
              <p className="text-muted-foreground">Page not found</p>
            </div>
          </div>
        }
      />
    </Routes>
  );
}

// Main App Component
function App() {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
}

export default App;

