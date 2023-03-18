export const register = async (data) => {
  let content;
  try {
    const rawResponse = await fetch("http://127.0.0.1:8000/auth/register", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "http://127.0.0.1:8000",
      },
      body: JSON.stringify(data),
    });
    content = await rawResponse.json();
  } catch (error) {
    content = error;
  }

  return content;
};

export const login = async (data) => {
  var formBody = [];
  for (var property in data) {
    var encodedKey = encodeURIComponent(property);
    var encodedValue = encodeURIComponent(data[property]);
    formBody.push(encodedKey + "=" + encodedValue);
  }
  formBody = formBody.join("&");
  let content;
  try {
    const rawResponse = await fetch("http://127.0.0.1:8000/auth/jwt/login", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "Access-Control-Allow-Origin": "http://127.0.0.1:8000",
      },
      body: formBody,
    });
    content = await rawResponse.json();
  } catch (error) {
    content = error;
  }

  return content;
};

export const getUserId = async (token) => {
  let content;
  try {
    const rawResponse = await fetch(
      "http://127.0.0.1:8000/protected-route-only-jwt",
      {
        method: "GET",
        headers: {
          Accept: "application/json",
          "Access-Control-Allow-Origin": "http://127.0.0.1:8000",
          Authorization: `Bearer ${token}`,
        },
      }
    );
    content = await rawResponse.json();
  } catch (error) {
    content = error;
  }

  return content;
};

export const forgotPassword = async (data) => {
  let content;
  try {
    const rawResponse = await fetch(
      "http://127.0.0.1:8000/auth/forgot-password",
      {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "http://127.0.0.1:8000",
        },
        body: JSON.stringify(data),
      }
    );
    content = await rawResponse.json();
  } catch (error) {
    content = error;
  }

  return content;
};
