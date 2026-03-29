import { motion } from "motion/react";
import { ArrowRight, FlaskConical } from "lucide-react";
import { Link } from "react-router-dom";
import { Button } from "../ui/button";
import { SignedIn, SignedOut, UserButton } from "@clerk/clerk-react";

const MotionDiv = motion.div;

export function Header() {
  return (
    <MotionDiv
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
    >
      <header className="border-b border-border bg-card/50 backdrop-blur-xl sticky top-0 z-50 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <motion.div
            className="flex items-center gap-2"
            whileHover={{ scale: 1.05 }}
            transition={{ type: "spring", stiffness: 400 }}
          >
            <div className="w-10 h-10 rounded-lg bg-linear-to-br from-primary to-secondary flex items-center justify-center shadow-lg">
              <FlaskConical className="w-6 h-6 text-primary-foreground" />
            </div>
            <span className="text-xl font-bold bg-linear-to-r from-primary to-secondary bg-clip-text text-transparent">
              TrialMatch
            </span>
          </motion.div>

          <div className="flex items-center gap-4">
            <SignedOut>
              <Button asChild variant="outline" className="group">
                <Link to="/login">
                  Sign In
                  <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
                </Link>
              </Button>
            </SignedOut>

            <SignedIn>
              <div className="flex items-center gap-3">
                <span className="text-sm text-muted-foreground font-medium">My Account</span>
                <UserButton afterSignOutUrl="/" />
              </div>
            </SignedIn>
          </div>
        </div>
      </header>
    </MotionDiv>
  );
}