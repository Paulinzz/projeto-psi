"use server";

export default async function Page() {
  const url = `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/reclamacoes`;

  const resp = await fetch(url, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });
  const data = await resp.json();
  const lista = data.reclamacoes;

  return (
    <>
      {lista.map((reclamacao) => (
        <div key={reclamacao.id}>
          {reclamacao.autor},{reclamacao.titulo},{reclamacao.descricao},
          {reclamacao.cidade},{reclamacao.status}
        </div>
      ))}
    </>
  );
}
