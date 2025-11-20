import { createClient } from '@supabase/supabase-js';

// Supabase configuration
const supabaseUrl = process.env.REACT_APP_SUPABASE_URL || 'https://dzlscihzuxyzvsdodcnr.supabase.co';
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR6bHNjaWh6dXh5enZzZG9kY25yIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzE0MzUwMDcsImV4cCI6MjA0NzAxMTAwN30.9gB_-wkCJEPmeWq2bVFd8F_8Y-j3_t6KN7Pp7uEpkDs';

// Create Supabase client
export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
    auth: {
        autoRefreshToken: true,
        persistSession: true,
        detectSessionInUrl: true,
    },
});

// Auth helper functions
export const authHelpers = {
    // Sign in with email and password (ONLY method available - NO SIGNUPS)
    async signIn(email, password) {
        // First check if email is authorized
        const { isAuthorized } = await this.isEmailAuthorized(email);

        if (!isAuthorized) {
            return {
                data: null,
                error: { message: 'This email is not authorized to access the system. Contact your administrator.' }
            };
        }

        const { data, error } = await supabase.auth.signInWithPassword({
            email,
            password,
        });
        return { data, error };
    },

    // NO SIGNUP FUNCTION - This is intentionally removed
    // Users can only sign in with pre-approved emails

    // Sign out
    async signOut() {
        const { error } = await supabase.auth.signOut();
        return { error };
    },

    // Send password reset email (Forgot Password)
    async resetPassword(email) {
        try {
            // Send password reset email directly
            // Supabase will only send if the user exists in auth.users
            const { data, error } = await supabase.auth.resetPasswordForEmail(email, {
                redirectTo: `http://localhost:3001/set-password`,
            });

            if (error) {
                console.error('Reset password error:', error);
                return { data: null, error };
            }

            // Always return success to prevent email enumeration
            return { data, error: null };
        } catch (err) {
            console.error('Reset password exception:', err);
            return { data: null, error: { message: 'Failed to send reset email.' } };
        }
    },

    // Update password
    async updatePassword(newPassword) {
        const { data, error } = await supabase.auth.updateUser({
            password: newPassword,
        });
        return { data, error };
    },

    // Get current user
    async getCurrentUser() {
        const { data: { user }, error } = await supabase.auth.getUser();
        return { user, error };
    },

    // Get current session
    async getSession() {
        const { data: { session }, error } = await supabase.auth.getSession();
        return { session, error };
    },

    // Check if email is authorized
    async isEmailAuthorized(email) {
        try {
            // Add timeout to prevent hanging
            const timeoutPromise = new Promise((_, reject) =>
                setTimeout(() => reject(new Error('Authorization check timeout')), 5000)
            );

            const queryPromise = supabase
                .from('authorized_users')
                .select('*')
                .eq('email', email)
                .eq('is_active', true)
                .maybeSingle();

            const { data, error } = await Promise.race([queryPromise, timeoutPromise]);

            // If error and it's not "no rows" error, return it
            if (error && error.code !== 'PGRST116') {
                console.error('Error checking email authorization:', error);
                return { isAuthorized: false, data: null, error };
            }

            // Return true if we found a matching user
            return { isAuthorized: !!data, data, error: null };
        } catch (err) {
            console.error('Exception checking email authorization:', err);
            return { isAuthorized: false, data: null, error: err };
        }
    },

    // Get user profile
    async getUserProfile(userId) {
        try {
            const { data, error } = await supabase
                .from('user_profiles')
                .select('*')
                .eq('id', userId)
                .maybeSingle();

            return { data, error };
        } catch (err) {
            console.error('Exception getting user profile:', err);
            return { data: null, error: err };
        }
    },

    // Listen to auth state changes
    onAuthStateChange(callback) {
        return supabase.auth.onAuthStateChange(callback);
    },
};

export default supabase;