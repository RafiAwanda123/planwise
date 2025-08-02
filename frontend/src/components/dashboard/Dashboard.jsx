/**
 * Main Dashboard Component
 */
import { useState, useEffect } from 'react';
import {
  DollarSign,
  TrendingUp,
  TrendingDown,
  Shield,
  Target,
  AlertTriangle,
  CheckCircle,
  Clock,
  BarChart3
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import apiService from '../../lib/api';

const RISK_COLORS = {
  low: '#22c55e',
  moderate: '#f59e0b',
  high: '#ef4444'
};

const CHART_COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#8dd1e1'];

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load multiple data sources
      const [
        financialSummary,
        riskDashboard,
        analyticsData
      ] = await Promise.all([
        apiService.getFinancialSummary(),
        apiService.getRiskDashboard(),
        apiService.getAnalyticsData()
      ]);

      setDashboardData({
        financial: financialSummary.success ? financialSummary.data.financial_summary : null,
        risk: riskDashboard.success ? riskDashboard.data.dashboard : null,
        analytics: analyticsData.success ? analyticsData.data.analytics : null
      });
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAssessRisk = async () => {
    try {
      await apiService.assessRisk();
      loadDashboardData(); // Reload data after assessment
    } catch (err) {
      console.error('Risk assessment error:', err);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertTriangle className="h-4 w-4" />
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    );
  }

  const { financial, risk, analytics } = dashboardData || {};

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-muted-foreground">
            Overview of your financial risk management
          </p>
        </div>
        <Button onClick={handleAssessRisk}>
          <Shield className="mr-2 h-4 w-4" />
          Assess Risk
        </Button>
      </div>

      {/* Key Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Net Worth */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Net Worth</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${financial?.net_worth?.toLocaleString() || '0'}
            </div>
            <p className="text-xs text-muted-foreground">
              {financial?.net_worth >= 0 ? (
                <span className="text-green-600">Positive net worth</span>
              ) : (
                <span className="text-red-600">Negative net worth</span>
              )}
            </p>
          </CardContent>
        </Card>

        {/* Monthly Surplus */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Monthly Surplus</CardTitle>
            {financial?.monthly_surplus >= 0 ? (
              <TrendingUp className="h-4 w-4 text-green-600" />
            ) : (
              <TrendingDown className="h-4 w-4 text-red-600" />
            )}
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${financial?.monthly_surplus?.toLocaleString() || '0'}
            </div>
            <p className="text-xs text-muted-foreground">
              Savings rate: {((financial?.savings_rate || 0) * 100).toFixed(1)}%
            </p>
          </CardContent>
        </Card>

        {/* Risk Level */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Risk Level</CardTitle>
            <Shield className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="flex items-center space-x-2">
              <div className="text-2xl font-bold">
                {risk?.risk_assessment?.risk_level || 'N/A'}
              </div>
              {risk?.risk_assessment?.risk_level && (
                <Badge
                  variant="outline"
                  style={{
                    borderColor: RISK_COLORS[risk.risk_assessment.risk_level],
                    color: RISK_COLORS[risk.risk_assessment.risk_level]
                  }}
                >
                  {risk.risk_assessment.total_risk_score}/10
                </Badge>
              )}
            </div>
            <p className="text-xs text-muted-foreground">
              {risk?.risk_assessment?.assessment_date ? 
                `Last assessed: ${new Date(risk.risk_assessment.assessment_date).toLocaleDateString()}` :
                'No assessment yet'
              }
            </p>
          </CardContent>
        </Card>

        {/* Emergency Fund */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Emergency Fund</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {financial?.emergency_fund_months?.toFixed(1) || '0'} months
            </div>
            <Progress 
              value={Math.min((financial?.emergency_fund_months || 0) / 6 * 100, 100)} 
              className="mt-2"
            />
            <p className="text-xs text-muted-foreground mt-1">
              Target: 6 months of expenses
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Risk Breakdown Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Risk Breakdown</CardTitle>
            <CardDescription>
              Distribution of risk factors
            </CardDescription>
          </CardHeader>
          <CardContent>
            {risk?.risk_assessment?.risk_breakdown ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={Object.entries(risk.risk_assessment.risk_breakdown).map(([key, value]) => ({
                      name: key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
                      value: value.weighted_score,
                      score: value.score
                    }))}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => `${name}: ${value.toFixed(1)}`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {Object.entries(risk.risk_assessment.risk_breakdown).map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={CHART_COLORS[index % CHART_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-64 text-muted-foreground">
                No risk assessment data available
              </div>
            )}
          </CardContent>
        </Card>

        {/* Portfolio Projection */}
        <Card>
          <CardHeader>
            <CardTitle>Portfolio Projection</CardTitle>
            <CardDescription>
              Monte Carlo simulation results
            </CardDescription>
          </CardHeader>
          <CardContent>
            {risk?.latest_simulation ? (
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-muted-foreground">Expected Value</p>
                    <p className="text-lg font-semibold">
                      ${risk.latest_simulation.expected_value?.toLocaleString() || 'N/A'}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Success Probability</p>
                    <p className="text-lg font-semibold">
                      {risk.latest_simulation.success_probability?.toFixed(1) || 'N/A'}%
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Time Horizon</p>
                    <p className="text-lg font-semibold">
                      {risk.latest_simulation.time_horizon || 'N/A'} years
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Value at Risk (95%)</p>
                    <p className="text-lg font-semibold">
                      ${risk.latest_simulation.var_95?.toLocaleString() || 'N/A'}
                    </p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex items-center justify-center h-64 text-muted-foreground">
                No simulation data available
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Recommendations */}
      {risk?.recommendations && risk.recommendations.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Recommendations</CardTitle>
            <CardDescription>
              Personalized suggestions based on your risk profile
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {risk.recommendations.map((rec, index) => (
                <div key={index} className="flex items-start space-x-3 p-3 bg-muted/50 rounded-lg">
                  <CheckCircle className="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="font-medium">{rec.title}</p>
                    <p className="text-sm text-muted-foreground">{rec.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
          <CardDescription>
            Common tasks to manage your financial risk
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button variant="outline" className="h-auto p-4 flex flex-col items-center space-y-2">
              <DollarSign className="h-6 w-6" />
              <span>Update Financial Data</span>
            </Button>
            <Button variant="outline" className="h-auto p-4 flex flex-col items-center space-y-2">
              <TrendingUp className="h-6 w-6" />
              <span>Run Simulation</span>
            </Button>
            <Button variant="outline" className="h-auto p-4 flex flex-col items-center space-y-2">
              <Target className="h-6 w-6" />
              <span>Set New Goal</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

