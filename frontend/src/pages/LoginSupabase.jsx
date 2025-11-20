import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';
import { authHelpers } from '@/lib/supabase';

const LoginSupabase = ({ onLogin }) => {
  const [loading, setLoading] = useState(false);
  const [loginData, setLoginData] = useState({
    email: '',
    password: '',
  });

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Sign in with Supabase (authorization check is inside signIn function)
      const { data, error } = await authHelpers.signIn(loginData.email, loginData.password);

      if (error) {
        if (error.message.includes('not authorized')) {
          toast.error('This email is not authorized to access the system. Contact your administrator.');
        } else if (error.message.includes('Invalid login credentials')) {
          toast.error('Invalid email or password. Please check your credentials or use "Forgot Password?"');
        } else if (error.message.includes('Email not confirmed')) {
          toast.error('Please verify your email before logging in. Check your inbox.');
        } else {
          toast.error(error.message || 'Login failed. Please try again.');
        }
        return;
      }

      // Get user profile
      const { data: profile, error: profileError } = await authHelpers.getUserProfile(data.user.id);

      if (profileError || !profile) {
        toast.error('Unable to load user profile. Please contact support.');
        return;
      }

      // Pass user data to parent component
      onLogin({
        id: profile.id,
        email: profile.email,
        name: profile.name,
        role: profile.role,
        contact: profile.contact,
        skillset: profile.skillset || [],
        current_tasks: profile.current_tasks || [],
      });

      toast.success(`Welcome back, ${profile.name}!`);
    } catch (error) {
      console.error('Login error:', error);
      toast.error('An unexpected error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleLoginChange = (field, value) => {
    setLoginData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="relative w-32 h-32 mx-auto mb-4">
            <img 
              src="https://customer-assets.emergentagent.com/job_25d84bc8-5cd6-4672-913d-7856f1b8c2dc/artifacts/7ukgfyx7_snr%20logo%20png.jpg"
              alt="SNR Automations"
              className="w-32 h-32 rounded-full border-4 border-[#FFD700] object-cover logo-glow"
            />
          </div>
          <h1 className="text-4xl font-bold mb-2 gold-gradient">SNR AUTOMATIONS</h1>
          <p className="text-gray-400">Team Dashboard</p>
        </div>

        <Card className="glass-effect border-[rgba(255,215,0,0.2)]" data-testid="login-card">
          <CardHeader>
            <CardTitle className="text-2xl text-white">Welcome Back</CardTitle>
            <CardDescription className="text-gray-400">
              Sign in with your authorized email
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <Label className="text-gray-300 text-sm mb-1 block">Email Address</Label>
                <Input
                  type="email"
                  placeholder="your.email@gmail.com"
                  value={loginData.email}
                  onChange={(e) => handleLoginChange('email', e.target.value)}
                  required
                  className="bg-[rgba(255,255,255,0.05)] border-[rgba(255,215,0,0.2)] text-white placeholder:text-gray-500"
                  data-testid="email-input"
                />
              </div>
              <div>
                <Label className="text-gray-300 text-sm mb-1 block">Password</Label>
                <Input
                  type="password"
                  placeholder="Enter your password"
                  value={loginData.password}
                  onChange={(e) => handleLoginChange('password', e.target.value)}
                  required
                  className="bg-[rgba(255,255,255,0.05)] border-[rgba(255,215,0,0.2)] text-white placeholder:text-gray-500"
                  data-testid="password-input"
                />
              </div>
              <Button
                type="submit"
                className="w-full btn-primary"
                disabled={loading}
                data-testid="login-button"
              >
                {loading ? 'Signing in...' : 'Sign In'}
              </Button>
              <p className="text-center text-gray-500 text-sm mt-4">
                Forgot your password?{' '}
                <a
                  href="/reset-password"
                  className="text-[#FFD700] hover:underline font-medium"
                >
                  Reset it here
                </a>
              </p>
            </form>

            {/* Info Message */}
            <div className="mt-6 p-4 bg-blue-500/10 border border-blue-500/20 rounded-lg">
              <p className="text-sm text-blue-300 text-center">
                ℹ️ Only authorized SNR team members can sign in.
                <br />
                First time? Use "Reset it here" to set up your password.
              </p>
            </div>
          </CardContent>
        </Card>

        <div className="mt-6 text-center">
          <p className="text-gray-500 text-sm">
            ðŸ”’ Secure authentication for authorized team members only
          </p>
          <p className="text-gray-600 text-xs mt-2">
            Need access? Contact your administrator
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginSupabase;
