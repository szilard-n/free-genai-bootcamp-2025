import { useState } from "react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow, } from "@/components/ui/table";
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
import { GroupsService } from "@/services/groups-service.ts";
import { useQuery } from "@tanstack/react-query";

const Groups = () => {
    const [searchQuery, setSearchQuery] = useState("");
    const [currentPage, setCurrentPage] = useState(1);

    const { data: paginatedResponse, isLoading, error } = useQuery({
        queryKey: ["groups", currentPage],
        queryFn: () => GroupsService.getGroups(currentPage),
    });

    if (error) {
        console.error('Error fetching words:', error);
        return <div>Error loading words: {error.message}</div>;
    }

    if (isLoading) {
        return <div>Loading...</div>;
    }

    const filteredGroups = paginatedResponse?.data?.filter(
        (group) =>
            group.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            group.description.toLowerCase().includes(searchQuery.toLowerCase())
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
                        {filteredGroups.map((group) => (
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

export default Groups;
