"use client";

import "../../login/form.css";
import { useSearchParams } from "next/navigation";

export default function Page() {
  const pPesquisa = useSearchParams();
  const id = Number(pPesquisa.get("id"));

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    const formData = new FormData(form);
    const url = `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/reclamacao/${id}/contestar`;
    const data = { id: id, motivo: formData.get("motivo") };
    const requisicao = await fetch(url, {
      method: "POST",
      credentials: "include" as RequestCredentials,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    return await requisicao.json();
  }
  return (
    <main className="flex justify-center">
      <form
        onSubmit={handleSubmit}
        className="flex flex-col gap-2 bg-gray-800 rounded-xl p-2 px-10"
      >
        <label htmlFor="motivo">
          Motivo<span className="text-red-500">*</span>
        </label>
        <input
          required
          id="motivo"
          name="motivo"
          type="text"
          placeholder="Insira o motivo"
        />
        <button type="submit" className="rounded">
          Adicionar
        </button>
      </form>
    </main>
  );
}
