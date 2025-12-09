export type StatusReclamacao = "Pendente" | "Resolvida" | "Contestada";

export interface Imagem {
    id: number,
    url: string,
    nomeArquivo: string,
    dataUpload: string,
}

export interface Contestacao {
    id: number,
    motivo: string,
    reclamacaoId: number,
    usuarioId: number,
    autor: string,
    dataContestacao: string,
    tituloReclamacao: string,
    provas: Imagem[],
}

export interface Reclamacao {
    id: number,
    titulo: string,
    descricao: string,
    cidade: string,
    endereco: string,
    latitude: number,
    longitude: number,
    status: StatusReclamacao,
    usuarioId: number,
    autor: string,
    dataCriacao: string,
    dataResolucao: string,
    dataAtualizacao: string,
    fotos: Imagem[],
    constestacoes: Contestacao[],
}