/**
 * API service for communicating with the backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = localStorage.getItem('access_token');
  }

  // Set authentication token
  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('access_token', token);
    } else {
      localStorage.removeItem('access_token');
    }
  }

  // Get authentication headers
  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };

    if (this.token) {
      headers.Authorization = `Bearer ${this.token}`;
    }

    return headers;
  }

  // Generic request method
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.getHeaders(),
      ...options,
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'API request failed');
      }

      return data;
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  // Authentication methods
  async login(email, password) {
    const response = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });

    if (response.success && response.data.tokens) {
      this.setToken(response.data.tokens.access_token);
    }

    return response;
  }

  async register(userData) {
    const response = await this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });

    if (response.success && response.data.tokens) {
      this.setToken(response.data.tokens.access_token);
    }

    return response;
  }

  async logout() {
    try {
      await this.request('/auth/logout', { method: 'POST' });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      this.setToken(null);
    }
  }

  async getProfile() {
    return this.request('/auth/profile');
  }

  // Financial data methods
  async getFinancialData() {
    return this.request('/financial/data');
  }

  async updateFinancialData(data) {
    return this.request('/financial/data', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getRiskProfile() {
    return this.request('/financial/risk-profile');
  }

  async updateRiskProfile(data) {
    return this.request('/financial/risk-profile', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getAssetAllocations() {
    return this.request('/financial/asset-allocations');
  }

  async updateAssetAllocation(data) {
    return this.request('/financial/asset-allocations', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getFinancialGoals() {
    return this.request('/financial/goals');
  }

  async createFinancialGoal(data) {
    return this.request('/financial/goals', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateFinancialGoal(goalId, data) {
    return this.request(`/financial/goals/${goalId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteFinancialGoal(goalId) {
    return this.request(`/financial/goals/${goalId}`, {
      method: 'DELETE',
    });
  }

  async getFinancialSummary() {
    return this.request('/financial/summary');
  }

  // Risk assessment methods
  async assessRisk() {
    return this.request('/risk/assess', { method: 'POST' });
  }

  async getRiskAssessment() {
    return this.request('/risk/assessment');
  }

  async getRiskHistory() {
    return this.request('/risk/history');
  }

  async getAssetAllocationRecommendations() {
    return this.request('/risk/recommendations/asset-allocation');
  }

  async runMonteCarloSimulation(data) {
    return this.request('/risk/simulations', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getMonteCarloSimulations() {
    return this.request('/risk/simulations');
  }

  async getMonteCarloSimulation(simulationId) {
    return this.request(`/risk/simulations/${simulationId}`);
  }

  async deleteMonteCarloSimulation(simulationId) {
    return this.request(`/risk/simulations/${simulationId}`, {
      method: 'DELETE',
    });
  }

  async getRiskDashboard() {
    return this.request('/risk/dashboard');
  }

  // Report methods
  async generateDashboardReport() {
    return this.request('/reports/dashboard', { method: 'POST' });
  }

  async generatePdfReport() {
    return this.request('/reports/pdf', { method: 'POST' });
  }

  async getReports() {
    return this.request('/reports/');
  }

  async getReport(reportId) {
    return this.request(`/reports/${reportId}`);
  }

  async downloadReport(reportId) {
    const url = `${this.baseURL}/reports/${reportId}/download`;
    const response = await fetch(url, {
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      throw new Error('Failed to download report');
    }

    return response.blob();
  }

  async deleteReport(reportId) {
    return this.request(`/reports/${reportId}`, {
      method: 'DELETE',
    });
  }

  async getAnalyticsData() {
    return this.request('/reports/analytics');
  }

  async exportData(format = 'json') {
    const url = `${this.baseURL}/reports/export?format=${format}`;
    const response = await fetch(url, {
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      throw new Error('Failed to export data');
    }

    return response.blob();
  }
}

// Create and export a singleton instance
const apiService = new ApiService();
export default apiService;

