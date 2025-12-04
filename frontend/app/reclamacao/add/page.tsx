"use client";
import "../../login/form.css";
import { useState } from "react";

export default function Page() {
  const [files, setFiles] = useState<File[]>([]);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    
    const formData = new FormData(form);
    
    const url = `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/reclamacao/adicionar`;
    const resp = await fetch(url, {
      method: "POST",
      credentials: "include" as RequestCredentials,
      body: formData,
    });
    return resp;
  }


  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return;

    const files = Array.from(e.target.files);
    setFiles(files);
  };
  return (
    <main className="flex align-center justify-center h-full">
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
        <input type="file" name="fotos" multiple onChange={handleFileChange} accept="image/*"/>
        <ul>
          {files.map((file, index) => (
          <li key={index}>{file.name}</li>
          ))}
      </ul>
        <button type="submit" className="rounded">
          Adicionar
        </button>
      </form>
    </main>
  );
}
