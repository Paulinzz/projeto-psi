"use client";

import { redirect } from "next/navigation";

export default async function loginAction(data: {
    email: string;
    password: string;
}) {
    const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

    const url = `${apiUrl}/api/login`;
    const options = {
        method: "POST",
        credentials: "include" as RequestCredentials,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    };

    const response = await fetch(url, options);
    const result = await response.json();
    if (response.status !== 200) {
        return result.message;
    }
    // redirect("/");
}
