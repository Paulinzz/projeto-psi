"use client";

import React, { useState } from "react";
import cadastroAction from "./actions";

export default function CadastroForm() {
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError("");
    setIsSubmitting(true);

    const form = e.currentTarget;
    const formData = new FormData(form);
    const data = {
      username: String(formData.get("nome")),
      email: String(formData.get("email")),
      password: String(formData.get("senha")),
    };

    const result = await cadastroAction(data);
    if (result) {
      setError(result);
    }
    setIsSubmitting(false);
  }

  return (
    <main className="flex justify-center">
      <form
        onSubmit={onSubmit}
        className="flex flex-col gap-2 bg-gray-800 rounded-xl p-2 px-5"
      >
        <label htmlFor="nome">Nome</label>
        <input type="text" id="nome" name="nome" required />

        <label htmlFor="email">Email</label>
        <input type="email" id="email" name="email" required />

        <label htmlFor="senha">Senha</label>
        <input type="password" id="senha" name="senha" required />

        <button
          className="rounded cursor-pointer"
          type="submit"
          disabled={isSubmitting}
        >
          {
            isSubmitting ? "Entrando..." : "Iniciar sessão"
            // OPERADOR TERNÁRIO
            // condição ? True : False

            // se a variavel for true, retorna Entrando..., se for false, retorna iniciar sessão
          }
        </button>
        {
          error && <p>{error}</p>
          // SHORT-CIRCUIT
          // retorna <p>{error}</p>, CASO error não seja um Falsy Value
          // Falsy Value: "", 0, false, null, undefined, NaN

          // se erro existe, renderiza o <p>, se não existe, nada é renderizado
        }
      </form>
    </main>
  );
}
