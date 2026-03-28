import { ClerkProvider } from "@clerk/clerk-react";
import { RouterProvider, useNavigate } from "react-router-dom";
import { router } from "./routes";

// Este componente resolve a navegação do Clerk usando o router
function ClerkWrapper({ children }: { children: React.ReactNode }) {
  const navigate = useNavigate();
  const CLERK_PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY || "";

  return (
    <ClerkProvider 
      publishableKey={CLERK_PUBLISHABLE_KEY}
      routerPush={(to) => navigate(to)}
      routerReplace={(to) => navigate(to, { replace: true })}
    >
      {children}
    </ClerkProvider>
  );
}

export default function App() {
  return (
    <RouterProvider router={router} />
  );
}