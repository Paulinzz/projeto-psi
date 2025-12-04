"use client";

import { useSearchParams } from "next/navigation";
import getInfoReclamacao from "./actions";
import { useState, useEffect } from "react";

export default function Page() {
  const pPesquisa = useSearchParams();
  const id = pPesquisa.get("id");

  const [reclamacao, setReclamacao] = useState<any | null>(null);

  useEffect(() => {
    if (id) {
      (async () => {
        const dados = await getInfoReclamacao(Number(id));

        setReclamacao(dados);
      })();
    }
  }, [id]);

  if (reclamacao) {
    return (
      <main>
        <h1>{reclamacao.titulo}</h1>
        <h3>{reclamacao.descricao}</h3>
        <ul>
          <li>Cidade: {reclamacao.cidade}</li>
          <li>Endreço: {reclamacao.endereco}</li>
          <li>Status: {reclamacao.status}</li>
          <li>Autor: {reclamacao.autor}</li>
          <li>Data criada: {reclamacao.dataCriacao}</li>
          <li>Data resolvida: {reclamacao.dataResolucao}</li>
          <li>Data atualizada: {reclamacao.dataAtualizacao}</li>
        </ul>
      </main>
    );
  } else {
    return (
      <main className="flex justify-center">
        <h1>Reclamação não encontrada</h1>
      </main>
    );
  }
}
