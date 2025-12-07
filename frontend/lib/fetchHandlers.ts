
export type Usuario = {
  autenticado: Boolean;
  usuario: {
    id: Number;
    nome: String;
    email: String;
  } | null;
}

export async function getUsuario(): Promise<Usuario> {
  "use client"
  const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
  const response = await fetch(`${apiUrl}/api/me`,
    {
      method: "GET",
      credentials: "include" as RequestCredentials
    }
  );

  const data: Usuario = await response.json();

  return data;
}