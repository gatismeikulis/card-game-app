import { Card, CardContent } from "./ui/card";

interface ErrorMessageProps {
  message: string;
}

export function ErrorMessage({ message }: ErrorMessageProps) {
  if (!message) return null;

  return (
    <Card className="border-destructive">
      <CardContent className="pt-6">
        <p className="text-destructive text-sm">{message}</p>
      </CardContent>
    </Card>
  );
}

