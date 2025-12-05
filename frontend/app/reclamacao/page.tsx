"use client";

import { useSearchParams } from "next/navigation";
import getInfoReclamacao from "./actions";
import { useState, useEffect, Key } from "react";
import toLocal from "@/utils/localTime";

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
      <div className="flex flex-col p-3 bg-gray-800 rounded-xl mx-[100px]">
        <h1 className="text-[20px] font-bold">{reclamacao.titulo}</h1>
        <h3 className="text-[15px] font-bold">{reclamacao.descricao}</h3>
        <ul>
          <li>Cidade: {reclamacao.cidade}</li>
          <li>Endreço: {reclamacao.endereco}</li>
          <li>Status: {reclamacao.status}</li>
          <li>Autor: {reclamacao.autor}</li>
          <li>Data criada: {toLocal(reclamacao.dataCriacao)}</li>
          <li>Data resolvida: {toLocal(reclamacao.dataResolucao)}</li>
          <li>Data atualizada: {toLocal(reclamacao.dataAtualizacao)}</li>
        </ul>
        <div className="flex flex-row gap-[20px] justify-center items-center">
          {reclamacao.fotos.map((foto: any) => (
            <img
              className="w-[200px]"
              key={foto.id}
              src={API_URL + foto.url}
              alt=""
            />
          ))}
        </div>
      </div>
    );
  } else {
    return (
      <main className="flex justify-center">
        <h1>Reclamação não encontrada</h1>
      </main>
    );
  }
}
