"use client"

export default function toLocal(isoString: string) {
    if (!isoString) {
        return null;
    }
    const date = new Date(isoString);
    return date.toLocaleString("pt-BR");
}
