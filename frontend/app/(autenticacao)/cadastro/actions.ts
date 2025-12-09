"use server";

export default async function cadastroAction(
    data: { 
        username: string; 
        email: string; 
        password: string; 
    }
) {
    const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

    const url = `${apiUrl}/api/cadastro`;
    const options = {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    }
    const response = await fetch(url, options);
    const json = await response.json();
    return {
        ok: response.ok,
        status: response.status,
        data: json
    };
}