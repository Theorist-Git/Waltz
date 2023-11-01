const enc = new TextEncoder();

async function return_key(password) {
    const passwordKey = await window.crypto.subtle.importKey("raw", enc.encode(password), "PBKDF2", false, [
    "deriveKey",
  ]);
    const salt = window.crypto.getRandomValues(new Uint8Array(16));

    return window.crypto.subtle.deriveKey(
    {
      name: "PBKDF2",
      salt: salt,
      iterations: 250000,
      hash: "SHA-256",
    },
    passwordKey,
    { name: "AES-GCM", length: 256 },
    false,
    ["encrypt", "decrypt"]
  );
}

function callOnStore(fn_) {

	// This works on all devices/browsers, and uses IndexedDBShim as a final fallback
	let indexedDB = window.indexedDB;
	// Open (or create) the database
	let open = indexedDB.open("Waltz", 4);

	// Create the schema
	open.onupgradeneeded = function() {
	    let db = open.result;
	    let store = db.createObjectStore("WaltzKeyStore", {keyPath: "id", autoIncrement: true});
	};


	open.onsuccess = function() {
	    // Start a new transaction
	    let db = open.result;
	    let tx = db.transaction("WaltzKeyStore", "readwrite");
	    let store = tx.objectStore("WaltzKeyStore");

	    fn_(store)

	    // Close the db when the transaction is done
	    tx.oncomplete = function() {
	        db.close();
	    };
	}
}

async function store_key() {

    const password = window.document.getElementById("PASSWORD").value;
    const aesKey = await return_key(password);

    callOnStore(function (store) {
        store.put({key: aesKey});
    })
}