import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useToast } from "@/components/ui/use-toast";
import { Clipboard, Loader2 } from "lucide-react";
import { generateVocabulary } from "@/services/vocabularyService";

export const WordGenerator = () => {
  const { toast } = useToast();
  const [category, setCategory] = useState("");
  const [count, setCount] = useState("5");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const words = await generateVocabulary({
        theme: category,
        count: parseInt(count)
      });

      setResult(words);
    } catch (error) {
      console.error('Error in handleSubmit:', error);
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to generate words. Please try again.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = async () => {
    if (!result) return;
    try {
      await navigator.clipboard.writeText(JSON.stringify(result, null, 2));
      toast({
        title: "Success",
        description: "Copied to clipboard",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to copy to clipboard",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <div className="container mx-auto p-6">
        <div className="mb-8">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900">German Vocabulary Generator</h2>
          <p className="text-lg text-gray-600 mt-2">Generate German vocabulary words based on a theme.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Form Section */}
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <label htmlFor="category" className="text-sm font-medium text-gray-700">
                  Theme
                </label>
                <Input
                  id="category"
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  placeholder="e.g., food, animals, professions"
                  className="transition-all duration-200 focus:ring-2 focus:ring-gray-400"
                  required
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="count" className="text-sm font-medium text-gray-700">
                  Number of Words (1-50)
                </label>
                <Input
                  id="count"
                  type="number"
                  value={count}
                  onChange={(e) => setCount(e.target.value)}
                  min="1"
                  max="50"
                  className="transition-all duration-200 focus:ring-2 focus:ring-gray-400"
                  required
                />
              </div>

              <Button
                type="submit"
                disabled={loading}
                className="w-full bg-gray-900 hover:bg-gray-800 text-white transition-all duration-200"
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Generating...
                  </>
                ) : (
                  "Generate Vocabulary"
                )}
              </Button>
            </form>
          </div>

          {/* Results Section */}
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <label className="text-sm font-medium text-gray-700">Generated Vocabulary</label>
              {result && (
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  onClick={handleCopy}
                  className="hover:bg-gray-100"
                >
                  <Clipboard className="h-4 w-4" />
                </Button>
              )}
            </div>
            <Textarea
              value={result || ""}
              readOnly
              placeholder="Generated vocabulary will appear here..."
              className="h-[calc(100vh-20rem)] min-h-[300px] font-mono text-sm bg-gray-50"
            />
          </div>
        </div>
      </div>
    </div>
  );
};
