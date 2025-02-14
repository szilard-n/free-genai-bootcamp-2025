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
import { WordsService } from "@/services/words-service";
import { useQuery } from "@tanstack/react-query";

const Words = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  const { data: paginatedResponse, isLoading, error } = useQuery({
    queryKey: ["words", currentPage],
    queryFn: () => WordsService.getWords(currentPage),
  });

  const filteredWords = paginatedResponse?.data?.filter(
    (word) =>
      word.german.toLowerCase().includes(searchQuery.toLowerCase()) ||
      word.english.toLowerCase().includes(searchQuery.toLowerCase())
  ) || [];

  if (error) {
    console.error('Error fetching words:', error);
    return <div>Error loading words: {error.message}</div>;
  }

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="animate-fade-up space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Words</h1>
        <p className="text-muted-foreground mt-2">
          Manage and review your vocabulary
        </p>
      </div>

      <div className="relative">
        <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Search words..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="pl-10"
        />
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>German</TableHead>
              <TableHead>English</TableHead>
              <TableHead>Class</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredWords.map((word) => (
              <TableRow key={word.id}>
                <TableCell>
                  <Link
                    to={`/words/${word.id}`}
                    className="text-blue-500 hover:underline"
                  >
                    {word.german}
                  </Link>
                </TableCell>
                <TableCell>{word.english}</TableCell>
                <TableCell>{word.class}</TableCell>
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
          {Array.from({ length: paginatedResponse?.pages || 0 }, (_, i) => i + 1).map((page) => (
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
              onClick={() => setCurrentPage((p) => Math.min(paginatedResponse?.pages || 1, p + 1))}
              disabled={currentPage === paginatedResponse?.pages}
            />
          </PaginationItem>
        </PaginationContent>
      </Pagination>
    </div>
  );
};

export default Words;
