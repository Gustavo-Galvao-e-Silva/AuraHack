import { useState } from "react";
import { useUser } from "@clerk/clerk-react";
import axios from "axios";
import { motion, AnimatePresence } from "motion/react";
import { DashboardLayout } from "../../components/shared/DashboardLayout";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Search, ShieldCheck, Loader2, AlertCircle, CheckCircle } from "lucide-react";

export default function ClaimResearch() {
  const { user } = useUser();
  const [nctId, setNctId] = useState("");
  const [status, setStatus] = useState<"idle" | "verifying" | "success" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState("");

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) return;

    setStatus("verifying");
    setErrorMessage("");

    try {
      const response = await axios.post(
        "http://localhost:8000/research/claim_research",
        null,
        {
          params: {
            researcher_email: user.primaryEmailAddress?.emailAddress,
            nct_id: nctId,
            clerk_user_id: user.id,
          },
        }
      );

      if (response.status === 201) {
        setStatus("success");
        console.log(response.data);
      }
    } catch (error: any) {
      setStatus("error");

      const detail = error.response?.data?.detail;

      if (error.response?.status === 409) {
        setErrorMessage("This study has already been claimed by someone else.");
      } else if (error.response?.status === 403) {
        setErrorMessage("Verification failed: Your email does not match the study contacts.");
      } else if (Array.isArray(detail)) {
        // 🔥 FIX PRINCIPAL
        setErrorMessage(detail.map((e: any) => e.msg).join(", "));
      } else if (typeof detail === "string") {
        setErrorMessage(detail);
      } else {
        setErrorMessage("An unexpected error occurred.");
      }
    }
  };

  return (
    <DashboardLayout role="researcher">
      <div className="max-w-2xl mx-auto pt-12 text-center space-y-8">
        <motion.div initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}>
          <div className="w-20 h-20 bg-primary/10 rounded-3xl flex items-center justify-center mx-auto mb-6">
            <ShieldCheck className="w-10 h-10 text-primary" />
          </div>
          <h1 className="text-4xl font-bold text-foreground">Verify Research Ownership</h1>
          <p className="text-muted-foreground mt-2">
            Logged in as:{" "}
            <span className="text-primary font-bold">
              {user?.primaryEmailAddress?.emailAddress}
            </span>
          </p>
        </motion.div>

        <form onSubmit={handleVerify} className="relative">
          <div className="relative group">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-6 h-6 text-muted-foreground group-focus-within:text-primary transition-colors" />
            <Input
              placeholder="NCT01234567"
              value={nctId}
              onChange={(e) => setNctId(e.target.value.toUpperCase())}
              className="pl-12 h-16 text-xl bg-card border-2 border-border focus:border-primary rounded-2xl shadow-sm glow"
              required
              disabled={status === "verifying"}
            />
          </div>

          <Button
            type="submit"
            size="lg"
            className="mt-6 w-full h-14 text-lg font-bold shadow-lg shadow-primary/20"
            disabled={status === "verifying" || !nctId}
          >
            {status === "verifying" && <Loader2 className="animate-spin mr-2" />}
            {status === "verifying"
              ? "Accessing ClinicalTrials.gov..."
              : "Claim Research"}
          </Button>
        </form>

        <AnimatePresence mode="wait">
          {status === "success" && (
            <motion.div
              key="success"
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              className="p-8 rounded-2xl bg-primary/10 border border-primary/30 text-foreground"
            >
              <CheckCircle className="w-12 h-12 text-primary mx-auto mb-4" />
              <h3 className="font-bold text-xl">Success!</h3>
              <p className="text-sm opacity-80 mt-2">
                The study has been verified and attached to your dashboard.
              </p>
              <Button
                className="mt-6 bg-primary"
                onClick={() => (window.location.href = "/researcher")}
              >
                Go to Dashboard
              </Button>
            </motion.div>
          )}

          {status === "error" && (
            <motion.div
              key="error"
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              className="p-6 rounded-2xl bg-destructive/10 border border-destructive/30 text-destructive"
            >
              <AlertCircle className="w-10 h-10 mx-auto mb-3" />
              <h3 className="font-bold text-lg">Verification Failed</h3>
              <p className="text-sm mt-1">
                {errorMessage || "Something went wrong."}
              </p>
              <Button
                variant="outline"
                className="mt-4 border-destructive text-destructive"
                onClick={() => setStatus("idle")}
              >
                Try Another ID
              </Button>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </DashboardLayout>
  );
}