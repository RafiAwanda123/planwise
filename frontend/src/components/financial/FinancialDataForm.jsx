/**
 * Financial Data Form Component
 */
import { useState, useEffect } from 'react';
import { Save, DollarSign, TrendingUp, Shield, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import apiService from '../../lib/api';

export default function FinancialDataForm() {
  const [financialData, setFinancialData] = useState({
    monthly_income: '',
    monthly_expenses: '',
    total_assets: '',
    total_debt: '',
    emergency_fund: '',
    insurance_coverage: ''
  });

  const [riskProfile, setRiskProfile] = useState({
    risk_tolerance: '',
    investment_experience: '',
    time_horizon: '',
    age: '',
    employment_status: ''
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [financialResponse, riskResponse] = await Promise.all([
        apiService.getFinancialData(),
        apiService.getRiskProfile()
      ]);

      if (financialResponse.success && financialResponse.data.financial_data) {
        const data = financialResponse.data.financial_data;
        setFinancialData({
          monthly_income: data.monthly_income || '',
          monthly_expenses: data.monthly_expenses || '',
          total_assets: data.total_assets || '',
          total_debt: data.total_debt || '',
          emergency_fund: data.emergency_fund || '',
          insurance_coverage: data.insurance_coverage || ''
        });
      }

      if (riskResponse.success && riskResponse.data.risk_profile) {
        const data = riskResponse.data.risk_profile;
        setRiskProfile({
          risk_tolerance: data.risk_tolerance || '',
          investment_experience: data.investment_experience || '',
          time_horizon: data.time_horizon || '',
          age: data.age || '',
          employment_status: data.employment_status || ''
        });
      }
    } catch (err) {
      setError('Failed to load financial data');
      console.error('Load error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFinancialDataChange = (field, value) => {
    setFinancialData(prev => ({
      ...prev,
      [field]: value
    }));
    clearMessages();
  };

  const handleRiskProfileChange = (field, value) => {
    setRiskProfile(prev => ({
      ...prev,
      [field]: value
    }));
    clearMessages();
  };

  const clearMessages = () => {
    setError(null);
    setSuccess(null);
  };

  const saveFinancialData = async () => {
    try {
      setSaving(true);
      clearMessages();

      // Convert string values to numbers
      const dataToSave = {
        monthly_income: parseFloat(financialData.monthly_income) || 0,
        monthly_expenses: parseFloat(financialData.monthly_expenses) || 0,
        total_assets: parseFloat(financialData.total_assets) || 0,
        total_debt: parseFloat(financialData.total_debt) || 0,
        emergency_fund: parseFloat(financialData.emergency_fund) || 0,
        insurance_coverage: parseFloat(financialData.insurance_coverage) || 0
      };

      const response = await apiService.updateFinancialData(dataToSave);
      
      if (response.success) {
        setSuccess('Financial data saved successfully');
      } else {
        setError(response.message || 'Failed to save financial data');
      }
    } catch (err) {
      setError('Failed to save financial data');
      console.error('Save error:', err);
    } finally {
      setSaving(false);
    }
  };

  const saveRiskProfile = async () => {
    try {
      setSaving(true);
      clearMessages();

      const dataToSave = {
        ...riskProfile,
        time_horizon: riskProfile.time_horizon ? parseInt(riskProfile.time_horizon) : null,
        age: riskProfile.age ? parseInt(riskProfile.age) : null
      };

      const response = await apiService.updateRiskProfile(dataToSave);
      
      if (response.success) {
        setSuccess('Risk profile saved successfully');
      } else {
        setError(response.message || 'Failed to save risk profile');
      }
    } catch (err) {
      setError('Failed to save risk profile');
      console.error('Save error:', err);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Financial Data</h1>
        <p className="text-muted-foreground">
          Manage your financial information and risk profile
        </p>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {success && (
        <Alert>
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{success}</AlertDescription>
        </Alert>
      )}

      <Tabs defaultValue="financial" className="space-y-6">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="financial">Financial Data</TabsTrigger>
          <TabsTrigger value="risk">Risk Profile</TabsTrigger>
        </TabsList>

        <TabsContent value="financial" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Income & Expenses */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <DollarSign className="h-5 w-5" />
                  <span>Income & Expenses</span>
                </CardTitle>
                <CardDescription>
                  Your monthly cash flow information
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="monthly_income">Monthly Income</Label>
                  <Input
                    id="monthly_income"
                    type="number"
                    placeholder="5000"
                    value={financialData.monthly_income}
                    onChange={(e) => handleFinancialDataChange('monthly_income', e.target.value)}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="monthly_expenses">Monthly Expenses</Label>
                  <Input
                    id="monthly_expenses"
                    type="number"
                    placeholder="3500"
                    value={financialData.monthly_expenses}
                    onChange={(e) => handleFinancialDataChange('monthly_expenses', e.target.value)}
                  />
                </div>
                {financialData.monthly_income && financialData.monthly_expenses && (
                  <div className="p-3 bg-muted rounded-lg">
                    <p className="text-sm font-medium">Monthly Surplus</p>
                    <p className={`text-lg font-bold ${
                      (financialData.monthly_income - financialData.monthly_expenses) >= 0 
                        ? 'text-green-600' 
                        : 'text-red-600'
                    }`}>
                      ${(financialData.monthly_income - financialData.monthly_expenses).toLocaleString()}
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Assets & Debt */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <TrendingUp className="h-5 w-5" />
                  <span>Assets & Debt</span>
                </CardTitle>
                <CardDescription>
                  Your total assets and liabilities
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="total_assets">Total Assets</Label>
                  <Input
                    id="total_assets"
                    type="number"
                    placeholder="100000"
                    value={financialData.total_assets}
                    onChange={(e) => handleFinancialDataChange('total_assets', e.target.value)}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="total_debt">Total Debt</Label>
                  <Input
                    id="total_debt"
                    type="number"
                    placeholder="25000"
                    value={financialData.total_debt}
                    onChange={(e) => handleFinancialDataChange('total_debt', e.target.value)}
                  />
                </div>
                {financialData.total_assets && financialData.total_debt && (
                  <div className="p-3 bg-muted rounded-lg">
                    <p className="text-sm font-medium">Net Worth</p>
                    <p className={`text-lg font-bold ${
                      (financialData.total_assets - financialData.total_debt) >= 0 
                        ? 'text-green-600' 
                        : 'text-red-600'
                    }`}>
                      ${(financialData.total_assets - financialData.total_debt).toLocaleString()}
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Emergency Fund & Insurance */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Shield className="h-5 w-5" />
                  <span>Emergency Fund & Insurance</span>
                </CardTitle>
                <CardDescription>
                  Your financial safety net
                </CardDescription>
              </CardHeader>
              <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="emergency_fund">Emergency Fund</Label>
                  <Input
                    id="emergency_fund"
                    type="number"
                    placeholder="15000"
                    value={financialData.emergency_fund}
                    onChange={(e) => handleFinancialDataChange('emergency_fund', e.target.value)}
                  />
                  {financialData.emergency_fund && financialData.monthly_expenses && (
                    <p className="text-sm text-muted-foreground">
                      Covers {(financialData.emergency_fund / financialData.monthly_expenses).toFixed(1)} months of expenses
                    </p>
                  )}
                </div>
                <div className="space-y-2">
                  <Label htmlFor="insurance_coverage">Insurance Coverage</Label>
                  <Input
                    id="insurance_coverage"
                    type="number"
                    placeholder="500000"
                    value={financialData.insurance_coverage}
                    onChange={(e) => handleFinancialDataChange('insurance_coverage', e.target.value)}
                  />
                  <p className="text-sm text-muted-foreground">
                    Total life and disability insurance coverage
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="flex justify-end">
            <Button onClick={saveFinancialData} disabled={saving}>
              {saving ? (
                <div className="flex items-center space-x-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Saving...</span>
                </div>
              ) : (
                <>
                  <Save className="mr-2 h-4 w-4" />
                  Save Financial Data
                </>
              )}
            </Button>
          </div>
        </TabsContent>

        <TabsContent value="risk" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Risk Profile</CardTitle>
              <CardDescription>
                Help us understand your risk tolerance and investment experience
              </CardDescription>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="risk_tolerance">Risk Tolerance</Label>
                <Select
                  value={riskProfile.risk_tolerance}
                  onValueChange={(value) => handleRiskProfileChange('risk_tolerance', value)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select risk tolerance" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="conservative">Conservative</SelectItem>
                    <SelectItem value="moderate">Moderate</SelectItem>
                    <SelectItem value="aggressive">Aggressive</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="investment_experience">Investment Experience</Label>
                <Select
                  value={riskProfile.investment_experience}
                  onValueChange={(value) => handleRiskProfileChange('investment_experience', value)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select experience level" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="beginner">Beginner</SelectItem>
                    <SelectItem value="intermediate">Intermediate</SelectItem>
                    <SelectItem value="advanced">Advanced</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="time_horizon">Investment Time Horizon (years)</Label>
                <Input
                  id="time_horizon"
                  type="number"
                  placeholder="10"
                  value={riskProfile.time_horizon}
                  onChange={(e) => handleRiskProfileChange('time_horizon', e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="age">Age</Label>
                <Input
                  id="age"
                  type="number"
                  placeholder="35"
                  value={riskProfile.age}
                  onChange={(e) => handleRiskProfileChange('age', e.target.value)}
                />
              </div>

              <div className="space-y-2 md:col-span-2">
                <Label htmlFor="employment_status">Employment Status</Label>
                <Input
                  id="employment_status"
                  type="text"
                  placeholder="Full-time employed"
                  value={riskProfile.employment_status}
                  onChange={(e) => handleRiskProfileChange('employment_status', e.target.value)}
                />
              </div>
            </CardContent>
          </Card>

          <div className="flex justify-end">
            <Button onClick={saveRiskProfile} disabled={saving}>
              {saving ? (
                <div className="flex items-center space-x-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Saving...</span>
                </div>
              ) : (
                <>
                  <Save className="mr-2 h-4 w-4" />
                  Save Risk Profile
                </>
              )}
            </Button>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}

