import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Eye, Play } from "lucide-react";
import { Link } from "react-router-dom";

// Mock data - replace with API call later
const mockActivities = [
  {
    id: 1,
    name: "Flashcards",
    thumbnail: "https://placehold.co/600x400/png",
  },
  {
    id: 2,
    name: "Multiple Choice",
    thumbnail: "https://placehold.co/600x400/png",
  },
  {
    id: 3,
    name: "Word Match",
    thumbnail: "https://placehold.co/600x400/png",
  },
];

const StudyActivities = () => {
  return (
    <div className="animate-fade-up space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Study Activities</h1>
        <p className="text-muted-foreground mt-2">
          Choose an activity to start studying
        </p>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {mockActivities.map((activity) => (
          <Card key={activity.id} className="overflow-hidden">
            <img
              src={activity.thumbnail}
              alt={activity.name}
              className="aspect-video w-full object-cover"
            />
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <h3 className="font-semibold">{activity.name}</h3>
                <div className="flex gap-2">
                  <Link to={`/study_activities/${activity.id}`}>
                    <Button variant="ghost" size="icon">
                      <Eye className="h-4 w-4" />
                      <span className="sr-only">View Details</span>
                    </Button>
                  </Link>
                  <Link to={`/study_activities/${activity.id}/launch`}>
                    <Button variant="ghost" size="icon">
                      <Play className="h-4 w-4" />
                      <span className="sr-only">Launch Activity</span>
                    </Button>
                  </Link>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default StudyActivities;
