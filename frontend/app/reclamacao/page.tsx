"use client";

import { useSearchParams } from "next/navigation";
import getInfoReclamacao from "./actions";
import { useState, useEffect, Key } from "react";
import  toLocal  from "@/utils/localTime";

export default function Page() {
  const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL;

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
          <li>Data criada: {toLocal(reclamacao.dataCriacao)}</li>
          <li>Data resolvida: {toLocal(reclamacao.dataResolucao)}</li>
          <li>Data atualizada: {toLocal(reclamacao.dataAtualizacao)}</li>
        </ul>
        <div>
          {reclamacao.fotos.map((foto: any) => (
            <img key={foto.id} src={API_URL+foto.url} alt="" />
          ))}
        </div>
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
