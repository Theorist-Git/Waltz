const enc = new TextEncoder();

async function return_key(password) {
    const passwordKey = await window.crypto.subtle.importKey("raw", enc.encode(password), "PBKDF2", false, [
        "deriveKey",
    ]);
    const salt = window.crypto.getRandomValues(new Uint8Array(16));

    return window.crypto.subtle.deriveKey({
            name: "PBKDF2",
            salt: new Uint8Array(0),
            iterations: 250000,
            hash: "SHA-256",
        },
        passwordKey, {
            name: "AES-GCM",
            length: 256
        },
        false,
        ["encrypt", "decrypt"]
    );
}

async function store_key(user_id) {

    const password = window.document.getElementById("PASSWORD").value;
    const aesKey = await return_key(password);

    callOnStore(function(store) {
        store.put({
            id: user_id,
            key: aesKey
        });
    })
}