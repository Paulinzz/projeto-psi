"use client";

import { useState, useEffect } from "react";
import toLocal from "@/utils/localTime";
import clsx from "clsx";
import { useRouter } from "next/navigation";

export default function Page() {
  const router = useRouter();
  const [reclamacoes, setReclamacoes] = useState<[] | null>(null);
  const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL;

  async function getDados() {
    const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    const url = `${apiUrl}/api/usuario/reclamacoes`;
    const request = await fetch(url, {
      method: "GET",
      credentials: "include" as RequestCredentials,
    });
    return await request.json();
  }

  useEffect(() => {
    if (reclamacoes === null) {
      (async () => {
        const dados = await getDados();

        setReclamacoes(dados.reclamacoes);
      })();
    }
  });
  if (reclamacoes) {
    return (
      <div className="flex flex-row justify-center items-center gap-[50px]">
        {reclamacoes.map((reclamacao) => (
          <div
            key={reclamacao.id}
            className="p-5 bg-gray-800 rounded-xl flex flex-col gap-2"
          >
            <ul className="flex flex-col gap-5">
              <li>Autor: {reclamacao.autor}</li>
              <li>Titulo: {reclamacao.titulo}</li>
              <li>Descrição: {reclamacao.descricao}</li>
              <li>Cidade: {reclamacao.cidade}</li>
              <li
                className={clsx("p-2 rounded-xl", {
                  "bg-green-600": reclamacao.status === "Resolvida",
                  "bg-yellow-600": reclamacao.status === "Pendente",
                  "bg-red-600": reclamacao.status === "Contestada",
                })}
              >
                Status: {reclamacao.status}
              </li>
            </ul>
            <button
              className="bg-gray-700 rounded p-3 cursor-pointer"
              onClick={() => {
                router.push(`/reclamacao?id=${reclamacao.id}`);
              }}
            >
              Acessar reclamação
            </button>
            <button
              className={clsx("bg-gray-700 rounded p-3 cursor-pointer", {
                invisible: ["Resolvida", "Contestada"].includes(
                  reclamacao.status,
                ),
              })}
              type="button"
              onClick={async () => {
                await handleResolver(reclamacao.id);
                router.refresh();
              }}
            >
              Resolver reclamação
            </button>
          </div>
        ))}
      </div>
    );
  } else {
    return (
      <>
        <h1>Erro</h1>
      </>
    );
  }
}
