// for large strings, use this from https://stackoverflow.com/a/49124600
const enc = new TextEncoder();
const dec = new TextDecoder();

const base64_to_buf = (b64) =>
  Uint8Array.from(atob(b64), (c) => c.charCodeAt(null));

const buff_to_base64 = (buff) => btoa(
    new Uint8Array(buff).reduce(
        (data, byte) => data + String.fromCharCode(byte), ''
    )
);

async function encrypt() {
    const data = window.document.getElementById("PASSWORD").value;
    callOnStore(function(store) {
        let getData = store.get(1);
        getData.onsuccess = async function() {
            let key = getData.result.key;
            window.document.add_record.PASSWORD.value = await encryptData(data, key);
            const test = window.document.getElementById("PASSWORD").value;
            // document.getElementById("add-sub").click()
        };
    })
}

async function decrypt() {
    const encryptedData = window.document.getElementById("PASSWORD").value;
    callOnStore(function(store) {
        let getData = store.get(1);
        getData.onsuccess = async function() {
            let key = getData.result.key;
            window.document.add_record.PASSWORD.value = await decryptData(encryptedData, key);
            // document.getElementById("add-sub").click()
        };
    })

}

function callOnStore(fn_) {

    // This works on all devices/browsers, and uses IndexedDBShim as a final fallback
    let indexedDB = window.indexedDB;
    // Open (or create) the database
    let open = indexedDB.open("Waltz", 4);

    // Create the schema
    open.onupgradeneeded = function() {
        let db = open.result;
        let store = db.createObjectStore("WaltzKeyStore", {
            keyPath: "id",
            autoIncrement: true
        });
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

async function encryptData(secretData, aesKey) {
    try {
        const salt = window.crypto.getRandomValues(new Uint8Array(16));
        const iv = window.crypto.getRandomValues(new Uint8Array(12));
        const encryptedContent = await window.crypto.subtle.encrypt({
                name: "AES-GCM",
                iv: iv,
            },
            aesKey,
            enc.encode(secretData)
        );

        const encryptedContentArr = new Uint8Array(encryptedContent);
        let buff = new Uint8Array(
            salt.byteLength + iv.byteLength + encryptedContentArr.byteLength
        );
        buff.set(salt, 0);
        buff.set(iv, salt.byteLength);
        buff.set(encryptedContentArr, salt.byteLength + iv.byteLength);
        const base64Buff = buff_to_base64(buff);
        return base64Buff;
    } catch (e) {
        console.log(`Error - ${e}`);
        return "";
    }
}

async function decryptData(encryptedData, aesKey) {
  try {
    const encryptedDataBuff = base64_to_buf(encryptedData);
    const iv = encryptedDataBuff.slice(16, 16 + 12);
    const data = encryptedDataBuff.slice(16 + 12);

    const decryptedContent = await window.crypto.subtle.decrypt(
      {
        name: "AES-GCM",
        iv: iv,
      },
      aesKey,
      data
    );
    return dec.decode(decryptedContent);
  } catch (e) {
    console.log(`Error - ${e}`);
    return "";
  }
}