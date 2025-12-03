"use client";
import "../../login/form.css";

export default function Page(formData: FormData) {
  async function handleSubmit() {
    const url = `${process.env.NEXT_PUBLIC_BACKEND_URL}/reclamacao/adicionar`;
    const resp = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        titulo: formData.get("titulo"),
        descricao: formData.get("descricao"),
        cidade: formData.get("cidade"),
        endereco: formData.get("endereco"),
        fotos: formData.get("fotos"),
      }),
    });
    return resp;
  }
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
        <input type="file" name="fotos" multiple />
        <button type="submit" className="rounded">
          Adicionar
        </button>
      </form>
    </main>
  );
}
