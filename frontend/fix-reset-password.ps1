$resetContent = @'
import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';
import { authHelpers } from '@/lib/supabase';

const ResetPassword = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState('request'); // 'request' or 'reset'
  const [resetSent, setResetSent] = useState(false);
  
  // For requesting reset
  const [email, setEmail] = useState('');
  
  // For resetting password
  const [passwords, setPasswords] = useState({
    password: '',
    confirmPassword: '',
  });

  useEffect(() => {
    // Check if this is a password reset callback (has access_token in URL)
    const checkResetToken = async () => {
      const accessToken = searchParams.get('access_token');
      const type = searchParams.get('type');
      
      if (accessToken && type === 'recovery') {
        // User arrived via email reset link
        setMode('reset');
      } else {
        // User clicked "Reset it here" - show email request form
        setMode('request');
      }
    };
    checkResetToken();
  }, [searchParams]);

  const handleRequestReset = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Check if email is authorized
      const { isAuthorized } = await authHelpers.isEmailAuthorized(email);
      
      if (!isAuthorized) {
        toast.error('This email is not registered in our system.');
        setLoading(false);
        return;
      }

      // Send password reset email
      const { error } = await authHelpers.resetPassword(email);

      if (error) {
        toast.error(error.message || 'Failed to send reset email. Please try again.');
        return;
      }

      setResetSent(true);
      toast.success('Password reset email sent! Check your inbox.');
    } catch (error) {
      console.error('Reset password error:', error);
      toast.error('An unexpected error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleResetPassword = async (e) => {
    e.preventDefault();

    // Validation
    if (passwords.password.length < 6) {
      toast.error('Password must be at least 6 characters long');
      return;
    }

    if (passwords.password !== passwords.confirmPassword) {
      toast.error('Passwords do not match');
      return;
    }

    setLoading(true);

    try {
      const { error } = await authHelpers.updatePassword(passwords.password);

      if (error) {
        toast.error(error.message || 'Failed to update password');
        return;
      }

      toast.success('Password updated successfully! Redirecting to login...');
      
      // Sign out and redirect to login
      await authHelpers.signOut();
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (error) {
      console.error('Update password error:', error);
      toast.error('An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2 gold-gradient">SNR AUTOMATIONS</h1>
          <p className="text-gray-400">Team Dashboard</p>
        </div>

        {mode === 'request' ? (
          // Email Request Form
          <Card className="glass-effect border-[rgba(255,215,0,0.2)]">
            <CardHeader>
              <CardTitle className="text-2xl text-white">Reset Password</CardTitle>
              <CardDescription className="text-gray-400">
                {resetSent 
                  ? 'Check your email for the reset link'
                  : 'Enter your authorized email to receive a reset link'
                }
              </CardDescription>
            </CardHeader>
            <CardContent>
              {resetSent ? (
                <div className="space-y-4">
                  <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-4 text-center">
                    <p className="text-green-400 text-sm">
                      ✅ Password reset email sent successfully!
                    </p>
                    <p className="text-gray-400 text-xs mt-2">
                      Check your inbox and click the link to reset your password.
                      <br />
                      The link will expire in 1 hour.
                    </p>
                  </div>
                  <Button
                    onClick={() => navigate('/login')}
                    className="w-full btn-primary"
                  >
                    Back to Login
                  </Button>
                </div>
              ) : (
                <form onSubmit={handleRequestReset} className="space-y-4">
                  <div>
                    <Label className="text-gray-300 text-sm mb-1 block">Email Address</Label>
                    <Input
                      type="email"
                      placeholder="your.email@snr.com"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                      className="bg-[rgba(255,255,255,0.05)] border-[rgba(255,215,0,0.2)] text-white placeholder:text-gray-500"
                    />
                  </div>
                  <Button
                    type="submit"
                    className="w-full btn-primary"
                    disabled={loading}
                  >
                    {loading ? 'Sending...' : 'Send Reset Email'}
                  </Button>
                  <p className="text-center text-gray-500 text-sm mt-4">
                    Remember your password?{' '}
                    <a
                      href="/login"
                      className="text-[#FFD700] hover:underline font-medium"
                    >
                      Sign in here
                    </a>
                  </p>
                </form>
              )}
            </CardContent>
          </Card>
        ) : (
          // Password Reset Form (from email link)
          <Card className="glass-effect border-[rgba(255,215,0,0.2)]">
            <CardHeader>
              <CardTitle className="text-2xl text-white">Set New Password</CardTitle>
              <CardDescription className="text-gray-400">
                Enter your new password below
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleResetPassword} className="space-y-4">
                <div>
                  <Label className="text-gray-300 text-sm mb-1 block">New Password</Label>
                  <Input
                    type="password"
                    placeholder="Min. 6 characters"
                    value={passwords.password}
                    onChange={(e) => setPasswords({ ...passwords, password: e.target.value })}
                    required
                    minLength={6}
                    className="bg-[rgba(255,255,255,0.05)] border-[rgba(255,215,0,0.2)] text-white placeholder:text-gray-500"
                  />
                </div>
                <div>
                  <Label className="text-gray-300 text-sm mb-1 block">Confirm New Password</Label>
                  <Input
                    type="password"
                    placeholder="Re-enter password"
                    value={passwords.confirmPassword}
                    onChange={(e) => setPasswords({ ...passwords, confirmPassword: e.target.value })}
                    required
                    minLength={6}
                    className="bg-[rgba(255,255,255,0.05)] border-[rgba(255,215,0,0.2)] text-white placeholder:text-gray-500"
                  />
                </div>
                <Button
                  type="submit"
                  className="w-full btn-primary"
                  disabled={loading}
                >
                  {loading ? 'Updating Password...' : 'Update Password'}
                </Button>
              </form>
            </CardContent>
          </Card>
        )}

        <div className="mt-6 text-center">
          <p className="text-gray-500 text-sm">
            🔒 Secure authentication for authorized team members only
          </p>
          <p className="text-gray-600 text-xs mt-2">
            Need access? Contact your administrator
          </p>
        </div>
      </div>
    </div>
  );
};

export default ResetPassword;
'@

Set-Content -Path "src\pages\ResetPassword.jsx" -Value $resetContent -Encoding UTF8
Write-Host "ResetPassword.jsx has been updated successfully!" -ForegroundColor Green
Write-Host "Now handles both: requesting reset email AND resetting password from email link" -ForegroundColor Cyan
