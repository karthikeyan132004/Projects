import { useState, useEffect } from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import LoginSupabase from "./pages/LoginSupabase";
import ResetPassword from "./pages/ResetPassword";
import SetPassword from "./pages/SetPassword";
import Dashboard from "./pages/Dashboard";
import TeamManagement from "./pages/TeamManagement";
import Projects from "./pages/Projects";
import Calendar from "./pages/Calendar";
import LeaveManagement from "./pages/LeaveManagement";
import ContentStudio from "./pages/ContentStudio";
import AILab from "./pages/AILab";
import CloudPanel from "./pages/CloudPanel";
import ResearchHub from "./pages/ResearchHub";
import PersonalPlanner from "./pages/PersonalPlanner";
import Finance from "./pages/Finance";
import Attendance from "./pages/Attendance";
import Training from "./pages/Training";
import Subscriptions from "./pages/Subscriptions";
import { Toaster } from "sonner";
import { authHelpers } from "@/lib/supabase";

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    document.documentElement.classList.add("dark");

    const initializeAuth = async () => {
      try {
        const { session } = await authHelpers.getSession();

        if (session?.user) {
          const { data: profile } = await authHelpers.getUserProfile(session.user.id);

          if (profile) {
            setUser({
              id: profile.id,
              email: profile.email,
              name: profile.name,
              role: profile.role,
              contact: profile.contact,
              skillset: profile.skillset || [],
              current_tasks: profile.current_tasks || [],
            });
          }
        }
      } catch (error) {
        console.error("Auth initialization error:", error);
      } finally {
        setLoading(false);
      }
    };

    initializeAuth();

    const { data: authListener } = authHelpers.onAuthStateChange(
      async (event, session) => {
        if (event === "SIGNED_IN" && session?.user) {
          const { data: profile } = await authHelpers.getUserProfile(session.user.id);
          if (profile) {
            setUser({
              id: profile.id,
              email: profile.email,
              name: profile.name,
              role: profile.role,
              contact: profile.contact,
              skillset: profile.skillset || [],
              current_tasks: profile.current_tasks || [],
            });
          }
        } else if (event === "SIGNED_OUT") {
          setUser(null);
        }
      }
    );

    return () => {
      authListener?.subscription?.unsubscribe();
    };
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = async () => {
    await authHelpers.signOut();
    setUser(null);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-[#0a0a0a] text-white">
        Loading...
      </div>
    );
  }

  return (
    <div className="App bg-[#0a0a0a] text-white min-h-screen">
      <Toaster position="top-right" richColors />

      <BrowserRouter>
        <Routes>
          <Route
            path="/login"
            element={!user ? (
              <LoginSupabase onLogin={handleLogin} />
            ) : (
              <Navigate to="/" />
            )}
          />

          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="/set-password" element={<SetPassword />} />

          <Route
            path="/"
            element={
              user ? (
                <Dashboard user={user} onLogout={handleLogout} />
              ) : (
                <Navigate to="/login" />
              )
            }
          />

          <Route
            path="/team"
            element={
              user ? (
                <TeamManagement user={user} onLogout={handleLogout} />
              ) : (
                <Navigate to="/login" />
              )
            }
          />

          <Route
            path="/projects"
            element={
              user ? (
                <Projects user={user} onLogout={handleLogout} />
              ) : (
                <Navigate to="/login" />
              )
            }
          />

          <Route
            path="/calendar"
            element={
              user ? (
                <Calendar user={user} onLogout={handleLogout} />
              ) : (
                <Navigate to="/login" />
              )
            }
          />

          <Route
            path="/leave"
            element={
              user ? (
                <LeaveManagement user={user} onLogout={handleLogout} />
              ) : (
                <Navigate to="/login" />
              )
            }
          />

          <Route
            path="/content"
            element={
              user ? (
                <ContentStudio user={user} onLogout={handleLogout} />
              ) : (
                <Navigate to="/login" />
              )
            }
          />

          <Route
            path="/ai-lab"
            element={
              user ? (
                <AILab user={user} onLogout={handleLogout} />
              ) : (
                <Navigate to="/login" />
              )
            }
          />

          <Route
            path="/cloud"
            element={
              user ? (
                <CloudPanel user={user} onLogout={handleLogout} />
              ) : (
                <Navigate to="/login" />
              )
            }
          />

          <Route
            path="/research"
            element={
              user ? (
                <ResearchHub user={user} onLogout={handleLogout} />
              ) : (
                <Navigate to="/login" />
              )
            }
          />

          <Route
            path="/planner"
            element={
              user ? (
                <PersonalPlanner user={user} onLogout={handleLogout} />
              ) : (
                <Navigate to="/login" />
              )
            }
          />

          <Route
            path="/finance"
            element={
              user ? (
                <Finance user={user} onLogout={handleLogout} />
              ) : (
                <Navigate to="/login" />
              )
            }
          />

          <Route
            path="/attendance"
            element={
              user ? (
                <Attendance user={user} onLogout={handleLogout} />
              ) : (
                <Navigate to="/login" />
              )
            }
          />

          <Route
            path="/training"
            element={
              user ? (
                <Training user={user} onLogout={handleLogout} />
              ) : (
                <Navigate to="/login" />
              )
            }
          />

          <Route
            path="/subscriptions"
            element={
              user ? (
                <Subscriptions user={user} onLogout={handleLogout} />
              ) : (
                <Navigate to="/login" />
              )
            }
          />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
