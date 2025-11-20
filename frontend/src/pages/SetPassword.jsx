import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase, authHelpers } from '../lib/supabase';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Label } from '../components/ui/label';
import { toast } from 'sonner';

const SetPassword = () => {
    const navigate = useNavigate();
    const [checking, setChecking] = useState(true);
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        let isMounted = true;
        
        // Check if we have the recovery token in the URL hash or sessionStorage
        const checkRecoveryToken = async () => {
            try {
                // First check if we already have a token in sessionStorage
                const existingToken = sessionStorage.getItem('recovery_token');
                if (existingToken) {
                    console.log('Recovery token found in sessionStorage, ready for password reset');
                    if (isMounted) {
                        setChecking(false);
                    }
                    return;
                }

                // Get hash fragment from URL
                const hashParams = new URLSearchParams(window.location.hash.substring(1));
                const accessToken = hashParams.get('access_token');
                const refreshToken = hashParams.get('refresh_token');
                const tokenType = hashParams.get('type');

                console.log('Hash params:', { 
                    accessToken: accessToken ? accessToken.substring(0, 20) + '...' : null, 
                    refreshToken: !!refreshToken, 
                    tokenType 
                });

                if (accessToken && tokenType === 'recovery') {
                    console.log('Valid recovery token found, cleaning URL and allowing password reset...');
                    
                    // Store the token temporarily for password update
                    sessionStorage.setItem('recovery_token', accessToken);
                    
                    // Clean up the URL immediately
                    window.history.replaceState({}, document.title, window.location.pathname);
                    
                    if (isMounted) {
                        setChecking(false);
                    }
                } else {
                    // No valid token found
                    console.log('No valid token found in URL');
                    if (isMounted) {
                        setError('Invalid reset link. Please request a new password reset.');
                        setChecking(false);
                    }
                }
            } catch (err) {
                console.error('Error processing recovery token:', err);
                if (isMounted) {
                    setError('An error occurred. Please try again.');
                    setChecking(false);
                }
            }
        };

        // Run the check immediately
        checkRecoveryToken();

        return () => {
            isMounted = false;
        };
    }, []);


    const handleSetPassword = async (e) => {
        e.preventDefault();
        setError('');

        // Validation
        if (password.length < 6) {
            setError('Password must be at least 6 characters long');
            toast.error('Password must be at least 6 characters long');
            return;
        }

        if (password !== confirmPassword) {
            setError('Passwords do not match');
            toast.error('Passwords do not match');
            return;
        }

        setLoading(true);

        try {
            // Get the recovery token from sessionStorage
            const recoveryToken = sessionStorage.getItem('recovery_token');
            
            if (!recoveryToken) {
                setError('Session expired. Please request a new reset link.');
                toast.error('Session expired. Please request a new reset link.');
                setLoading(false);
                return;
            }

            console.log('Updating password with recovery token...');

            // Use Supabase's updateUser with the recovery token
            const { data, error } = await supabase.auth.updateUser(
                { password: password },
                { 
                    accessToken: recoveryToken 
                }
            );

            if (error) {
                console.error('Password update error:', error);
                setError(error.message || 'Failed to update password');
                toast.error(error.message || 'Failed to update password');
            } else {
                console.log('Password updated successfully');
                setSuccess(true);
                toast.success('Password updated successfully!');
                
                // Clear the recovery token
                sessionStorage.removeItem('recovery_token');
                
                // Redirect to login after 2 seconds
                setTimeout(() => {
                    navigate('/login');
                }, 2000);
            }
        } catch (err) {
            console.error('Password update exception:', err);
            setError('An error occurred. Please try again.');
            toast.error('An error occurred. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center p-4">
            <div className="w-full max-w-md">
                <div className="text-center mb-8">
                    <div className="relative w-32 h-32 mx-auto mb-4">
                        <img 
                            src="https://customer-assets.emergentagent.com/job_25d84bc8-5cd6-4672-913d-7856f1b8c2dc/artifacts/7ukgfyx7_snr%20logo%20png.jpg" 
                            alt="SNR" 
                            className="w-32 h-32 rounded-full border-4 border-[#FFD700] object-cover logo-glow" 
                        />
                    </div>
                    <h1 className="text-4xl font-bold mb-2 gold-gradient">SNR AUTOMATIONS</h1>
                    <p className="text-gray-400">Team Dashboard</p>
                </div>
                <Card className="glass-effect border-[rgba(255,215,0,0.2)]">
                    <CardHeader>
                        <CardTitle className="text-2xl text-white">Set New Password</CardTitle>
                        <CardDescription className="text-gray-400">
                            {checking ? 'Verifying reset link...' : success ? 'Password updated!' : 'Enter your new password'}
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        {checking ? (
                            <div className="text-center py-8">
                                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#FFD700] mx-auto mb-4"></div>
                                <p className="text-gray-400">Verifying reset link...</p>
                            </div>
                        ) : error ? (
                            <div className="space-y-4">
                                <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-4 text-center">
                                    <p className="text-red-400 text-sm">{error}</p>
                                </div>
                                <Button 
                                    onClick={() => navigate('/reset-password')} 
                                    className="w-full btn-primary"
                                >
                                    Request New Reset Link
                                </Button>
                            </div>
                        ) : success ? (
                            <div className="space-y-4">
                                <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-4 text-center">
                                    <p className="text-green-400 text-sm">Password updated successfully! Redirecting...</p>
                                </div>
                            </div>
                        ) : (
                            <form onSubmit={handleSetPassword} className="space-y-4">
                                <div>
                                    <Label className="text-gray-300">New Password</Label>
                                    <Input 
                                        type="password" 
                                        placeholder="Enter new password (min 6 characters)" 
                                        value={password} 
                                        onChange={(e) => setPassword(e.target.value)} 
                                        required 
                                        className="bg-[rgba(255,255,255,0.05)] border-[rgba(255,215,0,0.2)] text-white" 
                                        disabled={loading}
                                    />
                                </div>
                                <div>
                                    <Label className="text-gray-300">Confirm New Password</Label>
                                    <Input 
                                        type="password" 
                                        placeholder="Confirm new password" 
                                        value={confirmPassword} 
                                        onChange={(e) => setConfirmPassword(e.target.value)} 
                                        required 
                                        className="bg-[rgba(255,255,255,0.05)] border-[rgba(255,215,0,0.2)] text-white" 
                                        disabled={loading}
                                    />
                                </div>
                                <Button 
                                    type="submit" 
                                    className="w-full btn-primary" 
                                    disabled={loading}
                                >
                                    {loading ? 'Updating Password...' : 'Update Password'}
                                </Button>
                                <p className="text-center text-sm">
                                    <a href="/login" className="text-[#FFD700]">Back to Login</a>
                                </p>
                            </form>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};

export default SetPassword;
