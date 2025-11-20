import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';
import { authHelpers } from '@/lib/supabase';

const ResetPassword = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [resetSent, setResetSent] = useState(false);
  const [email, setEmail] = useState('');

  const handleRequestReset = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const { error } = await authHelpers.resetPassword(email);
      if (error) {
        toast.error(error.message || 'Failed to send reset email.');
        return;
      }
      setResetSent(true);
      toast.success('Password reset email sent! Check your inbox.');
    } catch (error) {
      toast.error('An unexpected error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="relative w-32 h-32 mx-auto mb-4">
            <img src="https://customer-assets.emergentagent.com/job_25d84bc8-5cd6-4672-913d-7856f1b8c2dc/artifacts/7ukgfyx7_snr%20logo%20png.jpg" alt="SNR" className="w-32 h-32 rounded-full border-4 border-[#FFD700] object-cover logo-glow" />
          </div>
          <h1 className="text-4xl font-bold mb-2 gold-gradient">SNR AUTOMATIONS</h1>
          <p className="text-gray-400">Team Dashboard</p>
        </div>
        <Card className="glass-effect border-[rgba(255,215,0,0.2)]">
          <CardHeader>
            <CardTitle className="text-2xl text-white">Reset Password</CardTitle>
            <CardDescription className="text-gray-400">{resetSent ? 'Check your email' : 'Enter your email'}</CardDescription>
          </CardHeader>
          <CardContent>
            {resetSent ? (
              <div className="space-y-4">
                <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-4 text-center">
                  <p className="text-green-400 text-sm">Email sent!</p>
                </div>
                <Button onClick={() => navigate('/login')} className="w-full btn-primary">Back to Login</Button>
              </div>
            ) : (
              <form onSubmit={handleRequestReset} className="space-y-4">
                <div>
                  <Label className="text-gray-300">Email</Label>
                  <Input type="email" placeholder="your.email@gmail.com" value={email} onChange={(e) => setEmail(e.target.value)} required className="bg-[rgba(255,255,255,0.05)] border-[rgba(255,215,0,0.2)] text-white" />
                </div>
                <Button type="submit" className="w-full btn-primary" disabled={loading}>{loading ? 'Sending...' : 'Send Reset Email'}</Button>
                <p className="text-center text-sm"><a href="/login" className="text-[#FFD700]">Back to Login</a></p>
              </form>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ResetPassword;
