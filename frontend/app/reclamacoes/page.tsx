import ListaReclamacoes from "./ListaReclamacoes";

export default async function Page() {
  const url = `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/reclamacoes`;

  const resp = await fetch(url, { method: "GET" });
  const data = await resp.json();

  return (
    <main>
      <ListaReclamacoes lista={data.reclamacoes} />
    </main>
  );
}
