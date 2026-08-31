export async function analyseCode(code, language) {

    const response = await fetch(
        "http://127.0.0.1:5000/api/review",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                code,
                language
            })
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.error || "Review failed"
        );
    }

    return data;
}