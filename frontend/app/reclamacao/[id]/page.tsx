import CardReclamacao from "./CardReclamacao";
import getReclamacao from "../actions";
import { notFound } from "next/navigation";


interface PageProps {
  params: {
    id: string
  }
}

export default async function Page({ params }: PageProps) {
  const { id } = await params;

  const reclamacaoId = Number(id);
  if (!Number.isInteger(reclamacaoId)) {
    notFound();
  } 
  const response = await getReclamacao(reclamacaoId);
  if (response.status === 404) {
    notFound();
  }
  const reclamacao = response.data.reclamacao;

  return (
    <CardReclamacao reclamacao={reclamacao}/>
  );
}
