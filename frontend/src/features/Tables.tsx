import { useMutation, useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { apiFetch } from "../api";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { useToast } from "../components/ui/toast";
import { Plus, RefreshCw, Trash2, Users, ArrowRight, Loader2 } from "lucide-react";

export function Tables() {
  const { addToast } = useToast();

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["tables"],
    queryFn: () => apiFetch("/api/v1/tables/"),
    refetchInterval: 5000, // Poll every 5 seconds to see new tables and status updates
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

  if (isLoading) return (
    <div className="flex items-center justify-center min-h-[400px]">
      <Loader2 className="h-8 w-8 animate-spin text-primary" />
    </div>
  );

  if (error) return (
    <Card className="border-destructive">
      <CardContent className="pt-6">
        <p className="text-destructive">{String(error)}</p>
      </CardContent>
    </Card>
  );

  const tables = (data?.tables ?? []) as any[];
  
  return (
    <div className="space-y-6">
      <Card className="card-glow">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-2xl">Game Tables</CardTitle>
              <CardDescription>Create or join a game table to start playing</CardDescription>
            </div>
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => refetch()}
              >
                <RefreshCw className="mr-2 h-4 w-4" />
                Refresh
              </Button>
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
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {tables.length === 0 ? (
            <div className="text-center py-12">
              <Users className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
              <p className="text-muted-foreground mb-4">No tables available</p>
              <Button onClick={() => createTable.mutate()}>
                <Plus className="mr-2 h-4 w-4" />
                Create Your First Table
              </Button>
            </div>
          ) : (
            <div className="space-y-3">
              {tables.map((t) => (
                <Card key={t.id} className="card-hover">
                  <CardContent className="pt-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <div className="p-3 rounded-full bg-primary/20">
                          <Users className="h-5 w-5 text-primary" />
                        </div>
                        <div>
                          <div className="font-medium capitalize">
                            {t.game_name.replace("_", " ")}
                          </div>
                          <div className="text-sm text-muted-foreground">
                            Status: <span className="font-medium">{t.status}</span> • 
                            Players: <span className="font-medium">{t.game_table_players.length}</span>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Link to={`/tables/${t.id}`}>
                          <Button size="sm">
                            Open Table
                            <ArrowRight className="ml-2 h-4 w-4" />
                          </Button>
                        </Link>
                        <Button
                          variant="destructive"
                          size="sm"
                          onClick={() => removeTable.mutate(t.id)}
                          disabled={removeTable.isPending}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
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
