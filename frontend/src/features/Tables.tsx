import { useState, useMemo } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { Link, useNavigate } from "react-router-dom";
import { apiFetch } from "../api";
import { Button } from "../components/ui/button";
import { Label } from "../components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../components/ui/card";
import { useToast } from "../components/ui/toast";
import { useGameDisplayName } from "../components/UserInfo";
import { useUserData } from "../contexts/UserContext";
import {
  Plus,
  RefreshCw,
  Trash2,
  Users,
  ArrowRight,
  Loader2,
  ChevronLeft,
  ChevronRight,
  Filter,
  ChevronDown,
  ChevronUp,
  X,
  LogIn,
} from "lucide-react";

const STATUS_OPTIONS = [
  { value: "not_started", label: "Not Started", color: "text-blue-400" },
  { value: "in_progress", label: "In Progress", color: "text-green-400" },
  { value: "finished", label: "Finished", color: "text-gray-400" },
  { value: "cancelled", label: "Cancelled", color: "text-yellow-400" },
  { value: "aborted", label: "Aborted", color: "text-red-400" },
] as const;

export function Tables() {
  const { addToast } = useToast();
  const navigate = useNavigate();
  const displayName = useGameDisplayName();
  const { isLoggedIn } = useUserData();

  const [page, setPage] = useState(1);
  const [selectedStatuses, setSelectedStatuses] = useState<string[]>([
    "not_started",
    "in_progress",
  ]);
  const [selectedGame, setSelectedGame] = useState<string>("five_hundred");
  const [filtersExpanded, setFiltersExpanded] = useState(false);

  const buildQueryParams = () => {
    const params = new URLSearchParams();

    if (selectedStatuses.length > 0) {
      params.append("status", selectedStatuses.join(","));
    }

    if (selectedGame) {
      params.append("game_name", selectedGame);
    }

    params.append("limit", "10");
    params.append("offset", ((page - 1) * 10).toString());

    return params.toString();
  };

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["tables", selectedStatuses, selectedGame, page],
    queryFn: () => apiFetch(`/api/v1/tables/?${buildQueryParams()}`),
    refetchInterval: 5000,
  });

  const createTable = useMutation({
    mutationFn: () =>
      apiFetch("/api/v1/tables/", {
        method: "POST",
        body: JSON.stringify({
          game_name: "five_hundred",
        }),
      }),
    onSuccess: () => {
      refetch();
      addToast({
        title: "Table created",
        description: "Your game table has been created successfully.",
      });
    },
    onError: (error) => {
      addToast({
        title: "Failed to create table",
        description: String(error),
        variant: "destructive",
      });
    },
  });

  const removeTable = useMutation({
    mutationFn: (tableId: string) =>
      apiFetch(`/api/v1/tables/${tableId}/`, {
        method: "DELETE",
      }),
    onSuccess: () => {
      refetch();
      addToast({
        title: "Table removed",
        description: "The game table has been removed.",
      });
    },
    onError: (error) => {
      addToast({
        title: "Failed to remove table",
        description: String(error),
        variant: "destructive",
      });
    },
  });

  const handleStatusToggle = (status: string) => {
    setSelectedStatuses((prev) =>
      prev.includes(status)
        ? prev.filter((s) => s !== status)
        : [...prev, status]
    );
    setPage(1);
  };

  const handleGameChange = (game: string) => {
    setSelectedGame(game);
    setPage(1);
  };

  const clearFilters = () => {
    setSelectedStatuses([]);
    setSelectedGame("five_hundred");
    setPage(1);
  };

  const activeFiltersCount = selectedStatuses.length;
  const hasActiveFilters =
    activeFiltersCount > 0 || selectedGame !== "five_hundred";

  const paginationInfo = useMemo(() => {
    if (!data) return null;

    const count = data.count || 0;
    const limit = 10;
    const totalPages = Math.ceil(count / limit);

    return {
      count,
      totalPages,
      currentPage: page,
      hasNext: data.next !== null,
      hasPrevious: data.previous !== null,
    };
  }, [data, page]);

  if (isLoading)
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );

  if (error)
    return (
      <Card className="border-destructive">
        <CardContent className="pt-6">
          <p className="text-destructive">{String(error)}</p>
        </CardContent>
      </Card>
    );

  const tables = (data?.results ?? []) as any[];

  return (
    <div className="space-y-6">
      <Card className="card-glow">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-2xl">Game Tables</CardTitle>
              <CardDescription>
                {isLoggedIn
                  ? `Welcome, ${displayName}! Create or join a game table to start playing`
                  : "Browse available game tables. Login to create or join a table."}
              </CardDescription>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm" onClick={() => refetch()}>
                <RefreshCw className="mr-2 h-4 w-4" />
                Refresh
              </Button>
              {isLoggedIn ? (
                <Button
                  onClick={() => createTable.mutate()}
                  disabled={createTable.isPending}
                >
                  {createTable.isPending ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Creating...
                    </>
                  ) : (
                    <>
                      <Plus className="mr-2 h-4 w-4" />
                      Create Table
                    </>
                  )}
                </Button>
              ) : (
                <Button onClick={() => navigate("/login")} variant="default">
                  <LogIn className="mr-2 h-4 w-4" />
                  Login
                </Button>
              )}
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {/* Compact Filters */}
          <div className="mb-4 space-y-2">
            <div className="flex items-center gap-2 flex-wrap">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setFiltersExpanded(!filtersExpanded)}
                className="gap-2"
              >
                <Filter className="h-4 w-4" />
                Filters
                {activeFiltersCount > 0 && (
                  <span className="ml-1 px-1.5 py-0.5 text-xs bg-primary text-primary-foreground rounded-full">
                    {activeFiltersCount}
                  </span>
                )}
                {filtersExpanded ? (
                  <ChevronUp className="h-4 w-4" />
                ) : (
                  <ChevronDown className="h-4 w-4" />
                )}
              </Button>

              {hasActiveFilters && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={clearFilters}
                  className="gap-1 text-muted-foreground hover:text-foreground"
                >
                  <X className="h-4 w-4" />
                  Clear
                </Button>
              )}

              {paginationInfo && (
                <div className="ml-auto text-sm text-muted-foreground">
                  {paginationInfo.count}{" "}
                  {paginationInfo.count === 1 ? "table" : "tables"}
                </div>
              )}
            </div>

            {filtersExpanded && (
              <div className="bg-muted/50 rounded-lg p-4 space-y-3 animate-in slide-in-from-top-2 duration-200">
                {/* Game Filter */}
                <div>
                  <Label className="text-xs font-semibold text-muted-foreground mb-1.5 block">
                    Game
                  </Label>
                  <select
                    value={selectedGame}
                    onChange={(e) => handleGameChange(e.target.value)}
                    className="h-9 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                  >
                    <option value="five_hundred">Five Hundred</option>
                  </select>
                </div>

                {/* Status Filters */}
                <div>
                  <Label className="text-xs font-semibold text-muted-foreground mb-1.5 block">
                    Status
                  </Label>
                  <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2">
                    {STATUS_OPTIONS.map((status) => (
                      <label
                        key={status.value}
                        className="flex items-center space-x-2 cursor-pointer hover:bg-accent p-2 rounded-md transition-colors"
                      >
                        <input
                          type="checkbox"
                          checked={selectedStatuses.includes(status.value)}
                          onChange={() => handleStatusToggle(status.value)}
                          className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                        />
                        <span className={`text-sm ${status.color}`}>
                          {status.label}
                        </span>
                      </label>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Tables List */}
          {tables.length === 0 ? (
            <div className="text-center py-12">
              <Users className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
              <p className="text-muted-foreground mb-4">No tables available</p>
              {isLoggedIn ? (
                <Button onClick={() => createTable.mutate()}>
                  <Plus className="mr-2 h-4 w-4" />
                  Create Your First Table
                </Button>
              ) : (
                <Button onClick={() => navigate("/login")}>
                  <LogIn className="mr-2 h-4 w-4" />
                  Login to Create Table
                </Button>
              )}
            </div>
          ) : (
            <>
              <div className="space-y-2">
                {tables.map((t) => (
                  <Card key={t.id} className="card-hover">
                    <CardContent className="pt-4 pb-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3 flex-1 min-w-0">
                          <div className="p-2 rounded-full bg-primary/20">
                            <Users className="h-4 w-4 text-primary" />
                          </div>
                          <div className="flex-1 min-w-0">
                            <div className="font-medium capitalize text-sm">
                              {t.game_name.replace("_", " ")}
                            </div>
                            <div className="text-xs text-muted-foreground">
                              Status:{" "}
                              <span className="font-medium capitalize">
                                {t.status.replace("_", " ")}
                              </span>{" "}
                              • Players:{" "}
                              <span className="font-medium">
                                {t.game_table_players.length}
                              </span>
                            </div>
                            {/* Player Names */}
                            {t.game_table_players &&
                              t.game_table_players.length > 0 && (
                                <div className="mt-1.5 flex items-center gap-2 flex-wrap">
                                  <span className="text-xs text-muted-foreground">
                                    Players:
                                  </span>
                                  <div className="flex items-center gap-1.5 flex-wrap">
                                    {t.game_table_players.map(
                                      (player: any, idx: number) => (
                                        <div
                                          key={idx}
                                          className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-muted/50 text-xs"
                                        >
                                          <span className="text-foreground font-medium">
                                            {player.screen_name}
                                          </span>
                                          {player.bot_strategy_kind && (
                                            <span className="text-muted-foreground text-[10px]">
                                              (bot)
                                            </span>
                                          )}
                                        </div>
                                      )
                                    )}
                                  </div>
                                </div>
                              )}
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <Link to={`/tables/${t.id}`}>
                            <Button size="sm" variant="default">
                              Open
                              <ArrowRight className="ml-1.5 h-3.5 w-3.5" />
                            </Button>
                          </Link>
                          {isLoggedIn && (
                            <Button
                              variant="destructive"
                              size="sm"
                              onClick={() => removeTable.mutate(t.id)}
                              disabled={removeTable.isPending}
                            >
                              <Trash2 className="h-3.5 w-3.5" />
                            </Button>
                          )}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>

              {/* Pagination */}
              {paginationInfo && paginationInfo.totalPages > 1 && (
                <div className="flex items-center justify-between mt-4 pt-4 border-t">
                  <div className="text-xs text-muted-foreground">
                    Page {paginationInfo.currentPage} of{" "}
                    {paginationInfo.totalPages}
                  </div>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setPage(page - 1)}
                      disabled={!paginationInfo.hasPrevious}
                    >
                      <ChevronLeft className="h-4 w-4" />
                      Prev
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setPage(page + 1)}
                      disabled={!paginationInfo.hasNext}
                    >
                      Next
                      <ChevronRight className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              )}
            </>
          )}
        </CardContent>
      </Card>

      <details>
        <summary className="cursor-pointer text-sm text-muted-foreground hover:text-foreground">
          View Raw Data (Debug)
        </summary>
        <Card className="mt-2">
          <CardContent className="pt-6">
            <pre className="text-xs overflow-auto max-h-96">
              {JSON.stringify(data, null, 2)}
            </pre>
          </CardContent>
        </Card>
      </details>
    </div>
  );
}
