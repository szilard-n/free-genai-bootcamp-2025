import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "./lib/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import StudyActivities from "./pages/StudyActivities";
import StudyActivityShow from "./pages/StudyActivityShow";
import StudyActivityLaunch from "./pages/StudyActivityLaunch";
import Words from "./pages/Words";
import WordShow from "./pages/WordShow";
import Groups from "./pages/Groups";
import GroupShow from "./pages/GroupShow";
import StudySessions from "./pages/StudySessions";
import StudySessionShow from "./pages/StudySessionShow";
import Settings from "./pages/Settings";
import NotFound from "./pages/NotFound";
import { ThemeProvider } from "./components/ThemeProvider";

const App = () => (
  <ThemeProvider defaultTheme="system" storageKey="app-theme">
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Layout />}>
              <Route index element={<Dashboard />} />
              <Route path="dashboard" element={<Dashboard />} />
              <Route path="study_activities" element={<StudyActivities />} />
              <Route path="study_activities/:id" element={<StudyActivityShow />} />
              <Route path="study_activities/:id/launch" element={<StudyActivityLaunch />} />
              <Route path="words" element={<Words />} />
              <Route path="words/:id" element={<WordShow />} />
              <Route path="groups" element={<Groups />} />
              <Route path="groups/:id" element={<GroupShow />} />
              <Route path="study_sessions" element={<StudySessions />} />
              <Route path="study_sessions/:id" element={<StudySessionShow />} />
              <Route path="settings" element={<Settings />} />
              <Route path="*" element={<NotFound />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </TooltipProvider>
    </QueryClientProvider>
  </ThemeProvider>
);

export default App;
