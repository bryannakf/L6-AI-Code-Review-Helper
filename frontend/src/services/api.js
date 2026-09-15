const API_URL =
  import.meta.env.VITE_API_URL ||
  (window.location.hostname === "localhost" ||
  window.location.hostname === "127.0.0.1"
    ? "/api"
    : `${window.location.origin}/api`);


export async function analyseCode(
  code,
  language,
  secretConfirmed = false
) {
  const response = await fetch(
    `${API_URL.replace(/\/$/, "")}/review`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        code,
        language,
        secret_confirmed: secretConfirmed,
      }),
    }
  );

  const contentType =
    response.headers.get("content-type") || "";

  const rawText = await response.text();

  let data;

  if (contentType.includes("application/json")) {
    data = rawText ? JSON.parse(rawText) : {};
  } else if (rawText) {
    data = {
      error: `Unexpected API response: ${rawText.slice(
        0,
        180
      )}`,
    };
  } else {
    data = {};
  }

  if (!response.ok) {
    const error = new Error(
      data.error || "Code review failed"
    );

    error.response = {
      data,
      status: response.status,
    };

    throw error;
  }

  return data;
}