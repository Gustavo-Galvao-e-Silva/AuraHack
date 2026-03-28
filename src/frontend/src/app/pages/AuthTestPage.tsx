import { 
  SignedIn, 
  SignedOut, 
  SignInButton, 
  UserButton, 
  useUser 
} from "@clerk/clerk-react";

export default function AuthTestPage() {
  const { user } = useUser();

  return (
    <div style={{ padding: "2rem", textAlign: "center", backgroundColor: "#effaff", minHeight: "100vh" }}>
      <h1 style={{ color: "#037682" }}>Teste de Autenticação AuraHack</h1>
      
      {/* O que aparece quando NÃO está logado */}
      <SignedOut>
        <p>Você não está autenticado.</p>
        <div style={{ 
          backgroundColor: "#0a7f8a", 
          color: "white", 
          padding: "10px 20px", 
          borderRadius: "8px",
          display: "inline-block",
          cursor: "pointer" 
        }}>
          <SignInButton mode="modal" />
        </div>
      </SignedOut>

      {/* O que aparece quando ESTÁ logado */}
      <SignedIn>
        <p>Bem-vindo, <strong>{user?.firstName}</strong>!</p>
        <p>Seu e-mail: {user?.primaryEmailAddress?.emailAddress}</p>
        <div style={{ marginTop: "20px" }}>
          <UserButton afterSignOutUrl="/" />
        </div>
      </SignedIn>
    </div>
  );
}