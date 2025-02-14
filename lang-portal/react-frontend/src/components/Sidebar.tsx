
import { Link, useLocation } from "react-router-dom";
import { cn } from "@/lib/utils";
import { Book, BarChart, Layers, Settings, Users2, Clock, Layout as LayoutIcon } from "lucide-react";

const navigation = [
  { name: "Dashboard", href: "/dashboard", icon: BarChart },
  { name: "Study Activities", href: "/study_activities", icon: LayoutIcon },
  { name: "Words", href: "/words", icon: Book },
  { name: "Groups", href: "/groups", icon: Users2 },
  { name: "Study Sessions", href: "/study_sessions", icon: Clock },
  { name: "Settings", href: "/settings", icon: Settings },
];

const Sidebar = () => {
  const location = useLocation();

  return (
    <div className="flex h-screen w-64 flex-col border-r bg-card px-3">
      <div className="flex h-16 items-center px-4">
        <Link to="/" className="flex items-center space-x-2">
          <Layers className="h-6 w-6" />
          <span className="text-lg font-semibold">Language Portal</span>
        </Link>
      </div>
      <nav className="flex-1 space-y-1 px-2 py-4">
        {navigation.map((item) => {
          const isActive = location.pathname.startsWith(item.href);
          return (
            <Link
              key={item.name}
              to={item.href}
              className={cn(
                "group flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors",
                isActive
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
              )}
            >
              <item.icon className="mr-3 h-4 w-4" />
              {item.name}
            </Link>
          );
        })}
      </nav>
    </div>
  );
};

export default Sidebar;
