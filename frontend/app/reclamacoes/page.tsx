import ListaReclamacoes from "./ListaReclamacoes";
import Link from "next/link";
import Button from "@/components/ui/Button";

export default async function Page() {
  const url = `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/reclamacoes`;

  const resp = await fetch(url, { method: "GET" });
  const data = await resp.json();

  return (
    <>
      <div className="flex items-center justify-center">
        <Link href="/reclamacao/adicionar">
          <Button content="Adicionar reclamação" />
        </Link>
      </div>
      <ListaReclamacoes lista={data.reclamacoes} />
    </>
  );
}
