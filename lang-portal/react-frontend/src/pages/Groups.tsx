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
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { Plus, Search, Users } from "lucide-react";
import { Badge } from "@/components/ui/badge";

// Mock data - replace with API call later
const mockGroups = Array.from({ length: 20 }, (_, i) => ({
  id: i + 1,
  name: `Group ${i + 1}`,
  description: `Description for group ${i + 1}`,
  wordCount: Math.floor(Math.random() * 100),
  lastStudied: new Date(Date.now() - Math.random() * 10000000000).toLocaleDateString(),
  status: Math.random() > 0.5 ? "active" : "inactive",
}));

const Groups = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  const filteredGroups = mockGroups.filter(
    (group) =>
      group.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      group.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const totalPages = Math.ceil(filteredGroups.length / itemsPerPage);
  const currentGroups = filteredGroups.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  return (
    <div className="animate-fade-up space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Groups</h1>
          <p className="text-muted-foreground mt-2">
            Manage your study groups and word collections
          </p>
        </div>
        <Button className="gap-2">
          <Plus className="h-4 w-4" />
          New Group
        </Button>
      </div>

      <div className="relative">
        <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Search groups..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="pl-10"
        />
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Description</TableHead>
              <TableHead>Words</TableHead>
              <TableHead>Last Studied</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {currentGroups.map((group) => (
              <TableRow key={group.id}>
                <TableCell>
                  <Link
                    to={`/groups/${group.id}`}
                    className="flex items-center gap-2 text-blue-500 hover:underline"
                  >
                    <Users className="h-4 w-4" />
                    {group.name}
                  </Link>
                </TableCell>
                <TableCell>{group.description}</TableCell>
                <TableCell>{group.wordCount} words</TableCell>
                <TableCell>{group.lastStudied}</TableCell>
                <TableCell>
                  <Badge
                    variant={group.status === "active" ? "default" : "secondary"}
                  >
                    {group.status}
                  </Badge>
                </TableCell>
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

export default Groups;
