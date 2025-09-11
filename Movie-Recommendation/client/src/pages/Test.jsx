import React from 'react';
import { useAuth } from '../contexts/AuthContext';

const Test = () => {
  const { user, isAuthenticated, loading } = useAuth();
  
  console.log('Test page - user:', user, 'isAuthenticated:', isAuthenticated, 'loading:', loading);
  
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white rounded-lg shadow-md p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">Test Page</h1>
        <div className="space-y-2">
          <p><strong>Loading:</strong> {loading ? 'Yes' : 'No'}</p>
          <p><strong>Authenticated:</strong> {isAuthenticated ? 'Yes' : 'No'}</p>
          <p><strong>User:</strong> {user ? JSON.stringify(user) : 'None'}</p>
          <p><strong>Token:</strong> {localStorage.getItem('token') ? 'Present' : 'Missing'}</p>
        </div>
      </div>
    </div>
  );
};

export default Test;
