import { useMutation, useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { apiFetch } from "../api";
import { useState } from "react";

export function Tables() {
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["tables"],
    queryFn: () => apiFetch("/api/v1/tables/"),
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
      setErrorMessage(null);
    },
    onError: (error) => {
      setErrorMessage(String(error));
    },
  });

  const removeTable = useMutation({
    mutationFn: (tableId: string) =>
      apiFetch(`/api/v1/tables/${tableId}/`, {
        method: "DELETE",
      }),
    onSuccess: () => {
      refetch();
      setErrorMessage(null);
    },
    onError: (error) => {
      setErrorMessage(String(error));
    },
  });

  if (isLoading) return <div>Loading tables...</div>;
  if (error) return <div className="text-red-600">{String(error)}</div>;

  const tables = (data?.tables ?? []) as any[];
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-medium">Tables</h2>
        <div className="flex items-center gap-2">
          <button
            className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700"
            onClick={() => createTable.mutate()}
            disabled={createTable.isPending}
          >
            {createTable.isPending ? "Creating..." : "Create Table"}
          </button>
          <button className="text-sm underline" onClick={() => refetch()}>
            Refresh
          </button>
        </div>
      </div>
      {errorMessage && (
        <div className="text-red-600 text-sm">{errorMessage}</div>
      )}
      <ul className="space-y-2">
        {tables.map((t) => (
          <li key={t.id} className="border rounded p-3 bg-white">
            <div className="flex items-center justify-between">
              <div className="text-sm">
                {t.game_name} — {t.status} - {t.game_table_players.length}{" "}
                players
              </div>
              <div className="flex items-center gap-2">
                <Link
                  to={`/tables/${t.id}`}
                  className="text-blue-600 text-sm underline"
                >
                  Open
                </Link>
                <button
                  className="text-red-600 text-sm underline hover:text-red-800"
                  onClick={() => removeTable.mutate(t.id)}
                  disabled={removeTable.isPending}
                >
                  {removeTable.isPending ? "Removing..." : "Remove"}
                </button>
              </div>
            </div>
          </li>
        ))}
      </ul>
      <details>
        <summary className="cursor-pointer text-sm">Raw</summary>
        <pre className="text-xs bg-white p-3 rounded border overflow-auto">
          {JSON.stringify(data, null, 2)}
        </pre>
      </details>
    </div>
  );
}
