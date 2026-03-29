import { UserButton, useUser } from "@clerk/clerk-react";
import { FlaskConical, LayoutDashboard, FileText, MessageSquare } from "lucide-react";
import { motion } from "motion/react";

export default function Dashboard() {
  const { user } = useUser();

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header do Dashboard */}
      <header className="border-b border-border bg-card/50 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-linear-to-br from-primary to-secondary flex items-center justify-center shadow-lg">
              <FlaskConical className="w-5 h-5 text-primary-foreground" />
            </div>
            <span className="text-xl font-bold bg-linear-to-r from-primary to-secondary bg-clip-text text-transparent">
              TrialMatch
            </span>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm font-medium text-muted-foreground">
              {user?.firstName || "User"}
            </span>
            <UserButton afterSignOutUrl="/" />
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-7xl mx-auto w-full p-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          
          {/* Sidebar Interna (Menu) */}
          <aside className="md:col-span-1 space-y-2">
            <nav className="space-y-1">
              {[
                { name: "Overview", icon: LayoutDashboard },
                { name: "My Records", icon: FileText },
                { name: "Messages", icon: MessageSquare },
              ].map((item) => (
                <button
                  key={item.name}
                  className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all hover:bg-primary/10 text-muted-foreground hover:text-primary"
                >
                  <item.icon className="w-5 h-5" />
                  {item.name}
                </button>
              ))}
            </nav>
          </aside>

          {/* Conteúdo Principal (Usando sua classe 'glass') */}
          <section className="md:col-span-3">
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="glass p-8 rounded-2xl min-h-100"
            >
              <h1 className="text-3xl font-bold mb-4">Welcome back, {user?.firstName}!</h1>
              <p className="text-muted-foreground mb-8">
                Manage your medical records and track your trial matches here.
              </p>

              {/* Card de Exemplo */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="p-6 rounded-xl bg-card border border-border shadow-sm">
                  <h3 className="font-bold text-primary mb-2">Patient Profile</h3>
                  <p className="text-sm text-muted-foreground">Complete your data to improve matching.</p>
                </div>
                <div className="p-6 rounded-xl bg-card border border-border shadow-sm">
                  <h3 className="font-bold text-secondary mb-2">Trial Matches</h3>
                  <p className="text-sm text-muted-foreground">You have 0 new matches today.</p>
                </div>
              </div>
            </motion.div>
          </section>
        </div>
      </main>
    </div>
  );
}