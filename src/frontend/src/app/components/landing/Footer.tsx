import { FlaskConical } from "lucide-react";

export function Footer() {
    return(
      <footer className="border-t border-border bg-card/30 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-linear-to-br from-primary to-secondary flex items-center justify-center">
                <FlaskConical className="w-5 h-5 text-primary-foreground" />
              </div>
              <span className="font-bold bg-linear-to-r from-primary to-secondary bg-clip-text text-transparent">
                TrialMatch
              </span>
            </div>
            <p className="text-sm text-muted-foreground">
              © 2026 TrialMatch. Developed for the Hackathon.
            </p>
          </div>
        </div>
      </footer>
    );
}