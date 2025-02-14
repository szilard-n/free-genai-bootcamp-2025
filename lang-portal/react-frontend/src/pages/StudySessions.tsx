import { useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Input } from "@/components/ui/input";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { Link } from "react-router-dom";
import { Search } from "lucide-react";

// Mock data - replace with API call later
const mockSessions = Array.from({ length: 30 }, (_, i) => ({
  id: i + 1,
  activityName: ["Flashcards", "Multiple Choice", "Word Match"][Math.floor(Math.random() * 3)],
  groupName: `Group ${Math.floor(Math.random() * 5) + 1}`,
  startTime: new Date(Date.now() - Math.random() * 10000000000).toLocaleString(),
  endTime: new Date(Date.now() - Math.random() * 5000000000).toLocaleString(),
  reviewItems: Math.floor(Math.random() * 50) + 10,
}));

const StudySessions = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  const filteredSessions = mockSessions.filter(
    (session) =>
      session.activityName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      session.groupName.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const totalPages = Math.ceil(filteredSessions.length / itemsPerPage);
  const currentSessions = filteredSessions.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  return (
    <div className="animate-fade-up space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Study Sessions</h1>
        <p className="text-muted-foreground mt-2">
          View your study history and progress
        </p>
      </div>

      <div className="relative">
        <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Search sessions..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="pl-10"
        />
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>Activity Name</TableHead>
              <TableHead>Group Name</TableHead>
              <TableHead>Start Time</TableHead>
              <TableHead>End Time</TableHead>
              <TableHead>Review Items</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {currentSessions.map((session) => (
              <TableRow key={session.id}>
                <TableCell>
                  <Link
                    to={`/study_sessions/${session.id}`}
                    className="text-blue-500 hover:underline"
                  >
                    #{session.id}
                  </Link>
                </TableCell>
                <TableCell>{session.activityName}</TableCell>
                <TableCell>{session.groupName}</TableCell>
                <TableCell>{session.startTime}</TableCell>
                <TableCell>{session.endTime}</TableCell>
                <TableCell>{session.reviewItems} words</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <Pagination>
        <PaginationContent>
          <PaginationItem>
            <PaginationPrevious
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              disabled={currentPage === 1}
            />
          </PaginationItem>
          {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
            <PaginationItem key={page}>
              <PaginationLink
                onClick={() => setCurrentPage(page)}
                isActive={currentPage === page}
              >
                {page}
              </PaginationLink>
            </PaginationItem>
          ))}
          <PaginationItem>
            <PaginationNext
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              disabled={currentPage === totalPages}
            />
          </PaginationItem>
        </PaginationContent>
      </Pagination>
    </div>
  );
};

export default StudySessions;
