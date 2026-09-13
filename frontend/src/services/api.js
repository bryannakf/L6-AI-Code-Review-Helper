const API_URL = import.meta.env.VITE_API_URL || "/api";

export async function analyseCode(code, language) {
  const response = await fetch(`${API_URL.replace(/\/$/, "")}/review`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      code,
      language,
    }),
  });

  const contentType = response.headers.get("content-type") || "";
  const rawText = await response.text();

  let data;

  if (contentType.includes("application/json")) {
    data = rawText ? JSON.parse(rawText) : {};
  } else if (rawText) {
    data = {
      error: `Unexpected API response: ${rawText.slice(0, 180)}`,
    };
  } else {
    data = {};
  }

  if (!response.ok) {
    throw new Error(data.error || "Code review failed");
  }

  return data;
}
