"use server";

export default async function getReclamacao(id: number) {
  const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
  const response = await fetch(`${apiUrl}/api/reclamacao/${id}`);
  const data = await response.json();

  return {
    ok: response.ok,
    status: response.status,
    data: data,
  };
}
