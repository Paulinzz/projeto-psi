"use client";
import "../../login/form.css";
import "./box.css";
import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import getInfoReclamacao from "../actions";

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
  const [files, setFiles] = useState<File[]>([]);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;

    const formData = new FormData(form);

    const url = `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/reclamacao/atualizar`;
    const resp = await fetch(url, {
      method: "POST",
      credentials: "include" as RequestCredentials,
      body: formData,
    });
    return resp;
  }

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    if (!e.target.files) return;

    const files = Array.from(e.target.files);
    setFiles(files);
  }
  if (reclamacao) {
    return (
      <main className="flex align-center justify-center h-full gap-[20px]">
        <div className="flex flex-col gap-5 bg-gray-800 rounded-xl p-2 px-10">
          <h1 className="text-2xl">{reclamacao.titulo}</h1>
          <h3 className="text-xl">{reclamacao.descricao}</h3>
          <hr />
          <ul className="flex flex-col gap-2">
            <li>Cidade: {reclamacao.cidade}</li>
            <li>Endreço: {reclamacao.endereco}</li>
            <li>Status: {reclamacao.status}</li>
            <li>Autor: {reclamacao.autor}</li>
            <li>Data criada: {reclamacao.dataCriacao}</li>
            <li>Data resolvida: {reclamacao.dataResolucao}</li>
            <li>Data atualizada: {reclamacao.dataAtualizacao}</li>
          </ul>
        </div>
        <form
          onSubmit={handleSubmit}
          className="flex flex-col gap-2 bg-gray-800 rounded-xl p-2 px-10"
        >
          <label htmlFor="titulo">
            Titulo<span className="text-red-500">*</span>
          </label>
          <input
            required
            id="titulo"
            name="titulo"
            type="text"
            placeholder="Insira o título"
          />
          <label htmlFor="descricao">
            Descrição<span className="text-red-500">*</span>
          </label>
          <input
            required
            id="descricao"
            name="descricao"
            type="text"
            placeholder="Insira a descrição"
          />
          <label htmlFor="cidade">
            Cidade<span className="text-red-500">*</span>
          </label>
          <input
            required
            id="cidade"
            name="cidade"
            type="text"
            placeholder="Insira a cidade"
          />
          <label htmlFor="endereco">Endereço</label>
          <input
            required
            id="endereco"
            name="endereco"
            type="text"
            placeholder="Insira a cidade"
          />
          <label htmlFor="endereco">Fotos</label>
          <input
            type="file"
            name="fotos"
            multiple
            onChange={handleFileChange}
            accept="image/*"
          />
          <ul>
            {files.map((file, index) => (
              <li key={index}>{file.name}</li>
            ))}
          </ul>
          <button type="submit" className="rounded cursor-pointer">
            Atualizar
          </button>
        </form>
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
