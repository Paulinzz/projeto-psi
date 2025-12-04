"use server";

export default async function getInfoReclamacao(id: number) {
  const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
  const request = await fetch(`${apiUrl}/api/reclamacao/${id}`);
  const dados = await request.json();
  const reclamacao = await dados.reclamacao;
  return reclamacao;
}
